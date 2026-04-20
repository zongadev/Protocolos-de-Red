#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <time.h>

#define LOG_FILE "icmp_sniffer.log"

/* Función para escribir en el log con timestamp */
void escribir_log(const char *mensaje) {
    FILE *log = fopen(LOG_FILE, "a");
    if (!log) {
        perror("Error al abrir el archivo de log");
        return;
    }

    time_t ahora = time(NULL);
    struct tm *t = localtime(&ahora);

    fprintf(log, "%04d-%02d-%02d %02d:%02d:%02d - %s\n",
            t->tm_year + 1900, t->tm_mon + 1, t->tm_mday,
            t->tm_hour, t->tm_min, t->tm_sec,
            mensaje);

    fclose(log);
}

int main() {
    int sockfd;
    char buffer[65536];
    struct sockaddr saddr;
    socklen_t saddr_len = sizeof(saddr);

    // Crear raw socket
    sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
    if (sockfd < 0) {
        perror("Socket error");
        return 1;
    }

    printf("Sniffer ICMP iniciado... (Ctrl+C para detener)\n");
    escribir_log("Sniffer ICMP iniciado");

    while (1) {
        ssize_t packet_size = recvfrom(sockfd, buffer, sizeof(buffer), 0,
                                       &saddr, &saddr_len);
        if (packet_size < 0) {
            perror("recvfrom error");
            escribir_log("Error en recvfrom()");
            continue;
        }

        struct iphdr *ip = (struct iphdr *)buffer;

        if (ip->protocol == IPPROTO_ICMP) {
            struct icmphdr *icmp =
                (struct icmphdr *)(buffer + ip->ihl * 4);

            struct sockaddr_in *addr_in =
                (struct sockaddr_in *)&saddr;

            char src_ip[INET_ADDRSTRLEN];
            inet_ntop(AF_INET, &(addr_in->sin_addr),
                      src_ip, INET_ADDRSTRLEN);

            char log_msg[256];
            snprintf(log_msg, sizeof(log_msg),
                     "ICMP capturado: Origen=%s Tipo=%d Código=%d ID=%d Secuencia=%d Tamaño=%ld bytes",
                     src_ip,
                     icmp->type,
                     icmp->code,
                     ntohs(icmp->un.echo.id),
                     ntohs(icmp->un.echo.sequence),
                     packet_size);

            // Mostrar en consola
            printf("%s\n", log_msg);

            // Guardar en archivo
            escribir_log(log_msg);
        }
    }

    close(sockfd);
    return 0;
}

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>

int main() {
    int sockfd;
    char buffer[65536];
    struct sockaddr saddr;
    socklen_t saddr_len = sizeof(saddr);

    // Crear raw socket
    printf("Crea el socket por el que va a escuchar, usando tipo RAW y de protocolo ICMP \n");
    sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
    if (sockfd < 0) {
        perror("Socket error");
        return 1;
    }
     
    printf("Sniffer ICMP iniciado... (Ctrl+C para detener)\n");

    while (1) {
         printf("Espera a recibir un paquete que llegue a traves del socket\n");
        ssize_t packet_size = recvfrom(sockfd, buffer, sizeof(buffer), 0, &saddr, &saddr_len);
        if (packet_size < 0) {
            perror("recvfrom error");
            continue;
        }
         printf("En el momento en el que llega, empieza a desarmar el paquete. \nSetea el inicio del header ip en la misma direccion del inicio del paquete. Como el struct del ip header tiene el tamano del header (valga la redundancia), va a apuntar al inicio de la cabezera terminando en su fin.");
        struct iphdr *ip = (struct iphdr*) buffer;
        if (ip->protocol == IPPROTO_ICMP) {
            printf("\n Hace lo mismo con icmphdr. Inicia la direccion del struct del icmp hdr donde termina el hdr del ip.");
            struct icmphdr *icmp = (struct icmphdr*)(buffer + ip->ihl * 4);
            printf("ICMP capturado: Tipo=%d Código=%d ID=%d Secuencia=%d\n",
                icmp->type,
                icmp->code,
                ntohs(icmp->un.echo.id),
                ntohs(icmp->un.echo.sequence)
            );

            // Guardar en archivo para analizar con Python
            FILE *f = fopen("icmp_packet.bin", "wb");
            if (f) {
                fwrite(buffer, 1, packet_size, f);
                fclose(f);
                printf("Paquete guardado en icmp_packet.bin\n");
                break; // solo capturamos uno para el ejemplo
            }
        }
    }

    close(sockfd);
    return 0;
}

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <unistd.h>
#include <errno.h>
#include <sys/time.h>

#define PACKET_SIZE 4096
#define DEST_IP "127.0.0.1"
#define MAX_PINGS 5

unsigned short checksum(void *b, int len) {
    unsigned short *buf = b;
    unsigned int sum = 0;
    for (; len > 1; len -= 2)
        sum += *buf++;
    if (len == 1)
        sum += *(unsigned char*)buf;
    sum = (sum >> 16) + (sum & 0xFFFF);
    sum += (sum >> 16);
    return ~sum;
}

int main() {
    char packet[PACKET_SIZE];
    struct sockaddr_in dest;
    int sockfd, one = 1;
    struct timeval timeout = {1, 0};  // 1 segundo de timeout
    
    printf("Crea el socket de tipo raw con protocolo ICMP \n");
    sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
    if (sockfd < 0) {
        perror("socket");
        return 1;
    }
    // Permite incluir cabecera IP
    printf("Setea el socket para que no genere el IP header automaticamente \n");
    setsockopt(sockfd, IPPROTO_IP, IP_HDRINCL, &one, sizeof(one));
    // Configura timeout de recepción
    setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout));

    dest.sin_family = AF_INET;
    dest.sin_addr.s_addr = inet_addr(DEST_IP);

    for (int seq = 1; seq <= MAX_PINGS; seq++) {
        memset(packet, 0, PACKET_SIZE);
        printf("Crea la estructura del header de IP y del ICMP seteando la misma direccion inicial del packet al iphdr \n");
        printf("El header va a tomar los bytes que le correspondan a su tamano. \n");
        printf("El ICMPhdr se setea sumando el tamano del iphdr a la direccion del packet, saltando asi el iphdr y seteando el inicio del icmphdr");
        struct iphdr *ip = (struct iphdr *) packet;
        struct icmphdr *icmp = (struct icmphdr *) (packet + sizeof(struct iphdr));

        // IP Header
        ip->ihl = 5;
        ip->version = 4;
        ip->tos = 0;
        ip->tot_len = htons(sizeof(struct iphdr) + sizeof(struct icmphdr));
        ip->id = htons(1234 + seq);
        ip->frag_off = 0;
        ip->ttl = 64;
        ip->protocol = IPPROTO_ICMP;
        ip->saddr = inet_addr("127.0.0.1");  // IP local para pruebas
        ip->daddr = dest.sin_addr.s_addr;
        printf("Calcula el checksum manualmente, antes seteado en cero  \n");
        ip->check = checksum((unsigned short *)ip, sizeof(struct iphdr));

        // ICMP Header
        icmp->type = ICMP_ECHO;
        icmp->code = 0;
        icmp->un.echo.id = htons(1234);
        icmp->un.echo.sequence = htons(seq);
        icmp->checksum = checksum((unsigned short *)icmp, sizeof(struct icmphdr));
        printf("Envia el paquete  \n ");
        if (sendto(sockfd, packet, ntohs(ip->tot_len), 0,
                   (struct sockaddr *)&dest, sizeof(dest)) < 0) {
            perror("sendto");
        } else {
            printf("Ping #%d enviado a %s...\n", seq, DEST_IP);
        }

        // Recibir respuesta
        char recv_buffer[PACKET_SIZE];
        struct sockaddr_in recv_addr;
        socklen_t addr_len = sizeof(recv_addr);

        ssize_t bytes = recvfrom(sockfd, recv_buffer, sizeof(recv_buffer), 0,
                                 (struct sockaddr *)&recv_addr, &addr_len);

        if (bytes < 0) {
            if (errno == EAGAIN || errno == EWOULDBLOCK)
                printf("Timeout esperando respuesta ICMP #%d\n", seq);
            else
                perror("recvfrom");
        } else {
            printf("Setea el socket para recibir el paquete y lo empieza a desarmar de la misma froma que lo inicializamos\n tomando la longitud del header dada en palabras  \n ");
            struct iphdr *recv_ip = (struct iphdr *)recv_buffer;
            struct icmphdr *recv_icmp = (struct icmphdr *)(recv_buffer + (recv_ip->ihl * 4));
            printf("Si el tipo de mensaje recibido es ICMP, printea una cosa sino printea otra. Igual no funciona bien.");
            if (recv_icmp->type == ICMP_ECHOREPLY) { 
                printf("Respuesta ICMP #%d recibida desde %s\n\n",
                       ntohs(recv_icmp->un.echo.sequence),
                       inet_ntoa(recv_addr.sin_addr));
            } else {
                printf("Recibido otro tipo de paquete ICMP: tipo %d\n", recv_icmp->type);
            }
        }

        sleep(1);  // esperar 1 segundo antes del próximo ping
    }

    close(sockfd);
    return 0;
}

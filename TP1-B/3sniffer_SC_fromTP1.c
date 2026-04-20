#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <netinet/tcp.h>
int main() {
    int sockfd;
    char buffer[65536];
    struct sockaddr saddr;
    socklen_t saddr_len = sizeof(saddr);

    // Crear raw socket
    sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_TCP);
    if (sockfd < 0) {
        perror("Socket error");
        return 1;
    }

    printf("Sniffer ICMP iniciado... (Ctrl+C para detener)\n");

    while (1) {
        ssize_t packet_size = recvfrom(sockfd, buffer, sizeof(buffer), 0, &saddr, &saddr_len);
        if (packet_size < 0) {
            perror("recvfrom error");
            continue;
        }
        struct iphdr *ip = (struct iphdr*) buffer;
        if (ip->protocol == IPPROTO_TCP ) {
            struct tcphdr *tcp = (struct tcphdr*)(buffer + ip->ihl * 4);
            if(ntohs(tcp->source) ==8080){
            printf("TCP capturado: Secuencia=%d, Ventana tamano =%d Destino:%d. ; Mensaje:%s \n",
                tcp->seq,
                tcp->window,
                ntohs(tcp->dest),
                ((unsigned char *)(tcp)+(tcp->doff)*4));}
            /*Aca imprime basura pero no por este codigo sino por el cliente
            que no se asegura de que los strings terminen con \n*/
        }
    }

    close(sockfd);
    return 0;
}

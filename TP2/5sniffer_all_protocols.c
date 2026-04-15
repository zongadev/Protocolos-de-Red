#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <netinet/tcp.h>
#include <netinet/udp.h>
#include <linux/if_packet.h>
#include <linux/if_ether.h>

int main() {
    int sockfd;
    char buffer[65536];
    struct sockaddr saddr;
    socklen_t saddr_len = sizeof(saddr);


    sockfd = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_IP));
    if (sockfd < 0) {
        perror("Socket error");
        return 1;
    }

    printf("Sniffer iniciado... (Ctrl+C para detener)\n");

    while (1) {
        ssize_t packet_size = recvfrom(sockfd, buffer, sizeof(buffer), 0, &saddr, &saddr_len);
        if (packet_size < 0) {
            perror("recvfrom error");
            continue;
        }

        struct iphdr *ip = (struct iphdr*)(buffer + sizeof(struct ethhdr));
        printf("IP %s -> %s | VER=%d IHL=%d TTL=%d PROTO=%d LEN=%d ID=%d\n",
           inet_ntoa(*(struct in_addr *)&ip->saddr),
           inet_ntoa(*(struct in_addr *)&ip->daddr),
           ip->version,
           ip->ihl * 4,
           ip->ttl,
           ip->protocol,
           ntohs(ip->tot_len),
           ntohs(ip->id));
        switch(ip->protocol){
            case(IPPROTO_ICMP): {
                struct icmphdr *icmp = (struct icmphdr*)((unsigned char*)ip + ip->ihl * 4);
                printf("ICMP capturado: Tipo=%d Codigo: %d ID=%d SEQ=%d \n",
                    icmp->type,
                    icmp->code,
                    ntohs(icmp->un.echo.id),
                    ntohs(icmp->un.echo.sequence)
                );
                break;
            }
            case(IPPROTO_TCP):{
               struct tcphdr *tcp = (struct tcphdr*)((unsigned char*)ip + ip->ihl * 4);
               printf("TCP %s:%u -> %s:%u | SEQ=%u ACK=%u |WIN=%u LEN=%u\n",
                   inet_ntoa(*(struct in_addr *)&ip->saddr),
                   ntohs(tcp->source),
                   inet_ntoa(*(struct in_addr *)&ip->daddr),
                   ntohs(tcp->dest),
                   ntohl(tcp->seq),
                   ntohl(tcp->ack_seq),
                   ntohs(tcp->window),
                   ntohs(ip->tot_len) - (ip->ihl * 4) - (tcp->doff * 4));
                break;
                }
            case(IPPROTO_UDP):{
                struct udphdr *udp = (struct udphdr*)((unsigned char*)ip + ip->ihl * 4);
                  printf("UDP %s:%u -> %s:%u | LEN=%u\n",
                       inet_ntoa(*(struct in_addr *)&ip->saddr),ntohs(udp->source),
                       inet_ntoa(*(struct in_addr *)&ip->daddr), ntohs(udp->dest),
                       ntohs(udp->len) - sizeof(struct udphdr));
                                                       
                break;
            }
        }
    }

    close(sockfd);
    return 0;
}

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define MAX 1024
#define PORT 8080

int main() {
    int sockfd;
    struct sockaddr_in server_addr,from_addr;
    char buffer[MAX];
    char message[MAX];
    char name[50];

    // Crear socket
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd == -1) {
        perror("Socket falló");
        exit(1);
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr);
    memset(&(server_addr.sin_zero), 0, 8);

    // BIndeo al socket con el sv
    printf("Ingresar nombre: ");
    fgets(name, sizeof(name), stdin);
    name[strcspn(name, "\n")] = 0; // Eliminar salto de línea
    while (1) {
        // Enviar mensaje
        printf("%s: ", name);
        memset(buffer, 0, MAX);
        fgets(message, MAX, stdin);
        snprintf(buffer,MAX,"%s: %s",name,message);
        sendto(sockfd, buffer, strlen(buffer), 0,(struct sockaddr*)&server_addr, sizeof(server_addr));

        if (strncmp(buffer, "FIN", 3) == 0) {
            break;
        }

        // Recibir respuesta
        socklen_t addr_len = sizeof(from_addr);
        memset(buffer, 0, MAX);
        recvfrom(sockfd, buffer, MAX, 0,(struct sockaddr*)&from_addr, &addr_len);
        printf("Servidor: %s", buffer);
    }

    close(sockfd);
    return 0;
}

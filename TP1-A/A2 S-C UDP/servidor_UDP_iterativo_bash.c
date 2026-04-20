#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define MAX 1024
#define PORT 8080
void comm(int sockfd){
    
}
int main() {
    int sockfd;
    char buffer[MAX];
    struct sockaddr_in server_addr, client_addr;
    /*
    sockaddr_in es un struc definida por la libreria <netinet/in.h>
    struct sockaddr_in {
    short sin_family;        // Tipo de dirección
    unsigned short sin_port; // Puerto
    struct in_addr sin_addr; // IP
    char sin_zero[8];        // Padding
};
    */
    

    // Crear socket
    sockfd = socket(AF_INET, SOCK_DGRAM, 0); //sockfd es un nombre generico. No hace falta distinguir entre servidor y cliente
    if (sockfd == -1) {
        perror("Socket no pudo abrirse ... error ...");
        exit(1);
    }

    // Configurar estructura
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);//htons convierte int en tcp/ip format: big endian
    memset(&(server_addr.sin_zero), 0, 8); //limpia bytes de padding (?) rellena la estructura

    // Asociar dirección y puerto
    if (bind(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr)) != 0) {
                        //Casteo ^
        perror("Bind falló");
        exit(1);
    }
    printf("Servidor esperando mensaje en el puerto %d...\n", PORT);
    while(1){
      // Recibir mensaje del cliente
      socklen_t addr_len = sizeof(client_addr);
      memset(buffer, 0, MAX);
      
      recvfrom(sockfd, buffer, sizeof(buffer), 0,(struct sockaddr*)&client_addr, &addr_len);
      
      printf("%s", buffer);

      // Enviar respuesta
      printf("Servidor: ");
      memset(buffer, 0, MAX);
      fgets(buffer, MAX, stdin);
      sendto(sockfd, buffer, strlen(buffer), 0,(struct sockaddr*)&client_addr, addr_len);
      
      if (strncmp(buffer, "FIN", 3) == 0) {
          printf("Servidor finaliza la conexión.\n");
          break;
        }
      
}
    close(sockfd);
    
    return 0;
}

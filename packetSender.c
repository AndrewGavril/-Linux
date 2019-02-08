#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>

#define PORT 12345
#define SERVADDR "fe80::3c26:ad45:e02d:c12a" //адрес получателся

int main()
{
  int sock;
  socklen_t clilen;
  struct sockaddr_in6 server_addr, client_addr;
  char buffer[1024];
  char addrbuf[INET6_ADDRSTRLEN];

  sock = socket(PF_INET6, SOCK_DGRAM, 0);

  if (sock < 0) {
    perror("creating socket");
    exit(1);
  }
  memset(&server_addr, 0, sizeof(server_addr));
  server_addr.sin6_family = AF_INET6;
  inet_pton(AF_INET6, SERVADDR, &server_addr.sin6_addr);

  server_addr.sin6_port = htons(PORT);
  int op;
  char *msg;
  printf("Write number of operation:\n");
  scanf("%d", &op);
  if(op<0 || op>2){
     printf("Wrong input!");
     return 0;}
  if(op==0){
    if (sendto(sock, "send", sizeof("send"), 0,
               (struct sockaddr *)&server_addr,
               sizeof(server_addr)) < 0) {
        perror("sendto failed");
        exit(4);
    }
  }
  if(op==1){
    if (sendto(sock, "delete", sizeof("delete"), 0,
               (struct sockaddr *)&server_addr,
               sizeof(server_addr)) < 0) {
        perror("sendto failed");
        exit(4);
    }
  }
  if(op==2){
    if (sendto(sock, "make", sizeof("make"), 0,
               (struct sockaddr *)&server_addr,
               sizeof(server_addr)) < 0) {
        perror("sendto failed");
        exit(4);
    }
  }
  close(sock);

  return 0;
}

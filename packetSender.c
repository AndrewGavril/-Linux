#include <sys/types.h>
#include <sys/socket.h>
#include <string.h>
#include <netinet/in.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{
	char *message = (char*)malloc(6*sizeof(char));
	int dest_port = 2455;
	struct sockaddr_in6 dest_addr;
	int sockfd;

	sockfd = socket(PF_INET6, SOCK_DGRAM, 0);

	dest_addr.sin6_family = AF_INET6;
	dest_addr.sin6_port = htons(dest_port);
	inet_pton("fe80::24ca:5cff:fe6b:5da6",  &dest_addr.sin6_addr);

	int i = 0;
	while (1){
		sleep(5);
		i++;

		if (i%3 == 1)
			message = "send  ";
		else if (i%3 == 2)
			message = "delete";
		else message = "make";
		printf("Sending '%s' \n", message);
		sendto (sockfd, message, strlen(message)+1, 0 , (struct sockaddr*)&dest_addr, sizeof(struct sockaddr_in6));
	}
	return 0;
}

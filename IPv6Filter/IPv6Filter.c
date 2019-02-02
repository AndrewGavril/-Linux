#include <uapi/linux/ptrace.h>
#include <net/sock.h>
#include <bcc/proto.h>

int ip6_filter(struct __sk_buff *skb) {

	unsigned long byte = load_byte(skb, 14);
	
	int bits[4];
	int i, k;
	
	for(i=7; i>=4; i--){
		k = byte >> i;
		
		if (k & 1)
			bits[7 - i] = 1;
		else bits[7 - i] = 0;
	}

	if (bits[0] == 0 && bits[1] == 1 && bits[2] == 1 && bits[3] == 0)
		return -1;
	return 0;
}

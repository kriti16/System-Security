#include <stdio.h>

void function(int a, int b, int c) {
	char buffer1[5];
	char buffer2[40];
	int i,j;
	for(i=0;i<5;i++)
		buffer1[i] = '\0';
	for(j=0;j<40;j++)
		buffer2[j] = 0;
	a = a + 1;
}

void main() {
	int a,b,c;
	// scanf("%d %d %d",&a,&b,&c);
	function(1,2,3);
}
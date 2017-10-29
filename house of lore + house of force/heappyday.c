#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

#define MAX 100

// gcc heappyday.c -o heappyday -fPIE -pie -fstack-protector -Wl,-z,relro,-z,now

struct H {
	char* m[MAX];
	unsigned long size[MAX];
};

struct H ptr;

int clear_stdin() {
    while (getchar() != '\n');
    return 1;
}

void menu() {
	puts("---------Select--------");
	puts("1.- Create");
	puts("2.- Modify");
	puts("3.- View");
	puts("4.- Delete");
	puts("5.- Exit");
}

void crea() {
	char p[MAX] = {0}; // For one_gadget condition [rsp+0x30] == NULL
	unsigned pos = 0;
	char c;
	puts("Index: ");
	while ((scanf("%u%c", &pos, &c) != 2 || c != '\n') && clear_stdin());
	if (pos < MAX) {
		puts("Enter the size: ");
		while ((scanf("%lu%c", &ptr.size[pos], &c) != 2 || c != '\n') && clear_stdin());
		if (ptr.size[pos] >= 0x80) {
			ptr.m[pos] = malloc(ptr.size[pos]);
			puts("Enter the content: ");
			int n = read(0, ptr.m[pos], ptr.size[pos]);
			ptr.m[pos][n - 1] = '\0';
		} else {
			puts("Bad size.");
		}
	} else {
		puts("Bad index");
	}
}

void modify() {
	unsigned i = 0;
	char c;
	puts("Index: ");
	while ((scanf("%u%c", &i, &c) != 2 || c != '\n') && clear_stdin());
	if (i < MAX) {
		puts("Enter the content: ");
		int n = read(0, ptr.m[i], ptr.size[i]);
		ptr.m[i][n - 1] = '\0';
	} else {
		puts("Bad position");	
	}
}

void ver() {
	unsigned i = 0;
	char c;
	puts("Index: ");
	while ((scanf("%u%c", &i, &c) != 2 || c != '\n') && clear_stdin());
	if (i < MAX) {
		write(1, (char *)ptr.m[i], ptr.size[i]);
	} else {
		puts("Bad index");
	}	
}

void libera() {
	unsigned i = 0;
	char c;
	puts("Index: ");
	while ((scanf("%u%c", &i, &c) != 2 || c != '\n') && clear_stdin());
	if (i < MAX) {
		free(ptr.m[i]);
	} else {
		puts("Bad index");
	}
}	

int main(void) {
	int i = 0;
	char c;
	
	setvbuf(stdin, 0, 2, 0);
  	setvbuf(stdout, 0, 2, 0);

	do {
      		menu();
    		while ((scanf("%u%c", &i, &c) != 2 || c != '\n') && clear_stdin());
    		switch (i) {
	    		case 1: crea(); 
	    		break;
			case 2: modify(); 
			break;
			case 3: ver(); 
			break;
			case 4: libera(); 
			break;
			case 5: printf("Have a heappy day!!\n"); 
			exit(0);
    		}
    		
	} while (1);
}

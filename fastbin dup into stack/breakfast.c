#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

#define MAX 100

// gcc breakfast.c -o breakfast -fno-stack-protector -Wl,-z,relro,-z,now

struct H {
	void* m[MAX];
	unsigned size[MAX];
};

struct H ptr;

int clear_stdin() {
    while (getchar() != '\n');
    return 1;
}

void menu() {
	puts("---------Select Menú--------");
	puts("1.- Create breakfast");
	puts("2.- Ingredients");
	puts("3.- View");
	puts("4.- Delete");
	puts("5.- Exit");
}


void crea() {
	unsigned pos = 0;
	char c;
	puts("Enter the position of breakfast");
	while ((scanf("%u%c", &pos, &c) != 2 || c != '\n') && clear_stdin());
	if (pos < MAX) {
		puts("Enter the size in kcal.");
		while ((scanf("%u%c", &ptr.size[pos], &c) != 2 || c != '\n') && clear_stdin());
		if (ptr.size[pos] >= 0 && ptr.size[pos] <= 80) {
			ptr.m[pos] = malloc(ptr.size[pos]);
		} else {
			puts("Bad size.");
		}
	} else {
		puts("Bad position");
	}
}

void modify() {
	unsigned i = 0;
	char c;
	puts("Introduce the menu to ingredients");
	while ((scanf("%u%c", &i, &c) != 2 || c != '\n') && clear_stdin());
	if (i < MAX) {
		puts("Enter the ingredients");
		read(0, ptr.m[i], ptr.size[i]);
	} else {
		puts("Bad position");	
	}
}

void ver() {
	unsigned i = 0;
	char c;
	puts("Enter the breakfast to see");
	while ((scanf("%u%c", &i, &c) != 2 || c != '\n') && clear_stdin());
	if (i < MAX) {
		write(1, *((void **) ptr.m[i]), ptr.size[i]);
	} else {
		puts("Bad position");
	}	
}

void libera() {
	unsigned i = 0;
	char c;
	puts("Introduce the menu to delete");
	while ((scanf("%u%c", &i, &c) != 2 || c != '\n') && clear_stdin());
	if (i < MAX) {
		free(ptr.m[i]);
	} else {
		puts("Bad position");
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
			case 5: printf("Have a good day!!\n"); 
			return 0;
    		}
    		
	} while (1);
}

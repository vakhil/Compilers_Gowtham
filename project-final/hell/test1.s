.section .data
	  a :
		.int 0
	  b :
		.int 0
	  temp :
		.int 0
	  t9 :
		.int 0
	  i :
		.int 0
	  t7 :
		.int 0
	  t5 :
		.int 0
	  t3 :
		.int 0
	  t1 :
		.int 0
	  t11 :
		.int 0
	  t12 :
		.int 0
	  t13 :
		.int 0
	  n :
		.int 0
	 newline:
		.ascii "\n" 
.section .text


.globl _start


_start:
	movl $1, %ebx
	movl $1, %eax
	movl $3, %edi
	movl $7, %ecx
	movl $0, %esi
	movl  %ebx , a
	movl  %eax , b
	movl  %esi , temp
	movl  %esi , t9
	movl  %edi , i
	movl  %ecx , t7
	movl  %edi , t5
	movl  %eax , t3
	movl  %ebx , t1
	movl  %ecx , n
Block_1 :

	movl (i) , %ebx
	movl (n) , %eax
	cmpl %eax, %ebx
	jle Block_3
Block_2 :

	jmp Block_4
Block_3 :

	movl  a ,  %ebx
	movl  b ,  %eax
	movl  %ebx ,  %edi
	add %eax ,  %edi
	movl $1, %ecx
	movl  i ,  %esi
	add %ecx ,  %esi
	movl %eax,   a
	movl %edi,   b
	movl %ebx,   temp
	movl %esi,   i
	movl %edi,   t11
	movl %ecx,   t12
	movl %esi,   t13
	jmp Block_1
Block_4 :

	movl b,  %eax
	call  print
	movl $1, %eax
	movl $0, %ebx
	int $0x80 
print:
	movl $0, %edi
	call loop
	mov $4 , %eax
	mov  $1, %ebx
	mov  $newline, %ecx 
	int $0x80 
	ret
loop:
	mov $10, %ecx 
	movl $0, %edx 
	div %ecx
	add $48, %edx 
	pushl %edx 
	add $1, %edi 
	cmp $0, %eax 
	jnz loop 
	jmp true 
	ret
true:
	popl %edx 
	mov %edx, b 
	mov $4 , %eax
	mov  $1, %ebx 
	mov  $b, %ecx 
	mov  $1, %edx
	int $0x80 
	sub $1, %edi 
	cmp $0, %edi 
	jnz true 
	ret

[1, 7, 8, 10, 11, 13, 14, 19, 20]
.section .data
	  a :
		.int 0
	  c :
		.int 0
	  t8 :
		.int 0
	  t9 :
		.int 0
	  t6 :
		.int 0
	  t7 :
		.int 0
	  t5 :
		.int 0
	  t3 :
		.int 0
	  t1 :
		.int 0
	 b:
		.int 0
	 newline:
		.ascii "\n" 
.section .text


.globl _start


_start:
	movl $5, %ebx
	movl  %ebx ,  t1
	movl $10, %eax
	movl  %eax ,  t3
	movl $6, %edi
	movl %ebx,   a
	movl %eax,   c
	movl %edi,   t5
	movl (a) , %ebx
	movl (t5) , %eax
	cmpl %eax, %ebx
	jne Block_2
Block_1 :

	jmp Block_8
Block_2 :

	movl $10, %ebx
	movl %ebx,   t6
	movl (a) , %ebx
	movl (t6) , %eax
	cmpl %eax, %ebx
	jl Block_6
Block_3 :

	jmp Block_4
Block_4 :

	movl $8, %ebx
	movl %ebx,   t7
	movl (c) , %ebx
	movl (t7) , %eax
	cmpl %eax, %ebx
	jg Block_6
Block_5 :

	jmp Block_7
Block_6 :

	movl a,  %eax
	call  print
	movl $1, %ebx
	movl  a ,  %eax
	add %ebx ,  %eax
	movl  %eax ,  t9
	movl %eax,   a
	jmp Block_2
Block_7 :

	movl c,  %eax
	call  print
Block_8 :

Block_8 :

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

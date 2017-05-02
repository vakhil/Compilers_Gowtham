python parser.py
./codegen ./test/kane.txt > hell/test1.s
as --32 ./hell/test1.s -o ./hell/program.o
ld -m elf_i386 ./hell/program.o -o ./hell/program
clear
./hell/program
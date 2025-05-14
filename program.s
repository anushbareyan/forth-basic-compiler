.global _start
_start:
mov $stack_mem + 1024, %rbx

sub $8, %rbx
movq $8, (%rbx)

sub $8, %rbx
movq $5, (%rbx)

# / op
mov (%rbx), %rcx
add $8, %rbx
mov (%rbx), %rax
add $8, %rbx
div %rcx
sub $8, %rbx
mov %rax, (%rbx)

sub $8, %rbx
movq $2, (%rbx)

# + op
mov (%rbx), %rax
add $8, %rbx
mov (%rbx), %rcx
add $8, %rbx
add %rax, %rcx
sub $8, %rbx
mov %rcx, (%rbx)

sub $8, %rbx
movq $5, (%rbx)

# * op
mov (%rbx), %rax
add $8, %rbx
mov (%rbx), %rcx
add $8, %rbx
imul %rcx, %rax
sub $8, %rbx
mov %rax, (%rbx)

# .s op
push %r14
push %r13
mov %rbx, %r14
mov $stack_mem + 1024 - 8, %r13
loop_ss_0_start:
cmp %r14, %r13
jl loop_ss_0_end
mov (%r13), %rax
call print_number
# print space
mov $1, %rax
mov $1, %rdi
lea space(%rip), %rsi
mov $1, %rdx
syscall
sub $8, %r13
jmp loop_ss_0_start
loop_ss_0_end:
pop %r13
pop %r14

# exit syscall
mov $60, %rax
xor %rdi, %rdi
syscall

print_number:
push %rbx
push %rcx
push %rdx
push %rsi
push %rdi
push %rbp
mov %rax, %rbp
test %rbp, %rbp
jnz .non_zero
# zero division bad
mov $output_buffer, %rsi
movb $'0', (%rsi)
mov $1, %rdx
jmp .write
.non_zero:
# convert num to str
lea output_buffer + 19, %rsi
movb $0, (%rsi)
mov %rsi, %rdi
dec %rsi
mov $10, %rcx
.digit_loop:
xor %rdx, %rdx
mov %rbp, %rax
div %rcx
add $'0', %dl
movb %dl, (%rsi)
dec %rsi
mov %rax, %rbp
test %rax, %rax
jnz .digit_loop
# prepare to write
inc %rsi
mov %rdi, %rax
sub %rsi, %rax
mov %rax, %rdx
.write:
# write syscall
mov $1, %rax
mov $1, %rdi
syscall
# restore
pop %rbp
pop %rdi
pop %rsi
pop %rdx
pop %rcx
pop %rbx
ret

.section .data
space: .ascii " "
.section .bss
stack_mem: .space 1024
output_buffer: .space 20
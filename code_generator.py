def generate(tokens):
    output = [
        ".global _start",
        "_start:",
        "mov $stack_mem + 1024, %rbx",
        ""
    ]

    ss_label_count = 0
    
    for token in tokens:
        if isinstance(token, int):
            output.append(f"sub $8, %rbx")
            output.append(f"movq ${token}, (%rbx)")
        elif token == '+': # moves the stack last 2 top vals to rax rcx and sums them then changes address of stack top
            output.extend([
                "# + op",
                "mov (%rbx), %rax",
                "add $8, %rbx",
                "mov (%rbx), %rcx",
                "add $8, %rbx",
                "add %rax, %rcx",
                "sub $8, %rbx",
                "mov %rcx, (%rbx)"
            ])
        elif token == '-':
            output.extend([
                "# - op",
                "mov (%rbx), %rax",
                "add $8, %rbx",
                "mov (%rbx), %rcx",
                "add $8, %rbx",
                "sub %rax, %rcx",
                "sub $8, %rbx",
                "mov %rcx, (%rbx)"
            ])
        elif token == '*':
            output.extend([
                "# * op",
                "mov (%rbx), %rax",
                "add $8, %rbx",
                "mov (%rbx), %rcx",
                "add $8, %rbx",
                "imul %rcx, %rax",
                "sub $8, %rbx",
                "mov %rax, (%rbx)"
            ])
        elif token == '/':
            output.extend([
                "# / op",
                "mov (%rbx), %rcx",
                "add $8, %rbx",
                "mov (%rbx), %rax",
                "add $8, %rbx",
                "div %rcx", # i dont know how to handle signed cases -8/5 
                "sub $8, %rbx",
                "mov %rax, (%rbx)"
            ])
        elif token == '.':
            output.extend([
                  "# . op",
                  "mov (%rbx), %rax",        
                  "add $8, %rbx",            
                  "call print_number",       
                  "# print space",
                  "mov $1, %rax",            
                  "mov $1, %rdi",            
                  "lea space(%rip), %rsi",   
                  "mov $1, %rdx",            
                  "syscall"
            ])
        elif token == '.s':
           
            label_start = f"loop_ss_{ss_label_count}_start"
            label_end = f"loop_ss_{ss_label_count}_end"
            ss_label_count += 1
            
            output.extend([
                "# .s op",
                "push %r14",        
                "push %r13",
                "mov %rbx, %r14",  
                "mov $stack_mem + 1024 - 8, %r13",  
                f"{label_start}:",
                "cmp %r14, %r13",  
                f"jl {label_end}",  
                "mov (%r13), %rax", 
                "call print_number",
                "# print space",
                "mov $1, %rax",
                "mov $1, %rdi",
                "lea space(%rip), %rsi",
                "mov $1, %rdx",
                "syscall",
                "sub $8, %r13",     
                f"jmp {label_start}",
                f"{label_end}:",
                "pop %r13",         
                "pop %r14",
            ])
        elif token == 'dup':
           output.extend([
               "# dup op",
               "mov (%rbx), %rax",  
               "sub $8, %rbx",      
               "mov %rax, (%rbx)"   
           ])

        elif token == 'swap':
            output.extend([
                "# swap op",
                "mov (%rbx), %rax",       
                "mov 8(%rbx), %rcx",      
                "mov %rcx, (%rbx)",       
                "mov %rax, 8(%rbx)"       
            ])
        elif token == 'drop':
            output.extend([
                "# drop op",
                "add $8, %rbx" 
            ])
        output.append("")
    
    output.extend([
        "# exit syscall",
        "mov $60, %rax",
        "xor %rdi, %rdi",
        "syscall",
        "",
        "print_number:",
        "push %rbx",
        "push %rcx",
        "push %rdx",
        "push %rsi",
        "push %rdi",
        "push %rbp",
        "mov %rax, %rbp",
        "test %rbp, %rbp",
        "jnz .non_zero",
        "# zero division bad",
        "mov $output_buffer, %rsi",
        "movb $'0', (%rsi)",
        "mov $1, %rdx",
        "jmp .write",
        ".non_zero:",
        "# convert num to str",
        "lea output_buffer + 19, %rsi",
        "movb $0, (%rsi)",
        "mov %rsi, %rdi",
        "dec %rsi",
        "mov $10, %rcx",
        ".digit_loop:", # for num to str conversion digit by digit
        "xor %rdx, %rdx",
        "mov %rbp, %rax",
        "div %rcx",# rcx is 10 so divide to get last digit
        "add $'0', %dl",# convert by adding '0'
        "movb %dl, (%rsi)",
        "dec %rsi",
        "mov %rax, %rbp",
        "test %rax, %rax", # check if rax is 0 =>no digit left
        "jnz .digit_loop",
        "# prepare to write",
        "inc %rsi",
        "mov %rdi, %rax",
        "sub %rsi, %rax",
        "mov %rax, %rdx",
        ".write:",
        "# write syscall",
        "mov $1, %rax",
        "mov $1, %rdi",
        "syscall",
        "# restore",
        "pop %rbp",
        "pop %rdi",
        "pop %rsi",
        "pop %rdx",
        "pop %rcx",
        "pop %rbx",
        "ret",
        "",
        ".section .data",
        "space: .ascii \" \"",
        ".section .bss",
        "stack_mem: .space 1024",
        "output_buffer: .space 20"
    ])
    
    return '\n'.join(output)


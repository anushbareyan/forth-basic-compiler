import sys
import os
from scanner import scan
from code_generator import generate

def compile_forth(input_file):
    try:
        tokens = scan(input_file)
        if not tokens:
            print("invalid tokens :( ")
            return False
        asm = generate(tokens)
        with open("program.s", "w") as f:
            f.write(asm)
        if os.system("as program.s -o program.o") != 0:
            print("assembly failed :(")
            return False
        if os.system("ld program.o -o program") != 0:
            print("linking failed :(")
            return False
        os.chmod("program", 0o755)
        return True
    except Exception as e:
        print(f"error: {e}")
        return False
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("you should write python compiler.py input_file.fs")
        sys.exit(1)
    if compile_forth(sys.argv[1]):
        print("compilation successful :)  run with ./program")
    else:
        sys.exit(1)

import os
PATH = r'Enter file path here'

cTemplate = (
"""#include <stdio.h>

int main(){
    printf("Hello World!");
    return 0;
}""")

os.chdir(PATH)
print("Enter run mode\n- Create c file (0)\n- Compile c file (1)\n- Run compiled exe (2)")
i = input(":")

llvm = r"C:\Program Files\LLVM\bin\clang.exe"
if i == '2':
    name = input("\nEnter name of .exe file: ")
    path = os.path.join(PATH, name + ".exe")
elif i == '0' or i == '1':
    name = input("\nEnter name of .c file: ")
    path = os.path.join(PATH, name + ".c")

if i == '0':
    with open(path, 'w') as file:
        file.write(cTemplate)
    print(f"File created as: {path}")
elif i == '1':
    os.system(f'""{llvm}" "{path}""')
elif i == '2':
    os.system("\"" + path + "\"")
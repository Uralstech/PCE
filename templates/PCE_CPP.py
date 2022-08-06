import os
PATH = r''

cppTemplate = (
"""#include <iostream>

int main(){
    std::cout << "Hello World!" << std::endl;
    return 0;
}""")

os.chdir(PATH)
print("AVAILABLE TASKS:\n- Create C++ file (0)\n- Compile C++ file (1)\n- Run compiled executable (2)")
i = input("TASK TO EXECUTE: ")

llvm = r"C:\Program Files\LLVM\bin\clang.exe"
if i == '2':
    name = input("\nName of .exe file: ")
    path = os.path.join(PATH, name + ".exe")
elif i == '0' or i == '1':
    name = input("\nName of .cpp file: ")
    path = os.path.join(PATH, name + ".cpp")

if i == '0':
    with open(path, 'w') as file:
        file.write(cppTemplate)
    print(f"File created as: {path}")
elif i == '1':
    os.system(f'""{llvm}" "{path}""')
elif i == '2':
    os.system("\"" + path + "\"")
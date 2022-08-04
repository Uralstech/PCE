import os
PATH = 'Enter file path here'

cSharpTemplate = (
"""using System;

namespace Application{
    class Program{
        static void Main(string[] args){
            Console.WriteLine("Hello World!");
        }
    }
}""")

os.chdir(PATH)
print("Enter run mode\n- Create csproj (0)\n- Compile csproj (1)\n- Run compiled exe (2)")
i = input(":")

if i == '0':
    os.system("dotnet new console")
    with open(os.path.join(PATH, "Program.cs"), 'w') as file:
        file.write(cSharpTemplate)
elif i == '1':
    os.system("dotnet run \"" + PATH + "\"")
elif i == '2':
    name = PATH.split('\\')[-1]
    os.system("\"" + os.path.join(PATH, "bin/debug/net6.0/" + name + ".exe\""))
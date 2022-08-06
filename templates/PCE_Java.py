import os
PATH = r''

javaTemplate = (
"""class HelloWorld {
    public static void main(String[] args){
        System.out.println("Hello World!");
    }
}""")

os.chdir(PATH)
print("AVAILABLE TASKS:\n- Create Java file (0)\n- Compile Java file (1)\n- Run compiled Class file (2)\n- Convert Class file[s] to Jar file (3)\n- Run Jar file (4)")
i = input("TASK TO EXECUTE: ")

main = r"C:\Program Files\Java"
version = ""
for j in os.listdir(main):
    if "jdk" in j: version = j; break

javadk = "C:\\Program Files\\Java\\" + version + "\\bin\\javac.exe"
jar = "C:\\Program Files\\Java\\" + version + "\\bin\\jar.exe"
java = "C:\\Program Files\\Java\\" + version + "\\bin\\java.exe"

name = ""
path = ""

mainClass = ""
jarName = ""
m_version = ""
m_creator = ""
classPaths = ""
if i == '3':
    print(f"NOTE: ALL CLASS FILES SHOULD BE IN {PATH}")
    jarName = input("Name of Jar: ") + ".jar"
    m_version = input("Manifest version: ")
    m_creator = input("Name of creator: ")
    mainClass = input("Name of main Class file: ")
    classPaths = input("Other class files (format: e1.class e2.class): ")
elif i == '4':
    name = input("\nName of .jar file: ")
    path = os.path.join(PATH, name + ".jar")
elif i == '2':
    name = input("\nName of .class file: ")
    path = name
elif i == '0' or i == '1':
    name = input("\nName of .java file: ")
    path = os.path.join(PATH, name + ".java")

if i == '0':
    with open(path, 'w') as file:
        file.write(javaTemplate)
    print(f"File created as: {path}")
elif i == '1':
    os.system(f'""{javadk}" "{path}""')
elif i == '2':
    os.system(f'""{java}" "{path}""')
elif i == '3':
    manifest = os.path.join(PATH, "manifest.txt")
    with open(manifest, 'w') as file:
        file.write("Manifest-Version: " + m_version)
        file.write("\nCreated-By: " + m_creator)
        file.write("\nMain-Class: " + mainClass)
        file.write("\n\n")
    print(f"Manifest created as {manifest}")

    mainClass += ".class"
    command = f'""{jar}" cfm "{jarName}" "{manifest}" "{mainClass}"'
    if classPaths != "": command +=  f' "{classPaths}""'
    else: command += '"'
    os.system(command)
elif i == '4':
    os.system(f'""{java}" -jar "{path}""')
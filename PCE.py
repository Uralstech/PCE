from ShrtCde.IO import *
from rich.console import Console
from rich.theme import Theme
import os

os.system("title " + "Python Command-line Editor V1.2.3")

default = Theme({"normal" : "bold green", "error" : "bold underline red", "command" : "green", "file" : "yellow"})
theme01 = Theme({"normal" : "bold blue", "error" : "bold underline magenta", "command" : "blue", "file" : "green"})
theme02 = Theme({"normal" : "bold yellow", "error" : "bold underline red", "command" : "yellow", "file" : "cyan"})
theme03 = Theme({"normal" : "white", "error" : "white", "command" : "white", "file" : "white"})

current = 0
pyfile = True # NOTE: Set this to False when building EXE

here = ""
if pyfile:
    here = os.path.abspath(os.path.dirname(__file__)) + "\\PCESettings.txt"
else:
    here = os.path.abspath(os.path.dirname("PCE.exe")) + "\\PCESettings.txt"

try: current = int(readf(here, 'r'))
except:
    current = 0
    writef(here, ['0'])

console = None
if current == 1:
    console = Console(theme=theme01)
elif current == 2:
    console = Console(theme=theme02)
elif current == 3:
    console = Console(theme=theme03)
else:
    console = Console(theme=default)

console.print(r"[normal]>>Type in 'help' to get started[/]")

lines = []
path = ""

permissionFile = "permissionfile.pcepermission"
helpInfo =(
r"""[normal]>>COMMANDS[/]
[normal]>>  GENERAL[/]
[command]>>    theme (index)[/]
[normal]>>      Changes console theme according to index (available: 0, 1, 2, 3 | default: 0)[/]
[command]>>    clear[/]
[normal]>>      Clears console[/]
[command]>>    quit[/]
[normal]>>      Quits program[/]
[normal]>>  FILE[/]
[command]>>    open (path to file)[/]
[normal]>>      Opens/creates file at given path[/]
[command]>>    delete (path to file)[/]
[normal]>>      Deletes file at given path[/]
[command]>>    makedir (path to directory)[/]
[normal]>>      Creates new directory at path[/]
[command]>>    deletedir (path to directory)[/]
[normal]>>      Deletes directory at path[/]
[command]>>    showdir (path to directory)[/]
[normal]>>      Show all files in directory at path[/]
[normal]>>    ONLY USE BELOW IF A FILE IS OPEN[/]
[command]>>      i (index) (line to write)[/]
[normal]>>        Writes given data to file at index (for appending data, set index to -1)[/]
[command]>>      r (index) (line to replace with)[/]
[normal]>>        Removes/replaces data at index (for removing data, don't add anything after index)[/]
[command]>>      rb (from index) (to index)[/]
[normal]>>        Removes all data from index one to index two[/]
[command]>>      close[/]
[normal]>>        Closes current file[/]
[command]>>      show[/]
[normal]>>        Shows contents of current file[/]
[command]>>      showraw[/]
[normal]>>        Shows raw contents of current file, without indexing[/]
[command]>>      save[/]
[normal]>>        Saves current file[/]
[command]>>      saveas (path to file)[/]
[normal]>>        Saves content of current file to file at path[/]
[command]>>      run[/]
[normal]>>        (Only for Python files) Runs current file[/]
[bold blue]>>  NOTE: COLORS AND FONTS WILL VARY ACROSS DIFFERENT COMMAND-LINE INTERPRETERS[/]""")

def checkInput(cmd: str):
    global console
    global lines
    global path

    def loadLines():
        global lines
        if findf(path):
            lines = readf(path, 'rls')
            for i in range(len(lines)):
                if lines[i][-1] == '\n':
                    lines[i] = lines[i][:-1]
    
    def formatText(input):
        line = ""
        index = ""
        for i in range(len(input)):
            if input[i] != " ":
                index += input[i]
            else:
                line = input[i+1:]
                break
        
        formattedLine = ""
        index2 = 0
        for i in range(len(line)):
            if index2 + 1 < len(line):
                newChar = line[index2] + line[index2+1]
                if newChar == r"$n":
                    formattedLine += "\n"
                    index2 += 1
                elif newChar == r"$t":
                    formattedLine += "\t"
                    index2 += 1
                else:
                    formattedLine += line[index2]
            else:
                formattedLine += line[-1]
                break
            index2 += 1
        return formattedLine, index
    
    if cmd == r"help":
        console.print(helpInfo)
    elif cmd == r"clear":
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')
    elif cmd == r"quit":
        return 1
    elif cmd.startswith(r"theme "):
        if cmd[6] == '0':
            console = Console(theme=default)
            writef(here, ['0'])
            return
        elif cmd[6] == '1':
            console = Console(theme=theme01)
            writef(here, ['1'])
            return
        elif cmd[6] == '2':
            console = Console(theme=theme02)
            writef(here, ['2'])
            return
        elif cmd[6] == '3':
            console = Console(theme=theme03)
            writef(here, ['3'])
            return
        
        console.print("[error]>>INVALID COMMAND SYNTAX[/]")
    elif cmd.startswith(r"makedir "):
        path2 = cmd[8:]
        if os.path.isdir(path2):
            path2 = ""
            console.print("[error]>>DIRECTORY ALREADY EXISTS[/]")
            return
    
        os.mkdir(path2)
        writef(os.path.join(path2, permissionFile), ["The existance of this file tells PCE (Python Command-line Editor) this directory was created by it.", "If this did not exist, PCE won't be allowed to delete this directory."], 'x')
        console.print("[normal]>>Directory created[/]")
    elif cmd.startswith(r"deletedir "):
        path2 = cmd[10:]
        if not os.path.isdir(path2):
            path2 = ""
            console.print("[error]>>DIRECTORY DOES NOT EXIST[/]")
            return
        if not findf(os.path.join(path2, permissionFile)):
            path2 = ""
            console.print("[error]>>PCE IS ONLY ALLOWED TO DELETE DIRECTORIES MADE BY PCE[/]")
            return
    
        filesAtDir = []
        for i in os.scandir(path2):
            filesAtDir.append(i.name)
        if len(filesAtDir) > 1 or filesAtDir[0] != permissionFile:
            path2 = ""
            console.print(f"[error]>>FILES OTHER THAN {permissionFile} WERE FOUND IN DIRECTORY. DELETE THESE FILES BEFORE CONTINUING[/]")
            return
    
        os.remove(os.path.join(path2, permissionFile))
        os.rmdir(path2)
        console.print("[normal]>>Directory deleted[/]")
    elif cmd.startswith(r"showdir "):
        path2 = cmd[8:]
        if not os.path.isdir(path2):
            path2 = ""
            console.print("[error]>>DIRECTORY DOES NOT EXIST[/]")
            return
        
        console.print("[file][bold]>>FILE NAME                     FILE TYPE[/][/]")
        for i in os.listdir(path2):
            spaces = " "
            splitPath = list(os.path.splitext(i))
            length = 29 - len(splitPath[0])
            if os.path.isdir(os.path.join(path2, i)):
                splitPath[0] = i
                splitPath[1] = "folder"
            elif splitPath[1] == "":
                splitPath[1] = "unknown file"
            else:
                splitPath[1] = splitPath[1][1:] + " file"

            if length > 0:
                for _ in range(length):
                    spaces += " "

            console.print(f"[file]>>{splitPath[0]}{spaces}{splitPath[1]}[/]")
    elif path == "":
        if cmd.startswith(r"open "):
            path = cmd[5:]
            if not os.path.isdir(os.path.split(path)[0]):
                path = ""
                console.print("[error]>>INVALID PATH[/]")
                return

            if not findf(path):
                option = console.input("[command]>>File was not found. Create? y/n [/]")
                if option == "y":
                    writef(path, [""], 'x')
                    console.print("[normal]>>File created[/]")
                else:
                    path = ""
                    return

            loadLines()
        elif cmd.startswith(r"delete "):
            path = cmd[7:]
            if not findf(path):
                path = ""
                console.print("[error]>>FILE DOES NOT EXIST[/]")
                return

            option = console.input("[command]>>File will be permanently deleted. Continue? y/n [/]")
            if option == "y":
                os.remove(path)
                console.print("[normal]>>File deleted[/]")
                path = ""
            else:
                path = ""
        else:
            console.print("[error]INVALID COMMAND[/]")
    elif path != "":
        if cmd.startswith(r"i "):
            formattedLine, index = formatText(cmd[2:])

            try:
                index = int(index)
            except:
                console.print("[error]>>INVALID COMMAND SYNTAX[/]")
                return

            if index >= len(lines) or index < 0:
                lines.append(formattedLine)
            else:
                lines.insert(index, formattedLine)
        elif cmd.startswith(r"r "):
            formattedLine, index = formatText(cmd[2:])

            try:
                index = int(index)
            except:
                console.print("[error]>>INVALID COMMAND SYNTAX[/]")
                return

            if index >= len(lines) or index < 0:
                console.print("[error]>>INDEX OUT OF RANGE[/]")
                return
            else:
                newLines = []
                for i in range(len(lines)):
                    if i != index:
                        newLines.append(lines[i])
                    elif formattedLine != "":
                        newLines.append(formattedLine)
                lines = newLines
        elif cmd.startswith(r"rb "):
            _to, _from = formatText(cmd[3:])

            try:
                _from = int(_from)
                _to = int(_to)
            except:
                console.print("[error]>>INVALID COMMAND SYNTAX[/]")
                return

            if _to >= len(lines) or _from < 0:
                console.print("[error]>>INDEX OUT OF RANGE[/]")
                return
            elif _to < _from:
                console.print("[error]>>INDEX ONE CANNOT BE LESS THAN OR EQUAL TO INDEX TWO[/]")
                return
            else:
                newLines = []
                for i in range(len(lines)):
                    if i < _from or i > _to:
                        newLines.append(lines[i])
                lines = newLines
        elif cmd == r"close":
            writef(path, lines, 'w')
            lines = None
            path = ""
            console.print("[normal]>>File closed[/]")
        elif cmd == r"save":
            writef(path, lines, 'w')
            loadLines()
            console.print("[normal]>>File saved[/]")
        elif cmd.startswith(r"saveas "):
            writef(cmd[7:], lines)
            loadLines()
            console.print("[normal]>>File saved[/]")
        elif cmd == r"show":
            if len(lines) > 0:
                for i in range(len(lines)):
                    console.print("[file]>> (" + str(i) + ")" + lines[i] + "[/]")
            else:
                console.print("[file]>> File is empty[/]")
        elif cmd == r"showraw":
            if len(lines) > 0:
                for i in range(len(lines)):
                    console.print("[file]" + lines[i] + "[/]")
            else:
                console.print("[file]>> File is empty[/]")
        elif cmd.startswith(r"run"):
            alt = '"' + path + '"'

            if os.path.splitext(path)[1] == ".py":
                console.print(f"[command]>>START OF {path}[/]")
                os.system("python " + alt)
                console.print(f"\n[command]>>END OF {path}[/]")
            else:
                console.print("[error]>>RUN COMMAND ONLY SUPPORTS PYTHON FILES[/]")
        else:
            console.print("[error]>>INVALID COMMAND[/]")
    else:
        console.print("[error]>>INVALID COMMAND[/]")

while True:
    try:
        i = console.input("[command]>>[/]")
        if i != "":
            output = checkInput(i)
            if output == 1:
                break
    except:
        pass
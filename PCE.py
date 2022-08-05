from ShrtCde.IO import *
from rich.console import Console
from rich.theme import Theme
from rich.markup import escape
import os

os.system("title Python Command-line Editor V1.4.1")

default = Theme({"normal" : "bold green", "error" : "bold underline red", "command" : "green", "file" : "yellow"})
theme01 = Theme({"normal" : "bold blue", "error" : "bold underline magenta", "command" : "blue", "file" : "green"})
theme02 = Theme({"normal" : "bold yellow", "error" : "bold underline red", "command" : "yellow", "file" : "cyan"})
theme03 = Theme({"normal" : "white", "error" : "white", "command" : "white", "file" : "white"})

current = 0

here = ""
PCESettings = ""
here = os.getcwd()
PCESettings = here + "\\PCESettings.txt"

try: current = int(readf(PCESettings, 'r'))
except: current = 0; writef(PCESettings, ['0'])

console = None
if current == 1: console = Console(theme=theme01)
elif current == 2: console = Console(theme=theme02)
elif current == 3: console = Console(theme=theme03)
else: console = Console(theme=default)

console.print(r"[normal]>>Type in 'help' to get started[/]")

lines = []
copied = []
path = ""

permissionFile = "permissionfile.pcepermission"
helpInfo = (
r"""[normal]>>COMMANDS[/]
[normal]>>  GENERAL[/]
[command]>>    :(Command-line code)[/]
[normal]>>      Runs given Command-line code[/]
[command]>>    ::(Python code)[/]
[normal]>>      Runs given Python code[/]
[command]>>    cd (mode) (path to directory)[/]
[normal]>>      Changes current working directory (cwd) to given directory (leave empty to view cwd)[/]
[command]>>    theme (index)[/]
[normal]>>      Changes console theme according to index (available: 0, 1, 2, 3 | default: 0)[/]
[command]>>    clear[/]
[normal]>>      Clears console[/]
[command]>>    quit[/]
[normal]>>      Quits program[/]
[normal]>>  FILE[/]
[command]>>    open (mode) (path to file)[/]
[normal]>>      Opens/creates file at given path[/]
[command]>>    delete (mode) (path to file)[/]
[normal]>>      Deletes file at given path[/]
[command]>>    run (mode) (path to file)[/]
[normal]>>      (Only for Python files) Runs file at path (leave empty to run current file)[/]
[command]>>    makedir (mode) (path to directory)[/]
[normal]>>      Creates new directory at path[/]
[command]>>    deletedir (mode) (path to directory)[/]
[normal]>>      Deletes directory at path[/]
[command]>>    showdir (mode) (path to directory)[/]
[normal]>>      Show all files in directory at path[/]
[command]>>    template (mode) (path to directory)[/]
[normal]>>      Make a new template file at given path (use command for more details)/]
[normal]>>    ONLY USE BELOW IF A FILE IS OPEN[/]
[command]>>      i (index) (line to write)[/]
[normal]>>        Writes given data to file at index (for appending data, set index to -1)[/]
[command]>>      c (from index) (to index)[/]
[normal]>>        Copies all data from index one to index two[/]
[command]>>      p (index)[/]
[normal]>>        Pastes all copied data to index (for appending data, set index to -1)[/]
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
[command]>>      saveas (mode) (path to file)[/]
[normal]>>        Saves content of current file to file at path[/]
[normal]>>  MODES:[/]
[command]>>    c[/]
[normal]>>      Points to any file/directory in CWD[/]
[command]>>    r[/]
[normal]>>      Points to any file/directory in the directory that contains the CWD[/]
[command]>>    f[/]
[normal]>>      Points to any file/directory in SYSTEM (needs full path)[/]
[bold blue]>>  NOTE: TEXT FORMATTING IS AVAILABLE WITH $n (new-line) and $t (tab-space)
[bold blue]>>  NOTE: COLORS AND FONTS WILL VARY ACROSS DIFFERENT COMMAND-LINE INTERPRETERS[/]""")

def checkInput(cmd: str):
    global console
    global copied
    global lines
    global path

    def loadLines():
        global lines
        if findf(path):
            lines = readf(path, 'rls')
            def func(n):
                if n[-1] == '\n': n = n[:-1]
                return n
            lines = list(map(func, lines))
    
    def formatText(iinput):
        main = tuple(iinput.split())
        index = ""
        line = ""
        if len(main) > 1: index, line = main[0], main[1]
        else: index = main[0]

        line = line.replace(r"$n", "\n")
        line = line.replace(r"$t", "\t")
        return line, index

    def checkMode(input):
        if len(input) == 0:console.print("[error]>>INVALID COMMMAND SYNTAX[/]"); return -1
        elif input[0] == 'c': return os.path.join(os.getcwd(), input[2:])
        elif input[0] == 'r': temp = "\\".join(os.getcwd().split('\\')[:-1]); return os.path.join(temp, input[2:])
        elif input[0] == 'f': return input[2:]
        else: console.print("[error]>>INVALID COMMMAND SYNTAX[/]"); return -1
    
    def dirSize(dirpath):
        total = 0
        try:
            with os.scandir(dirpath) as scan:
                for entry in scan:
                    if entry.is_file(): total += entry.stat().st_size
                    elif entry.is_dir(): total += dirSize(entry.path)
        except: return "e"
        return total

    def checkPath(currentPath, dir=False):
        if not dir and not findf(currentPath): console.print("[error]>>INVALID PATH: FILE DOES NOT EXIST[/]"); return 0
        elif dir and not os.path.isdir(currentPath): console.print("[error]>>INVALID PATH: DIRECTORY DOES NOT EXIST[/]"); return 0
        return 1

    if cmd.startswith(r"::"):
        console.print("[command]>>START OF [CUSTOM PYTHON CODE][/]")
        eval(cmd[2:])
        console.print("[command]>>END OF [CUSTOM PYTHON CODE][/]")
    elif cmd.startswith(r":"):
        console.print("[command]>>START OF [COMMAND][/]")
        os.system(cmd[1:])
        console.print("[command]>>END OF [COMMAND][/]")
    elif cmd.startswith(r"cd"):
        if cmd == r"cd":
            console.print("[normal]>>" + os.getcwd() + "[/]")
            return
            
        path2 = checkMode(cmd[3:])
        if path2 == -1: return
        if checkPath(path2, True) == 0: return
        
        os.chdir(path2)
    elif cmd == r"help":
        console.print(helpInfo)
    elif cmd == r"clear":
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')
    elif cmd == r"quit":
        return 1
    elif cmd.startswith(r"theme "):
        if cmd[6] == '0':
            console = Console(theme=default)
            writef(PCESettings, ['0'])
        elif cmd[6] == '1':
            console = Console(theme=theme01)
            writef(PCESettings, ['1'])
        elif cmd[6] == '2':
            console = Console(theme=theme02)
            writef(PCESettings, ['2'])
        elif cmd[6] == '3':
            console = Console(theme=theme03)
            writef(PCESettings, ['3'])
        else: console.print("[error]>>INVALID COMMAND SYNTAX[/]")
    elif cmd.startswith(r"makedir"):
        path2 = checkMode(cmd[8:])
        if path2 == -1: return

        if os.path.isdir(path2): console.print("[error]>>DIRECTORY ALREADY EXISTS[/]"); return

        os.mkdir(path2)
        writef(os.path.join(path2, permissionFile), ("This file grants PCE (Python Command-line Editor) permission to delete this directory when empty.", "If you do not want PCE to have this permission, please delete this file."), 'x')
        console.print("[normal]>>Directory created[/]")
    elif cmd.startswith(r"deletedir"):
        path2 = checkMode(cmd[10:])
        if path2 == -1: return
            
        if checkPath(path2, True) == 0: return
        if not findf(os.path.join(path2, permissionFile)):
            console.print("[error]>>PCE IS ONLY ALLOWED TO DELETE DIRECTORIES MADE BY PCE[/]")
            return
    
        filesAtDir = []
        for i in os.scandir(path2):
            filesAtDir.append(i.name)
        if len(filesAtDir) > 1 or filesAtDir[0] != permissionFile:
            console.print(f"[error]>>FILES OTHER THAN {permissionFile} WERE FOUND IN DIRECTORY. DELETE THESE FILES BEFORE CONTINUING[/]")
            return
    
        os.remove(os.path.join(path2, permissionFile))
        os.rmdir(path2)
        console.print("[normal]>>Directory deleted[/]")
    elif cmd.startswith(r"showdir"):
        path2 = checkMode(cmd[8:])
        if path2 == -1: return

        if checkPath(path2, True) == 0: return
        
        console.print("[file][bold]>>WARNING: THIS CODE MAY BE ERRONEOUS BECAUSE OF INACCESSIBLE FILES[/]")
        console.print("[file][bold]>>NAME\t\t\t\tTYPE\t\t\t\tSIZE[/][/]")
        with os.scandir(path2) as scan:
            for i in scan:
                spaces = " "
                mainPath = os.path.join(path2, i.name)
                splitPath = list(os.path.splitext(i.name))
                length = 29 - len(splitPath[0])
                if os.path.isdir(mainPath): splitPath[0] = i.name; splitPath[1] = "folder"
                elif splitPath[1] == "": splitPath[1] = "unknown file"
                else: splitPath[1] = splitPath[1][1:] + " file"

                if length > 0: spaces += " " * length

                spaces2 = ""
                length2 = 32 - len(splitPath[1])
                if length2 > 0: spaces2 += " " * length2

                size = ""
                try:
                    if findf(mainPath): size = os.path.getsize(mainPath)
                    elif os.path.isdir(mainPath): size = dirSize(mainPath)
                except: pass

                if size == "" or size == "e": size = "unknown"
                elif size >= 1024**3: size = (f"{size/(1024**3):.2f}") + " Gb"
                elif size >= 1024**2: size = (f"{size/(1024**2):.2f}") + " Mb"
                elif size >= 1024: size = (f"{size/1024:.2f}") + " Kb"
                else: size = (f"{size:.2f}") + " Bytes"

                console.print(f"[file]>>{splitPath[0]}{spaces}{splitPath[1]}{spaces2}{size}[/]")
    elif cmd.startswith(r"run"):
        alt = ""
        cpath = ""

        if len(cmd) > 3:
            cpath = checkMode(cmd[4:])
            if cpath == -1: return
            alt = '"' + cpath + '"'
        else:
            alt = '"' + path + '"'
            cpath = str(path)
            
        if checkPath(cpath) == 0: return

        if os.path.splitext(cpath)[1] == ".py":
            console.print(f"[command]>>START OF {cpath}[/]")
            os.system("python " + alt)
            console.print(f"\n[command]>>END OF {cpath}[/]")
        else: console.print("[error]>>RUN COMMAND ONLY SUPPORTS PYTHON FILES[/]")
    elif path == "":
        if cmd.startswith(r"open"):
            path = checkMode(cmd[5:])
            if path == -1: path = ""; return

            if checkPath(os.path.split(path)[0], True) == 0: path = ""; return

            if not findf(path):
                option = console.input("[command]>>File was not found. Create? y/n [/]")
                if option == "y":
                    writef(path, (""), 'x')
                    console.print("[normal]>>File created[/]")
                else: path = ""; return

            loadLines()
        elif cmd.startswith(r"delete"):
            path2 = checkMode(cmd[7:])
            if path2 == -1: return
            
            if checkPath(path2) == 0: return

            option = console.input("[command]>>File will be permanently deleted. Continue? y/n [/]")
            if option == "y":
                os.remove(path2)
                console.print("[normal]>>File deleted[/]")
        elif cmd.startswith(r"template"):
            path2 = checkMode(cmd[9:])
            if path2 == -1: return

            if checkPath(path2, True) == 0: return

            templates = (
            "[normal]>>Templates allow PCE to work with/debug/run projects from other languages"
            + "\n>>AVAILABLE TEMPLATES:"
            + "\n>>  C file (index: 0, requires: clang)"
            + "\n>>  C++ file (index: 1, requires: clang)"
            + "\n>>  C# project (index: 2, requires: .NET SDK)"
            + "\n>>  Java file (index 3, requires: Java development kit, Java)[/]")

            console.print(templates)
            i = console.input("[command]>>Enter the index of the template: (-1 to escape) ")

            temp = ""
            if i == '0': temp = "PCE_C.py"
            elif i == '1': temp = "PCE_CPP.py"
            elif i == '2': temp = "PCE_CSharp.py"
            elif i == '3': temp = "PCE_Java.py"
            elif i == '-1': return
            else: console.print("[error]>>INVALID COMMAND SYNTAX"); return
            
            def func(n):
                if n[-1] == '\n': n = n[:-1]
                return n

            tempInfo = tuple(readf(os.path.join(here, str.join("", ("templates/", temp))), 'rls'))
            tempInfo = list(map(func, tempInfo))
            if path2[-1] == "\\": path2 = path2[:-1]
            tempInfo[1] = "PATH = r\"" + path2 + "\""

            writef(os.path.join(path2, temp), tempInfo)
            console.print(f"[normal]>>Template created. To use it, open {temp} in {path2}  and type in the command \'run\'")
        else: console.print("[error]INVALID COMMAND[/]")
    elif path != "":
        if cmd.startswith(r"i "):
            formattedLine, index = formatText(cmd[2:])

            try: index = int(index)
            except: console.print("[error]>>INVALID COMMAND SYNTAX[/]"); return

            if index >= len(lines) or index < 0: lines.append(formattedLine)
            else: lines.insert(index, formattedLine)
        elif cmd.startswith(r"r "):
            formattedLine, index = formatText(cmd[2:])

            try: index = int(index)
            except: console.print("[error]>>INVALID COMMAND SYNTAX[/]"); return

            if index >= len(lines) or index < 0:
                console.print("[error]>>INDEX OUT OF RANGE[/]")
                return
            else:
                if formattedLine == "": del lines[index]
                else: lines[index] = formattedLine
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
            elif _to <= _from:
                console.print("[error]>>INDEX ONE CANNOT BE LESS THAN OR EQUAL TO INDEX TWO[/]")
                return
            else: del lines[_from:_to+1]
        elif cmd.startswith(r"c "):
            _to, _from = formatText(cmd[2:])

            try:
                _from = int(_from)
                _to = int(_to)
            except:
                console.print("[error]>>INVALID COMMAND SYNTAX[/]")
                return

            if _to >= len(lines) or _from < 0:
                console.print("[error]>>INDEX OUT OF RANGE[/]")
                return
            if _to < _from:
                console.print("[error]>>INDEX ONE CANNOT BE LESS THAN INDEX TWO[/]")
                return

            copied = tuple(lines[_from:_to+1])
        elif cmd.startswith(r"p "):
            _from, _to = formatText(cmd[2:])

            try:
                _to = int(_to)
            except:
                console.print("[error]>>INVALID COMMAND SYNTAX[/]")
                return

            if copied == []:
                console.print("[error]>>NOTHING HAS BEEN COPIED FOR PASTING[/]")
                return

            if _to >= len(lines) or _to < 0: lines.extend(copied)
            else:
                lines = [*lines[:_to], *copied, *lines[_to:]]
                print(lines)
        elif cmd == r"close":
            lines = None
            path = ""
            console.print("[normal]>>File closed[/]")
        elif cmd == r"save":
            writef(path, tuple(lines), 'w')
            loadLines()
            console.print("[normal]>>File saved[/]")
        elif cmd.startswith(r"saveas "):
            path2 = checkMode(cmd[7:])
            if path2 == -1: return

            writef(path2, tuple(lines), 'w')
            loadLines()
            console.print(f"[normal]>>File saved as: {path2}[/]")
        elif cmd == r"show":
            if len(lines) > 0:
                space = len(str(len(lines)-1))
                for i in range(len(lines)):
                    num = str(i)
                    if space - len(num) > 0: num = str.join("", (num, ' ' * (space - len(num))))
                    temp = lines[i].replace("\t", "    ")
                    console.print(f"[file]{escape(num)}>>{escape(temp)}[/]")
            else: console.print("[file]>>File is empty[/]")
        elif cmd == r"showraw":
            if len(lines) > 0: console.print(str.join("", ("[file]", '\n'.join(lines))))
            else: console.print("[file]>>File is empty[/]")
        else: console.print("[error]>>INVALID COMMAND[/]")
    else: console.print("[error]>>INVALID COMMAND[/]")

while True:
    try:
        i = console.input("[command]>>[/]")
        if i != "":
            output = checkInput(i)
            if output == 1: break
    except: pass

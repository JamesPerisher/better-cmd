import os
import subprocess
from colorama import *
import asyncio
from code import InteractiveConsole
import sys
import ctypes
init()


class executer:
    def __init__(self, name, desc, col):
        self.name = name
        self.description = desc
        self.col = col
        self.isCurrent = False

    def get(self, command):
        return "Default response to: %s\n"%command

    def get_linestat(self):
        return "Enter command:~$ "

    def getSelf(self):
        return self
    def eventOn(self):
        pass
    def eventOff(self):
        pass

class CMD(executer):
    def __init__(self, perms):
        super().__init__("CMD", "Runs and returns the results of CMD commands", Fore.BLUE)

        if perms != "Admin":
            os.chdir("C:\\Users\\%s" %os.getlogin())
        else:
            os.chdir("C:\\WINDOWS\\system32")
        self.dir = os.getcwd()

    def get_linestat(self):
        return "%s> " %self.dir

    def decoder(self, bytein):
        out = str(bytein).replace("\\r", "").replace("\\n", "\n").replace("\\\'", "\'").replace("\\\\", "\\")   #fixes basic \n \r
        out = out.replace("\\xb3", "│").replace("\\xc3", "├").replace("\\xc0", "└").replace("\\xc4", "─")   #fixes byte error with .decode()

        return out[2:-1]

    def get(self, command):
        if command == "":
            return
        if command[0:3].lower() == "cd ":
            if command[3:7] == "home":
                os.chdir("C:\\Users\\%s" %os.getlogin())
                self.dir = os.getcwd()
                command = "cd %s" %command[8::]
            try:
                os.chdir(command[3::].replace("\"", ""))
                self.dir = os.getcwd()
                return ""
            except FileNotFoundError:
                print(Fore.YELLOW+Style.BRIGHT + "The system cannot find the path specified.\n")
                return

        p = subprocess.Popen(["call"]+command.split(" "), stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, shell=True)

        while p.poll() is None:
            a = p.stdout.readline()
            a = self.decoder(a)
            print(a, end="")
        print()

class MinecrftClient(executer):
    def __init__(self, perms):
        super().__init__("MinecrftClient", "Minecrft client process from console", Fore.YELLOW)

        self.dir = os.getcwd()

    def get_linestat(self):
        return "%s> " %self.dir

    def decoder(self, bytein):
        out = str(bytein).replace("\\r", "").replace("\\n", "\n").replace("\\\'", "\'").replace("\\\\", "\\")   #fixes basic \n \r
        out = out.replace("\\xb3", "│").replace("\\xc3", "├").replace("\\xc0", "└").replace("\\xc4", "─")   #fixes byte error with .decode()

        return out[2:-1]

    def get(self, command):
        if command == "":
            return
        if command[0:3].lower() == "cd ":
            if command[3:7] == "home":
                os.chdir("C:\\Users\\%s" %os.getlogin())
                self.dir = os.getcwd()
                command = "cd %s" %command[8::]
            try:
                os.chdir(command[3::].replace("\"", ""))
                self.dir = os.getcwd()
                return ""
            except FileNotFoundError:
                print(Fore.YELLOW+Style.BRIGHT + "The system cannot find the path specified.\n")
                return

        p = subprocess.Popen(["call"]+command.split(" "), stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, shell=True)

        while p.poll() is None:
            a = p.stdout.readline()
            a = self.decoder(a)
            print(a, end="")
        print()

class MC(executer):
    def __init__(self, main):
        super().__init__("MC", "Shortcut to Minecrft Client", Fore.YELLOW)
        self.main = main

    def getSelf(self):
        return MinecrftClient(self.main)

class FileCacher:
    "Cache the stdout text so we can analyze it before returning it"
    def __init__(self):
        self.reset()
    def reset(self):
        self.out = []
    def write(self,line):
        self.out.append(line)
    def flush(self):
        output = '\n'.join(self.out)
        self.reset()
        return output

class Shell(InteractiveConsole):
    "Wrapper around Python that can filter input/output to the shell"
    def __init__(self, caller):
        self.stdout = sys.stdout
        self.cache = FileCacher()
        self.caller = caller
        InteractiveConsole.__init__(self)
        return

    def get_output(self):
        sys.stdout = self.cache
    def return_output(self):
        sys.stdout = self.stdout

    def raw_input(self, prompt):
        self.caller.prompt()

        return super().raw_input("")

    def push(self, line):
        self.get_output()
        # you can filter input here by doing something like
        # line = filter(line)
        if self.caller.analyze(line):
            self.push("exit()")
            return

        InteractiveConsole.push(self, line)
        self.return_output()
        output = self.cache.flush()
        # you can filter the output here by doing something like
        # output = filter(output)
        print(output.replace("\n\n\n", "\n"), end="") # or do something else with it
        return

class Python(executer):
    def __init__(self, caller):
        super().__init__("Python", "Runs and returns the results of Python commands", Fore.GREEN)
        self.shell = Shell(caller)

    def get_linestat(self):
        return ">>> "

    def get(self, command):
        return self.shell.push(command)
        super().get(command)

class Py(executer):
    def __init__(self, main):
        super().__init__("Py", "Shortcut to PYTHON", Fore.GREEN)
        self.main = main

    def getSelf(self):
        return Python(self.main)


class helpMgr():
    def __init__(self):
        self.BASE = 0
        self.ALL = 1
        self.EXECS = 2
        self.COMMANDS = 3

        self.allopts = {}

    def list(self, type):
        if type == self.ALL:
            for i in self.allopts:
                new = self.allopts[i]
                print("%s%s%s." %(new.name, " "*(15-len(new.name)),new.description))
        for i in self.allopts:
            if self.allopts[i].type == type:
                new = self.allopts[i]
                print("%s%s%s." %(new.name, " "*(15-len(new.name)),new.description))

    def help_specified(self, name):
        try:
            item = self.get(name)
            print(Fore.MAGENTA+Style.DIM + "%s.\n" %item.description)

            print("%s"%item.name.upper(), end="")
            for i in item.params:
                print(" [%s]" %i, end="")
            print()
            for i in item.params:
                print("  %s%s%s." %(i, " "*(12-len(i) ), item.params[i]))
            print()

        except KeyError:
            print(Fore.YELLOW+Style.BRIGHT + "This command is not supported by the help utility.\n")

    def add_opt(self, new):
        self.allopts[new.name.upper()] = new

    def get(self, name):
        return self.allopts[name]

class helpItem():
    def __init__(self, name, desc, type = helpMgr().BASE, params = {}):
        self.name = name
        self.description = desc
        self.params = params
        self.type = type


class caller:
    def __init__(self, perms, col):
        self.executers = []
        self.executer = None
        self.perms = perms
        self.col = col
        self.helpMgr = helpMgr()

    def prompt(self):
        print(self.col+Style.BRIGHT + "[%s]" %self.perms, end="")
        print(self.executer.col + "[%s] " %self.executer.name, end="")
        print(Fore.WHITE+Style.DIM + "%s" %self.executer.get_linestat(), end="")
        print(Fore.WHITE+Style.BRIGHT, end="")

    def get_input(self):
        print(self.col+Style.BRIGHT + "[%s]" %self.perms, end="")
        print(self.executer.col + "[%s] " %self.executer.name, end="")
        print(Fore.WHITE+Style.DIM + "%s" %self.executer.get_linestat(), end="")
        print(Fore.WHITE+Style.BRIGHT, end="")
        return input("")

    def analyze(self, current):
        if current[0:4].lower() == "exec":
            new = current[5::]
            if new.lower() == "list":
                print(Fore.MAGENTA+Style.DIM,end="")
                self.helpMgr.list(self.helpMgr.EXECS)

            for i in self.executers:
                if new.lower() == i.name.lower():
                    if i.getSelf().name == self.executer.name:
                        print(Fore.YELLOW+Style.BRIGHT + "Already running with %s\n" %new)
                        return True
                    self.select(i.getSelf())
                    print(Fore.GREEN+Style.BRIGHT + "Now Running command with %s\n" %i.getSelf().name)
            return True
        if current.lower() == "cls":
            os.system("cls")
            return True
        if current.lower() == "exit":
            exit()
            return True

        if current[0:4].lower() == "help":

            if current[5::].strip() == "":
                print(Fore.MAGENTA+Style.DIM + "For more information on a specific command, type HELP command-name\n")
                self.helpMgr.list(self.helpMgr.ALL)

            else:
                self.helpMgr.help_specified(current[5::].upper())
            return True

    def resp(self, current):
        resp = self.executer.get(current)

        if resp != None:
            print(resp)

    def select(self, toSelect):
        self.executer = toSelect
        for i in self.executers:
            i.isCurrent = False
            i.eventOff()
        self.executer.isCurrent = True
        self.executer.eventOn()

    def add_exec(self, new):
        self.executers.append(new)

    def _loop(self):
        current = self.get_input()
        if not self.analyze(current):
            self.resp(current)
        self._loop()

    def mainloop(self):
        if len(self.executers) != 0:
            self.select(self.executers[0])
        else:
            raise Exception("You need at least 1 executer.")



        self.helpMgr.add_opt(helpItem("EXEC", "Used to switch between command executers e.g. exec cmd", self.helpMgr.COMMANDS, {"executer":"The name of the executer you with to use", "list":"lists all available executers"}))
        self.helpMgr.add_opt(helpItem("HELP", "Provides Help information for Manager commands",         self.helpMgr.COMMANDS, {"command":"displays help information on that command"}))
        self.helpMgr.add_opt(helpItem("CLS", "Clears the screen",                                       self.helpMgr.COMMANDS, ))
        self.helpMgr.add_opt(helpItem("EXIT", "Quits the Manager program (command interpreter)",        self.helpMgr.COMMANDS, ))

        for i in self.executers:
            self.helpMgr.add_opt(helpItem(i.name.upper(), i.description, self.helpMgr.EXECS))

        self.helpMgr.get("TEST").params = {"command":"a test parameter", "thing":"a different test parameter"}



        self._loop()


try:
    isAdmin = ctypes.windll.shell32.IsUserAnAdmin()
except:
    isAdmin = 0

if isAdmin == 0:
    main = caller(os.getlogin(), Fore.CYAN)
if isAdmin == 1:
    main = caller("Admin", Fore.RED)

main.add_exec(CMD(main.perms))
main.add_exec(executer("test", "A description for the base object", Fore.CYAN))
main.add_exec(Python(main))
main.add_exec(Py(main))
main.add_exec(MinecrftClient(main))
main.add_exec(MC(main))


main.mainloop()

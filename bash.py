import cmd
import os
from base import executer, colour

class Bash(cmd.CMD):
    def __init__(self, executer, perms):
        self.name = "bash"
        self.description = "Runs and returns the results of some bash commands"
        self.col = colour("yellow")

        if perms != "root":
            os.chdir("C:\\Users\\%s" %os.getlogin())
        else:
            os.chdir("C:\\WINDOWS\\system32")

    def get_linestat(self):
        return "%s $ " %os.getcwd()

    def get(self, command):
        if command.strip()[0:2].lower() == "ls":
            d = command[3::].lower() if command[3::].strip() != "" else None

            out = []
            for i in os.scandir(d):
                iname = "'%s'"%i.name if " " in i.name else i.name
                if iname[0:10] == "NTUSER.DAT":
                    continue
                if iname[0:8] == "GodMode.":
                    continue

                if i.is_dir():
                    out.append("%s%s%s/"%(colour("blue"), iname, colour("white")))
                else:
                    out.append("%s%s%s"%(colour("white"), iname, colour("white")))

            mxl = max(len(x) for x in out)
            colls = int(round(os.get_terminal_size().columns / mxl, 0))
            colls = 1 if colls <= 0 else colls

            for i in range(len(out)):
                print("%s%s"%(out[i], " "*(mxl-len(out[i]))), end="")
                if i % colls == 0:
                    if i != len(out)-1:
                        print("")
        print("\n")




if __name__ == '__main__':
    os.chdir("C:\\Users\\James\\OneDrive\\Documents\\Coding\\python\\Programs\\new cmd")
    a = Bash(0, "roota")
    a.get("ls")
    a.get("ls Desktop")

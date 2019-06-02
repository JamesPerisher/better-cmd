import cmd
import os
from base import executer, colour

class Bash(cmd.CMD):
    def __init__(self, perms):
        self.name = "bash"
        self.desc = "Runs and returns the results of some bash commands"
        self.col = colour("black")

        if perms != "root":
            os.chdir("C:\\Users\\%s" %os.getlogin())
        else:
            os.chdir("C:\\WINDOWS\\system32")
        self.dir = os.getcwd()

    def get_linestat(self):
        return "%s $ " %self.dir

    def get(self, command):
        if command[0:2] == "ls":
            command = "dir /w"+command[3::]
        super().get(command)


if __name__ == '__main__':
    a = Bash("roota")
    a.get("ls")

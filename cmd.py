import subprocess
import os
from base import executer, colour


class CMD(executer):
    def __init__(self, caller, perms):
        super().__init__("CMD", "Runs and returns the results of CMD commands", colour("cyan"))

        if perms != "Admin":
            os.chdir("C:\\Users\\%s" %os.getlogin())
        else:
            os.chdir("C:\\WINDOWS\\system32")

    def get_linestat(self):
        return "%s> " %os.getcwd()

    def decoder(self, bytein):
        out = str(bytein).replace("\\r", "").replace("\\n", "\n").replace("\\\'", "\'").replace("\\\\", "\\")   #fixes basic \n \r
        out = out.replace("\\xb3", "│").replace("\\xc3", "├").replace("\\xc0", "└").replace("\\xc4", "─")   #fixes byte error with .decode()

        return out[2:-1]

    def get(self, command):
        if command == "":
            return
        p = subprocess.Popen(["call"]+command.split(" "), stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, shell=True)

        while p.poll() is None:
            a = p.stdout.readline()
            a = self.decoder(a)
            print(a, end="")
        print()

if __name__ == '__main__':
    a = CMD("user")
    a.get("dir")

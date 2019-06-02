import os
import cmd
from base import colour,base_interpereter


class caller:
    def __init__(self, perms, col):
        self.perms = perms
        self.col = col
        self.all_exec = []
        self.exec = None

    def add_exec(self, new):
        self.all_exec.append(new(self, self.perms))
        self.exec = self.all_exec[0]

    def prompt(self):
        print("%s[%s]%s[%s]%s%s" %(self.col, self.perms, self.exec.col, self.exec.name, colour("white", bright=False), self.exec.get_linestat()), end="")
        return input(colour("white", bright=True))

    def get(self, comm):
        try:
            self.exec.get(comm)
        except:
            print("error")

    def mainloop(self):
        while True:
            comm = self.prompt()
            check_comm = base_interpereter(comm)
            if check_comm == None:
                continue

            if check_comm[0] == "exec":
                print("changing exec to %s"%check_comm[1])
                continue
            self.get(check_comm)





if __name__ == '__main__':
    a = caller("user", colour("blue"))
    a.add_exec(cmd.CMD)
    a.mainloop()

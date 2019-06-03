import os
import cmd
import python
from base import colour,base_interpereter


class caller:
    def __init__(self, perms, col):
        self.perms = perms
        self.col = col
        self.all_exec = {}
        self.exec = None

    def add_exec(self, new):
        new = new(self, self.perms)
        self.all_exec[new.name.lower()] = new
        self.exec = self.all_exec[list(self.all_exec)[0]]

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
                if check_comm[1] == "list":
                    maxex     = max(len(x) for x in [self.all_exec[y].name        for y in self.all_exec])+2
                    maxexname = max(len(x) for x in [self.all_exec[y].description for y in self.all_exec])
                    out = "\n".join([("%s%s%s%s"%(self.all_exec[x].name, " "*(maxex-len(self.all_exec[x].name)), self.all_exec[x].description, " "*(maxexname-len(self.all_exec[x].description)))) for x in self.all_exec])
                    print(colour("magenta", bright=False)+out+"\n")
                    continue
                try:
                    self.exec = self.all_exec[check_comm[1]]
                    print("%sset current executer to %s\n"%(colour("green", bright=False), check_comm[1]))
                except KeyError:
                    print("%sno module named %s\n"%(colour("red", bright=False), check_comm[1]))
                continue
            self.get(check_comm)





if __name__ == '__main__':
    a = caller("user", colour("blue"))
    a.add_exec(cmd.CMD)
    a.add_exec(python.Python)
    a.mainloop()

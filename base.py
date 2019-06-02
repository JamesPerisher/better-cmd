def color_table():
    print("\033[0;37;40m Normal text\n")
    print("\033[2;37;40m Underlined text\033[0;37;40m \n")
    print("\033[1;37;40m Bright Colour\033[0;37;40m \n")
    print("\033[3;37;40m Negative Colour\033[0;37;40m \n")
    print("\033[5;37;40m Negative Colour\033[0;37;40m\n")

    print("\033[1;37;40m \033[2;37:40m TextColour BlackBackground          TextColour GreyBackground                WhiteText ColouredBackground\033[0;37;40m\n")
    print("\033[1;30;40m Dark Gray      \033[0m 1;30;40m            \033[0;30;47m Black      \033[0m 0;30;47m               \033[0;37;41m Black      \033[0m 0;37;41m")
    print("\033[1;31;40m Bright Red     \033[0m 1;31;40m            \033[0;31;47m Red        \033[0m 0;31;47m               \033[0;37;42m Black      \033[0m 0;37;42m")
    print("\033[1;32;40m Bright Green   \033[0m 1;32;40m            \033[0;32;47m Green      \033[0m 0;32;47m               \033[0;37;43m Black      \033[0m 0;37;43m")
    print("\033[1;33;40m Yellow         \033[0m 1;33;40m            \033[0;33;47m Brown      \033[0m 0;33;47m               \033[0;37;44m Black      \033[0m 0;37;44m")
    print("\033[1;34;40m Bright Blue    \033[0m 1;34;40m            \033[0;34;47m Blue       \033[0m 0;34;47m               \033[0;37;45m Black      \033[0m 0;37;45m")
    print("\033[1;35;40m Bright Magenta \033[0m 1;35;40m            \033[0;35;47m Magenta    \033[0m 0;35;47m               \033[0;37;46m Black      \033[0m 0;37;46m")
    print("\033[1;36;40m Bright Cyan    \033[0m 1;36;40m            \033[0;36;47m Cyan       \033[0m 0;36;47m               \033[0;37;47m Black      \033[0m 0;37;47m")
    print("\033[1;37;40m White          \033[0m 1;37;40m            \033[0;37;40m Light Grey \033[0m 0;37;40m               \033[0;37;48m Black      \033[0m 0;37;48m")


def colour(col, bright=True, background = "black"):
    if bright == True:
        bright = "true"
    if bright == False:
        bright = "false"
    colours = {"black":30,"red":31,"green":32,"yellow":33,"blue":34,"magenta":35,"cyan":36,"white":37}
    br = {"true":1, "false":0}
    return "\033[%s;%s;%sm" %(br[bright], colours[col], colours[background]+10)

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

def base_interpereter(comm):
    if comm.strip() == "":
        return
    if comm.strip().lower() == "help":
        print("%shelp"%colour("magenta", bright=False))
        return
    if comm.strip().lower() == "exit":
        print("%sexiting%s\n"%(colour("green", bright=False), colour("white", bright=False)))
        exit()
    if comm.strip()[0:4].lower() == "exec":
        arg = comm[5::].strip().lower()
        if arg == "":
            print("%sno argument specified\n"%colour("red", bright=False))
            return
        return ("exec", arg)
    return comm


if __name__ == '__main__':
    base_interpereter("exec")
    base_interpereter("exec hello")

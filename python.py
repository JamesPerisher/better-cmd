from code import InteractiveConsole
import sys
from base import executer, colour



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
    def __init__(self):
        self.stdout = sys.stdout
        self.cache = FileCacher()
        InteractiveConsole.__init__(self)

    def get_output(self):
        sys.stdout = self.cache
    def return_output(self):
        sys.stdout = self.stdout

    def push(self, line):
        self.get_output()
        if line.strip() == "exit()":  # filtering input
            print("can not escape current execution.")
            return

        InteractiveConsole.push(self, line)
        self.return_output()
        output = self.cache.flush()
        # output can be filtered
        print(output.replace("\n\n\n", "\n"), end="") # or do something else with it
        return

class Python(executer):
    def __init__(self, caller, perms):
        super().__init__("Python", "Runs and returns the results of Python commands", colour("green"))
        self.shell = Shell()

    def get_linestat(self):
        return ">>> "

    def get(self, command):
        return self.shell.push(command)
        super().get(command)


if __name__ == '__main__':
    a = Python()
    a.get("exit()")
    a.get("print('test')")

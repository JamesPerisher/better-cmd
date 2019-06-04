import uuid
import os
import subprocess as sb
from base import executer, colour


class MAC_Spoof(executer):
    def __init__(self, caller, perms):
        super().__init__("MAC", "Spoof and view divice mac adresses", colour("cyan"))

    def _get_list_format(self, v):
        v = [["name", "device", "current mac"]] + v
        out = ""
        max_len = max( len(str(x)) for k in v for x in k)
        for inner in v:
            first = True
            for elem in inner[:-1]: # all but the last
                text = "{}".format(elem).ljust(max_len+2)
                out = out + (text)

            out = out + (inner[-1]) + "\n" # print last
        return out

    def get_list(self, ):
        a = sb.check_output('spoof-mac.py list', shell=True).decode().split("\n")[0:-1]
        out = []
        for i in a:
            i = i.replace("\r", "")
            current = []
            current.append(i.split("\" on device \"")[0][3::])
            current.append(i.split("\" with MAC address ")[0][len(current[-1])+16::])
            current.append(i.split(" currently set to ")[0][len(current[-1])+len(current[-2])+35::])
            out.append(current)
        return out


    def get(self, comm):
        if comm.strip() == "list":
            print(self._get_list_format(self.get_list()))


if __name__ == '__main__':
    a = MAC_Spoof(0, 0)
    a.get("list")

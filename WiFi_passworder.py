import subprocess
from base import executer, colour


class WiFi_cache(executer):
    def __init__(self, caller, perms):
        super().__init__("WiFi_cache", "Gets cached wifi passwords", colour("cyan"))

    def get_profiles(self):
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
        profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
        return profiles

    def get_pass(self, profile):
        try:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
            results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
            try:
                return (profile,results[0])
            except IndexError:
                return (profile,None)
        except subprocess.CalledProcessError:
            return (profile,"ENCODING ERROR")
        return data

    def get_all(self):
        data = {}
        for i in self.get_profiles():
            current = self.get_pass(i)
            data[current[0]] = current[1]
        return data

    def get(self, comm):
        if comm.lower().strip() == "/?":
            print("%scommands: list, get [network name]\n"%colour("magenta", bright=False))
            return
        if comm.lower().strip() == "list":
            a = {"network name":"password", **self.get_all()}
            max_len = max(max(len(str(x)),len(str(a[x]))) for x in a)+1
            b = [(i+(" "*(max_len-len(i))), str(a[i]).replace("None", "")+(" "*(max_len-len(str(a[i]))))) for i in a]
            out = "\n".join(i[0]+i[1] for i in b)
            print("%s\n"%out)
            return
        if comm.lower()[0:3] == "get":
            try:
                print("%s\n"%self.get_all()[comm[3::].strip()])
                return
            except KeyError:
                print("%sno network named: %s\n"%(colour("red", bright=False), comm[3::].strip()))
                return
        print("%s'%s' is not a command in this executer.\n"%(colour("red", bright=False), comm.strip().split(" ")[0].lower()))


if __name__ == '__main__':
    a = WiFi_cache(0, 0)
    a.get("list")
    a.get("get Telekom_FON")
    a.get("get no net")
    a.get("er")

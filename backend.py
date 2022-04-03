import subprocess

class Backend():
    def __init__(self):
        self.path = None
    
    def set(self, path, mode):
        self.path = path
        if mode:
            self.interface = "fwk"
        else:
            self.interface = None

    def run(self, command, args):
        if not self.path:
            return
        subprocess.run([self.path] + (["--interface=" + self.interface] if self.interface else []) + [command] + args)

    def change_color(self, name, r, g, b):
        self.run('led', [name, "red=" + str(r)])
        self.run('led', [name, "green=" + str(g)])
        self.run('led', [name, "blue=" + str(b)])

    def fan(self, value):
        if value == -1:
            self.run("autofanctrl", ["on"])
        else:
            self.run("fanduty", [str(round(value))])

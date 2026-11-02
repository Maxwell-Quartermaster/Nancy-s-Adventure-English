"""Shared harness for the QM self-tests. Scratch goes to runs/selftest/<stamp>-<tool>/ (made with os.makedirs,
never /tmp or another bot's folder) and is never deleted. Older runs stay parked in selftest-runs/."""
import datetime, os, subprocess, sys
from zoneinfo import ZoneInfo
HERE = os.path.dirname(os.path.abspath(__file__))


def scratch(name):
    d = os.path.join(HERE, "runs", "selftest", datetime.datetime.now(ZoneInfo("America/Denver")).strftime("%Y%m%d-%H%M%S-%f") + "-" + name)
    os.makedirs(d)  # parents created too (runs/selftest/)
    return d


def run(tool, *args):
    p = subprocess.run([sys.executable, os.path.join(HERE, tool), *args], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


class T:
    def __init__(self, name):
        self.name, self.n, self.fail = name, 0, []

    def ok(self, cond, label, out=""):
        self.n += 1
        print(("PASS " if cond else "FAIL ") + label)
        if not cond:
            self.fail.append(label)
            print("     output: " + out.strip().replace("\n", "\n     "))

    def done(self):
        print(f"{self.name}: {self.n - len(self.fail)}/{self.n} passed")
        return 1 if self.fail else 0

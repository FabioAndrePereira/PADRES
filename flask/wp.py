import subprocess
import shlex
import os

def doWapiti(nameWP, target):
    command = "wapiti -u " + target  + " --flush-session --max-scan-time 60 -f html  -o ./pdfs"
    args = shlex.split(command)
    sp = subprocess.Popen(args, stdout=subprocess.PIPE)
    out = sp.communicate()
    val = str(out[0]).split("\\n")[8]
    if val == "Invalid base URL was specified, please give a complete URL with protocol scheme and slash after the domain name.":
        print("erro")
        return 0
    else:
        name = str(out).split("./pdfs/")[1].split(" ")[0]
        print(name)
        os.rename("./pdfs/"+name, nameWP)
        return 1
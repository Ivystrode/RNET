import socket
import subprocess

label = "[" + socket.gethostname() + "]"

def reboot():
    print("made it to cpu con reboot func")
    reboot_command = "/user/bin/sudo /sbin/reboot =r now"
    print("issue subprocess comd")
    process = subprocess.Popen()(reboot_command.split(), stdout=subprocess.PIPE)
    print("output=")
    output=process.communicate()[0]
    print(f"{label} {output}")
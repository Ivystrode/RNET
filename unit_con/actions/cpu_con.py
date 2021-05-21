import socket
import subprocess

label = "[" + socket.gethostname() + "]"

def reboot():
    reboot_command = "/usr/bin/sudo /sbin/reboot =r now"
    process = subprocess.Popen(reboot_command.split(), stdout=subprocess.PIPE)
    output=process.communicate()[0]
    print(f"{label} {output}")
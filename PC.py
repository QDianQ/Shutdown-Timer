import os

def shutdown(time):
    os.system(f"shutdown -s -t {time}")

def reboot(time):
    os.system(f"shutdown -r -t {time}")

def abortShutdown():
    os.system(f"shutdown -a")

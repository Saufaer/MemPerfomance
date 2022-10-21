import subprocess
try:
    subprocess.run(["perf", "record", "-d", "-e", "cpu/event=0xd0,umask=0x83/ppu", "-c", "2000003"])
except KeyboardInterrupt:
    exit()

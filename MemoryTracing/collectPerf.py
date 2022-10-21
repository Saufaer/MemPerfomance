import subprocess
try:
    subprocess.run(["perf", "record", "-d", "-e", "cpu/event=0xd0,umask=0x83/ppu", "-c", "1003"])
except KeyboardInterrupt:
    exit()

#perf record -d -e cpu/event=0xd0,umask=0x83/ppu -c 2000003
#perf record -d -e cpu/event=0xd0,umask=0x81/ppu,cpu/event=0xd0,umask=0x82/ppu -c 2000003
#-c <SampleAfterValue>
#-d - write data linear address

#perf report -D | fgrep SAMPLE
#perf script -F ip,sym,addr
#perf script -F time,addr
#perf script -F addr


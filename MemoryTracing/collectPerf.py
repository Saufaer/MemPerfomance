import subprocess
try:
    subprocess.run(["perf", "record", "-d", "-e", "cpu/event=0xd0,umask=0x83/ppu", "-c", "1003"])
except KeyboardInterrupt:
    exit()

# sudo /opt/5.3.18-lp152.106-perf-buffer/perf record --data --event=cpu/event=0xd0,umask=0x83/ppu -c 1
# sudo /opt/5.3.18-lp152.106-perf-buffer/perf record --data --event=cpu/event=0xd0,umask=0x81/ppu,cpu/event=0xd0,umask=0x82/ppu -c 1

# sudo /home/o.lalykin/perfBufftest/mat/scripts/module.sh reset;
# sudo /home/o.lalykin/perfBufftest/mat/scripts/module.sh --buffer-size 0.3G set;
# sudo /home/o.lalykin/perfBufftest/mat/scripts/module.sh showbuffers
# sudo /home/o.lalykin/perfBufftest/mat/scripts/module.sh write
# sudo /home/o.lalykin/perfBufftest/mat/scripts/binaryToHex.py 


#perf record -d -e cpu/event=0xd0,umask=0x83/ppu -c 2000003
#perf record -d -e cpu/event=0xd0,umask=0x81/ppu,cpu/event=0xd0,umask=0x82/ppu -c 2000003
#-c <SampleAfterValue>
#-d - write data linear address

#perf report -D | fgrep SAMPLE
#perf script -F ip,sym,addr
#perf script -F time,addr
#perf script -F addr

#######
#perf mem -t load,store rec
#perf mem -t load,store rep --sort=mem --stdio
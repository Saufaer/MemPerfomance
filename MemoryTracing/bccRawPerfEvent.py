import bcc
import os
import time
import unittest
from bcc import BPF, PerfType, PerfHWConfig, PerfSWConfig, PerfEventSampleFormat
from bcc import Perf
from bcc.utils import printb
from time import sleep
import ctypes as ct
#from utils import kernel_version_ge, mayFail

# on x86, need to set precise_ip in order for perf_events to write to 'addr'
bpf_text=b"""
#include <linux/perf_event.h>

struct data_t {
    u64 addr;
    char comm[TASK_COMM_LEN];
};

BPF_HASH(counts, struct data_t);

int on_sample_hit(struct bpf_perf_event_data *ctx) {
    u64 zero = 0;
    struct data_t data = {};
    data.addr = ctx->addr;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));

    u64 *val = counts.lookup_or_try_init(&data, &zero);
    if (val) {(*val)++;}
    return 0;
}

"""

b = BPF(text=bpf_text)
try:
    event_attr = Perf.perf_event_attr()

    event_attr.exclude_kernel = 1

    event_attr.type = PerfType.RAW #
    #4383d0 = ?? + "UMask": "0x83" + "EventCode": "0xD0" = ?? + 83 + d0
    # ?? = 43 = Precise event with data address
    event_attr.config = int("4383d0",16) #MEM_INST_RETIRED.ANY_PS:pp -> Precise event with data address
    event_attr.sample_type = PerfEventSampleFormat.ADDR
    #event_attr.sample_type = int("7df",16) # PERF_SAMPLE_ADDR

    event_attr.sample_period = 1003
    event_attr.precise_ip = 2
    b.attach_perf_event_raw(attr=event_attr, fn_name=b"on_sample_hit", pid=-1, cpu=-1)
except Exception:
    print("Failed to attach to a raw event. Please check the event attr used")
    exit()

def printData():
    counts = b.get_table("counts")   
    for k, v  in counts.items():
        print(k.addr,v.value)# addr; count of events

try:
    sleep(10)
    printData()
except KeyboardInterrupt:
    printData()
    exit()



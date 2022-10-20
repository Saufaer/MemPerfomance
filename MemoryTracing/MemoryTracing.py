#!/usr/bin/env python3

import bcc
import os
import time
import unittest
from bcc import BPF, PerfType, PerfHWConfig, PerfSWConfig, PerfEventSampleFormat
from bcc import Perf
from bcc.utils import printb
from time import sleep

bpf_text=b"""
#include <linux/perf_event.h>
struct key_t {
  int cpu;
  int pid;
  char name[100];
};
BPF_HASH(counts,int, u64);

static inline __attribute__((always_inline)) void get_key(struct key_t* key) {
  key->cpu = bpf_get_smp_processor_id();
  key->pid = bpf_get_current_pid_tgid();
  bpf_get_current_comm(&(key->name), sizeof(key->name));
}

int on_sample_hit(struct bpf_perf_event_data *ctx) {
  struct key_t key = {};
  get_key(&key);
  u64 zero = 0;
  u64 addr = ctx->addr;

  u64 *val = counts.lookup_or_try_init(&key.pid, &zero);
  if (val) {(*val)++;}
  //bpf_trace_printk("test_attach_raw_event_x86: pid: %ld, comm: %s, addr: 0x%llx\\n", key.pid, key.name, addr);

return 0;
}

"""

b = BPF(text=bpf_text)
try:
    event_attr = Perf.perf_event_attr()
    event_attr.type = Perf.PERF_TYPE_HARDWARE
    event_attr.config = PerfHWConfig.CPU_CYCLES
    event_attr.sample_period = 10
    event_attr.sample_type = PerfEventSampleFormat.ADDR
    event_attr.exclude_kernel = 1
    event_attr.precise_ip = 0
    b.attach_perf_event_raw(attr=event_attr, fn_name=b"on_sample_hit", pid=-1, cpu=-1)

except Exception:
    print("Failed to attach to a raw event. Please check the event attr used")
    exit()

counts = b.get_table("counts")

print("Running for 10 seconds or hit Ctrl-C to end. Check trace file for samples information written by bpf_trace_printk.")
for i in range(10):
    try:
        sleep(1)
        printb(b"\nIteration %i, Collected %i events"%(i, len(counts)))
        printb(b"PID CACHE_MISSES")
        for k, v in sorted(counts.items(), key=lambda counts: counts[0].value):
            printb(b"%i %i" % (k.value, v.value))

        counts.clear()

    except KeyboardInterrupt:
        exit()
#!/usr/bin/python3
import time
from bcc import BPF

# 定義一個 inline BPF program，裡面是 C 語言程式碼
prog = """
int hello_world(void *ctx) {
	bpf_trace_printk("hello, world!\\n");
	return 0;
}
"""

b = BPF(text=prog)
b.attach_kprobe(event="__x64_sys_clone", fn_name="hello_world")

try:
	while True:
		(task, pid, cpu, flags, ts, msg) = b.trace_fields()
		print(f"Program:{task.decode('utf-8')}-{pid} / Message:{msg.decode('utf-8')}")
		time.sleep(1)
except KeyboardInterrupt:
    pass

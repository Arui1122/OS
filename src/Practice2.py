import time
from bcc import BPF

prog = """
int mkdir_detector(void *ctx){
    bpf_trace_printk("A new folder has been created!!!\\n");
    return 0;
}
"""

b = BPF(text = prog)
b.attach_kprobe(event = "__x64_sys_mkdir", fn_name = "mkdir_detector")

try:
    while True:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
        print(f"Program:{task.decode('utf-8')}-{pid} / CPU:{cpu} / Message:{msg.decode('utf-8')}")
        time.sleep(1)
except KeyboardInterrupt:
    pass

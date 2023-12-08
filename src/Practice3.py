#!/usr/bin/python3
import time
from bcc import BPF

prog = r"""
//創建用於儲存task的map
BPF_TASK_STORAGE(task_storage_map, __u64);

KFUNC_PROBE(__x64_sys_link)
{
    //__u64代表64-bit的非負整數
    //bpf_ktime_get_ns()是eBPF內建用於查詢timestamp的function
    __u64 timestamp = bpf_ktime_get_ns();

    //將timestamp儲存於電腦記憶體中
    task_storage_map.task_storage_get(bpf_get_current_task_btf(), &timestamp, BPF_LOCAL_STORAGE_GET_F_CREATE);

    return 0;
}

KRETFUNC_PROBE(__x64_sys_link)
{
    __u64 *timestamp;

    timestamp = task_storage_map.task_storage_get(bpf_get_current_task_btf(), 0, 0);
    if (!timestamp)
        return 0;

    //在此填入缺少的程式碼!!!!!!!
    __u64 exit_timestamp = bpf_ktime_get_ns();
    __u64 start_timestamp = *timestamp;
    __u64 elapsed_time = exit_timestamp - start_timestamp;
    
    task_storage_map.task_storage_delete(bpf_get_current_task_btf());

    bpf_trace_printk("__x64_sys_link exit: cost %lldns\n", elapsed_time);

    return 0;
}
"""

b = BPF(text=prog)
try:
    while True:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
        print(f"{msg.decode('utf-8')}")
        time.sleep(1)
except KeyboardInterrupt:
    pass

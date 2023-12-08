#!/usr/bin/python3
import time
from bcc import BPF

prog = """
BPF_HASH(detector_timer_map);
BPF_HASH(packets_number_map);

int ddos_detector(void *ctx) {
    __u64 max_packets_number_per_ten_seconds = 10000;
    __u64 receive_packets_index = 0, receive_packets_init_value = 0,*receive_packets_number;
    __u64 ddos_detector_timer_index = 0, ddos_detector_timer_init_value = bpf_ktime_get_ns(),*ddos_detector_timer;

    receive_packets_number=packets_number_map.lookup_or_init(&receive_packets_index,&receive_packets_init_value);
    ddos_detector_timer=detector_timer_map.lookup_or_init(&ddos_detector_timer_index,&ddos_detector_timer_init_value);

    //在此填入缺少的程式碼!!!!!!!
    __u64 current_time = bpf_ktime_get_ns();
    
    // Reset values every 10 seconds
    if(current_time - *ddos_detector_timer >= (__u64)10 * 1000000000){
        *ddos_detector_timer = current_time;
        *receive_packets_number = 0;
    };
    
    // Increment received packets
    (*receive_packets_number)++;

    // Check for potential DDos attack
    if(*receive_packets_number > max_packets_number_per_ten_seconds){
        bpf_trace_printk("Detect DDoS!!! => number of packets in ten seconds: %llu\n", *receive_packets_number);
    };

    packets_number_map.update(&receive_packets_index,receive_packets_number);
    detector_timer_map.update(&ddos_detector_timer_index, ddos_detector_timer);

    return 0;

};
"""

b = BPF(text=prog)
b.attach_kprobe(event="ip_rcv", fn_name="ddos_detector")
try:
    while True:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
        print(f"{msg.decode('utf-8')}")
except KeyboardInterrupt:
    pass

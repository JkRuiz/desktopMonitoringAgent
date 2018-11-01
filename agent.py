import argparse
import sys
from time import sleep, time

import helpers.db_helper as db
import helpers.data_helper as dh
from utils.cpu_utils import CPUUtils
from utils.disk_utils import DiskUtils
from utils.network_utils import NetworkUtils
from utils.ram_utils import RAMUtils
from utils.vm_utils import VMUtils
from utils.process_utils import ProcessUtils

FREQUENCY = 1
INFINITE = True
DURATION = 0
UNACLOUD_PORT = 10027

network_utils = NetworkUtils()
cpu_utils = CPUUtils()
ram_utils = RAMUtils()
disk_utils = DiskUtils()
vm_utils = VMUtils()
vbox_process = ProcessUtils(VMUtils.VBOX_PROCESS)
unacloud_process = None


def parse_arguments():
    global unacloud_process
    parser=argparse.ArgumentParser(description="Monitor the machine's resources")
    parser.add_argument('-f', '--frequency', type=int,
                        help='Frequency (in seconds) with which the agent will send system information')
    parser.add_argument('-d', '--duration', type=int,
                        help='Duration (in seconds) for which the problem will run')
    parser.add_argument('-pp', '--pport', type=int,
                        help='Port in which the UnaCloud process is running')
    args = parser.parse_args()
    if args.frequency:
        global FREQUENCY
        FREQUENCY = args.frequency
    if args.duration:
        global DURATION, INFINITE
        DURATION = args.duration
        INFINITE = False
    if args.pport:
        global UNACLOUD_PORT
        UNACLOUD_PORT = args.pport
    unacloud_process = ProcessUtils(port=UNACLOUD_PORT)


def main():
    parse_arguments()
    db.post_hardware_info(get_initial_info())
    curr_duration = DURATION
    while (curr_duration > 0) or INFINITE:
        start_time = time()
        db.post_metric(get_system_info())
        if not INFINITE:
            curr_duration = curr_duration - FREQUENCY
        sleep(FREQUENCY - ((time() - start_time) % FREQUENCY))


def get_system_info():
    return {
        "timestamp": dh.format_time(),
        "ip": network_utils.get_ip_addr(),
        "ram": ram_utils.get_ram_percent(),
        "swap": ram_utils.get_swap_memory(),
        "disk": disk_utils.get_disk_percent(),
        "cpu": cpu_utils.get_cpu_percent(),
        "cpu_details": cpu_utils.get_percpu_peruser_percent(),
        "net_io_counters": network_utils.get_net_io_counters(),
        "vms": vm_utils.get_vms(running=False),
        "running_vms": vm_utils.get_vms(),
        "virtualbox_status": vm_utils.get_vbox_status(),
        "vbox_process_count": ProcessUtils.count_processes_by_name(VMUtils.VBOX_PROCESS),
        "unacloud_status": 1 if unacloud_process.get_process_status() == "running" else 0
    }

def get_initial_info():
    return {
        "cpu_count": cpu_utils.get_cpu_count(),
        "disk_partitions": disk_utils.get_disk_partitions(),
        "total_ram": ram_utils.get_ram_percent(total=True),
        "total_swap": ram_utils.get_swap_memory(total=True),
        "total_disc": disk_utils.get_disk_percent(total=True)
    }


if __name__ == "__main__":
    main()

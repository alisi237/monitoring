import psutil
import CheckModule
from time import sleep

def check_CPU(soft_limit, hard_limit):
    CheckModule.check_for_excess(soft_limit, hard_limit, psutil.cpu_percent(), "CPU")

def check_RAM(soft_limit, hard_limit):
    CheckModule.check_for_excess(soft_limit, hard_limit, psutil.virtual_memory().percent, "RAM")

def check_disk_storage(disk_path, soft_limit, hard_limit):
    CheckModule.check_for_excess(soft_limit, hard_limit, psutil.disk_usage(disk_path).percent, "Disk " + disk_path)

while True:
    check_CPU(80, 90)
    check_RAM(1, 90)
    check_disk_storage("C:", 50, 60)
    sleep(10)
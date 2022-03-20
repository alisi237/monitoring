import psutil as ps
import ExceedanceCheckModule as ECM

# first element of array is the value, second element is the data source
cpu = [0, 'CPU']
ram = [0, 'RAM']
disk_storage = [0, 'Disk C:']

# queries the values of all data sources and stores them as first element in array
# disk path is defined
def get_data():
    cpu[0] = ps.cpu_percent()
    ram[0] =  ps.virtual_memory().percent
    disk_storage[0] = ps.disk_usage("C:").percent

# parameterized call of the check_for_excess method
def check_value(soft_limit, hard_limit, value):
    ECM.check_for_excess(soft_limit, hard_limit, value[0], value[1])
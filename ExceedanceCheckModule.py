import LoggerService as LS
import MailerService as MS
import platform as pl
import time as tm

# last time a message was written to log file
last_logged_cpu = 0
last_logged_ram = 0
last_logged_disk_storage = 0

# checks if the current value of the chosen data source exceeds any limit 
# and reacts with logging and when exceeding the hard limit sending an email in addition
def check_for_excess(soft_limit, hard_limit, value, data_source):
    if value > float(hard_limit):
        log('critical', data_source, hard_limit, soft_limit, value)
        MS.send_email(get_message_for_mail(data_source, hard_limit, value))
    elif value > float(soft_limit):
        log('warning', data_source, hard_limit, soft_limit, value)
    elif value < float(soft_limit): 
        log('info', data_source, hard_limit, soft_limit, value)

# based on the log level, the method accesses the logger method of the LoggerService with the related log message as parameter     
def log(log_level, data_source, hard_limit, soft_limit, value):
    if check_last_logged(data_source):
        if log_level == 'critical':
            LS.logger.critical(get_message_for_log(data_source, 'hard limit', hard_limit, value))
        elif log_level == 'warning':
            LS.logger.warning(get_message_for_log(data_source, 'soft limit', soft_limit, value))
        elif log_level == 'info':
            LS.logger.info(get_message_for_log(data_source, 'soft limit', soft_limit, value))
             
# creates a message in case the hardlimit is exceeded with subject and text body containing the important information
def get_message_for_mail(data_source, hard_limit, value):
    return 'Subject: {}\n\n{}'.format(
        "CRITICAL INCIDENT",
        "The following object has exceeded the hardlimit: " + data_source 
        + "\n Limit: " + str(hard_limit) 
        + "\n Current Value: " + str(value) 
        + "\n Please perform an action!")

# combines all the information to a log message
def get_message_for_log(data_source, limit_type, limit_value, value):
    return str(pl.uname().node) + " - " + data_source + " --- " + limit_type + ": " + str(limit_value) + "% --- current value: " +  str(value) + "%"

def check_last_logged(data_source):
    global last_logged_cpu
    global last_logged_ram
    global last_logged_disk_storage
    if data_source == 'CPU':
        if check_last_executed(last_logged_cpu, 60):
            last_logged_cpu = tm.time()
            return True
    elif data_source == 'RAM':
        if check_last_executed(last_logged_ram, 60):
            last_logged_ram = tm.time()
            return True
    elif data_source == 'Disk C:':
        if check_last_executed(last_logged_disk_storage, 60):
            last_logged_disk_storage = tm.time()
            return True
    else: 
        return False

# checks if last time executed is longer ago than given seconds       
def check_last_executed(last_time, seconds):
    return tm.time() - last_time > seconds
import PySimpleGUI as sg
import MonitoringModule as MM
import time as tm
   
# default values
cpu_limits = [80, 90]
ram_limits = [80, 90]
disk_limits = [80, 90]
      
# set window theme
sg.theme('Dark Blue 17')
 
# layout of the overview window
layout = [[sg.Text('CPU:            '), sg.Button('monitor', key='cpu_mon'), sg.Button('configure', key='cpu_conf')],
          [sg.Text('RAM:            '), sg.Button('monitor', key='ram_mon'), sg.Button('configure', key='ram_conf')],
          [sg.Text('Disk Storage:'), sg.Button('monitor', key='disk_mon'), sg.Button('configure', key='disk_conf')]]

# returns layout of the configuration window
def get_config_window(data_limits):
    return sg.Window('Configuration', [[sg.Text('Change warning limits:')],
                     [sg.Text('Soft Limit'), sg.Input(key='soft_input'), sg.Text('Current: '), sg.Text(str(data_limits[0]), key='soft_output'), sg.Text('%'), sg.Button('Submit', key='submit_soft')],
                     [sg.Text('Hard Limit'), sg.Input(key='hard_input'), sg.Text('Current: '), sg.Text(str(data_limits[1]), key='hard_output'), sg.Text('%'), sg.Button('Submit', key='submit_hard')]])

# returns layout of the monitoring window
def get_monitor_window(data_limits, current_value):
    return sg.Window('Monitoring',  [[sg.Text('Watch the current status:')],
                     [sg.Text('Soft Limit: ' + str(data_limits[0]) + '%')],
                     [sg.Text('Hard Limit: ' + str(data_limits[1]) + '%')],
                     [sg.Text('Current Value: '), sg.Text(str(current_value), key='current'), sg.Text('%')]])

# updates soft / hard limit if input is a float between 0 and 100 
def update_limit(limit, window, output):
    if is_float(limit) and is_in_range(float(limit)):
        window[output].update(limit)
    else: 
        sg.Popup('Your input must be a number between 0 and 100.')
        
# checks if given value is a float        
def is_float(n):
    try:
        float(n)
        return True
    except:
        return False  
 
# checks if given value is between 0 and 100
def is_in_range(n):
    return n in range(0, 100)
     
# if soft or hard limit should be updated, this method refreshes the window with the new limits 
def refresh_configuration(window, data_source):
    while True:
        event, values = window.read()
        
        if event in (None, 'Exit'):
            break
        
        elif event == 'submit_soft':
            update_limit(values['soft_input'], window, 'soft_output')
            data_source[0] = values['soft_input']
            window['soft_input'].update('')
        elif event == 'submit_hard':
            update_limit(values['hard_input'], window, 'hard_output')      
            data_source[1] = values['hard_input']
            window['hard_input'].update('')

# refreshes monitoring window every second, so the current value is always up to date
# performs check for excess and triggers log and email function
def refresh_monitoring(window, data_source):
    while True:
        event, values = window.read(timeout = 1)
        if event in (None, 'Exit'):
            break
        MM.get_data()
        MM.check_value(cpu_limits[0], cpu_limits[1], MM.cpu)
        MM.check_value(ram_limits[0], ram_limits[1], MM.ram)
        MM.check_value(disk_limits[0], disk_limits[1], MM.disk_storage)
        window['current'].update(data_source[0])
        tm.sleep(1)       

# creates and opens main window
window = sg.Window('Monitoring', layout)
  
# main loop for main window with actions for the different buttons
while True:
    event, values = window.read()

    if event in (None, 'Exit'):
        break 
    
    elif event == 'cpu_conf':
        conf_window = get_config_window(cpu_limits)
        refresh_configuration(conf_window, cpu_limits)
    elif event == 'ram_conf':
        conf_window = get_config_window(ram_limits)
        refresh_configuration(conf_window, ram_limits)
    elif event == 'disk_conf':
        conf_window = get_config_window(disk_limits)     
        refresh_configuration(conf_window, disk_limits)
    elif event == 'cpu_mon':
        mon_window = get_monitor_window(cpu_limits, MM.cpu[0])
        refresh_monitoring(mon_window, MM.cpu)
    elif event == 'ram_mon':
        mon_window = get_monitor_window(ram_limits, MM.ram[0])
        refresh_monitoring(mon_window, MM.ram)
    elif event == 'disk_mon':
        mon_window = get_monitor_window(disk_limits, MM.disk_storage[0])
        refresh_monitoring(mon_window, MM.disk_storage)          
     
window.close()
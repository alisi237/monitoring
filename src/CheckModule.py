import LoggerModule
import platform
import smtplib, ssl

log_info = "info"
log_warning = "warning"
log_critical = "critical"
port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "systemalert22@gmail.com"
receiver_email = "alinasiol@icloud.com"
password = "Passwort123!"
message = """\
Subject: CRITICAL INCIDENT

One of your data sources exceeded the hard limit. Please see the logs and take action!"""
    

def check_for_excess(soft_limit, hard_limit, value, data_source):
    if value > hard_limit:
        log(value, data_source, log_critical)
        send_email()
    elif value > soft_limit:
        log(value, data_source, log_warning)
    elif value < soft_limit: 
        log(value, data_source, log_info)
    
def log(value, data_source, log_level):
    if log_level == log_critical:
        LoggerModule.logger.critical(str(platform.uname().node) + " - " + data_source + " exceeded the hardlimit with the following value: " +  str(value))
    elif log_level == log_warning:
        LoggerModule.logger.warning(str(platform.uname().node) + " - " + data_source + " exceeded the softlimit with the following value: " +  str(value))
    elif log_level == log_info:
        LoggerModule.logger.info(str(platform.uname().node) + " - " + data_source + " is under the limit: " +  str(value))
    
def send_email():
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

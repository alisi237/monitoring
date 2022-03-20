import smtplib
import ssl
import time
import ExceedanceCheckModule as ECM

# smtp server of gmail is used for mail communication
# port 587 is used for starttls

last_sent = 0

port = 587  
smtp_server = "smtp.gmail.com"
sender_email = "systemalert22@gmail.com"
receiver_email = "alinasiol@icloud.com"
password = "Passwort123!"

# connects via smtp, logs in with given user and sends email if last email was sent 10 minutes+ ago
def send_email(message):
    global last_sent
    if ECM.check_last_executed(last_sent, 600):
        last_sent = time.time()
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  
            server.starttls(context=context)
            server.ehlo() 
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
 

            
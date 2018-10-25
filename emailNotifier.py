import os
import sys
import signal
import time
import datetime
import smtplib

# Properties
sender = "sender@gmail.com" # sender's email address
sender_password = "sender_password" # sender's email account password
recipients = "recipient@gmail.com" # email's recipients (separate addresses with ',')
subject = "Reminder" # email's subject
body = "Drink a glass of water." # email's body
amount = int(10) # amount of emails to be delivered
interval = int(3600) # amount of seconds between every email delivery

def smtp_initialize():
    try:
        global s
        s = smtplib.SMTP_SSL('smtp.gmail.com', 465) # use correct SMTP settings according to sender's email server
        s.ehlo() # greet server (trivial)
    except:
        print("Error: Unable to connect with the SMTP server.")
        end()
    else:
        print("Connection with the SMTP server successful")
        smtp_authenticate()

def smtp_authenticate():
    try:
        s.login(sender, sender_password)
    except:
        print("Error: Unable to authenticate to the SMTP server.")
        end()
    else:
        print("Authentication to the SMTP server successful")
        smtp_sendmail()

def smtp_sendmail():
    global count
    count = 0
    while count < amount:
        try:
            timestamp = str(datetime.datetime.now()) + " : "
            s.sendmail(sender, recipients, 'Subject: {}\n\n{}'.format(subject, timestamp + body))
        except:
            print("Error: unable to send the email.")
            end()
        else:
            count = count + 1
            print("Message sent " + "(" + str(count) + ")")
            for i in range(interval, 0, -1):
                time.sleep(1)
                print(str(i) + " seconds left until next email delivery")
    else:
        end()

def signal_handler(signal, frame):
    print(" ")
    print("Process interrupted by user.")
    end()

def end():
    print("A total of " + str(count) + " email(s) sent")
    s.quit()
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    smtp_initialize()

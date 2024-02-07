# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
msg=MIMEText("")
# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = 'TEST1234' 
msg['From'] = 'alessio.ranalli@asl2abruzzo.it'
msg['To'] = 'stefano.piccoli@asl2abruzzo.it'

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP_SSL('smtpadv.pelconsip.aruba.it')
print("DONE")
s.connect('smtpadv.pelconsip.aruba.it',465)
print("DONE2")
s.login("assistenza.portale@asl2abruzzo.it",password="PORass@30")
print("DONE3")
s.sendmail(msg["From"], msg["To"], msg.as_string())
s.quit()
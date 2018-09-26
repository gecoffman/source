
import sys
sys.path.insert( 0, '/home/ekarg/src' )

import smtplib
from passwords.antiqueEmail import password

from email.mime.text import MIMEText

def sendMail( to, subject, msg ):
	''' Send message from company email address to given address '''
	
	sender = password['username']

	formattedMsg = "\r\n".join([
  	"From:"  + sender,
  	"To:" + to ,
  	"Subject:" + subject,
  	"",
  	msg
  	]) 
	# Send the message via our own SMTP server, but don't include the
	# envelope header.
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(sender,password['password'])
	server.sendmail(sender, [to], msg)
	server.quit()






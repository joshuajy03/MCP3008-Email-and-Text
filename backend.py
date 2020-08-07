from mq import *
import sys, time
import smtplib
import keyboard


# start talking to the SMTP server for Gmail
# now login as my gmail user
username2='joshuajy03@gmail.com'
password2='lpckxwshydaaonvc'

username='joshuayang0303@gmail.com'
password='Sparta2go'

# the email objects
replyto='doNotReply@gmail.com' # where a reply to will go
sendto=['joshuajy03@gmail.com'] # list to send to
sendtoShow='joshuajy03@gmail.com' # what shows on the email as send to
mailtext='From: '+replyto+'\nTo: '+sendtoShow+'\n'
subject='Detected' # subject line

tonumber =' '

maxLPG=40
maxCO=40
maxSMOKE=40
detectLPD=False
detectCO=False
detectSMOKE=False
content="Hello, \n"



carriers = {
	'att': 'mms.att.net',
	'tmobile': '@tmomail.net',
	'verizon': '@vtext.com',
	'sprint': '@page.nextel.com'

}	

def send(message):
	global password
	global username
	global tonumber
	global content
	
	auth = (username,password)
	tonumber ='4089140666{}'.format(carriers['tmobile'])
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login(auth[0], auth[1])
	
	from_mail = username
	to = tonumber
	
	body = content
	message = ("From: %s\r\n" % from_mail + "To: %s\r\n" % to + "Subject: %s\r\n" % 'Danger' + "\r\n" + body)
	
	server.sendmail(auth[0], tonumber, message)
	
	
def detect(perc):
	
	global subject
	global maxLPG
	global maxCO
	global maxSMOKE
	global detectLPD
	global detectCO
	global detectSMOKE
	global content
	
	if perc["GAS_LPG"] == -1 or perc["CO"] == -1 or perc["SMOKE"] == -1:
		sendemail()
	elif perc["GAS_LPG"] > maxLPG or perc["CO"] > maxCO or perc["SMOKE"] > maxSMOKE:
		if perc["GAS_LPG"] > maxLPG:
			detectLPG=True
			subject += 'Toxic Natural Gas'
			content += "Toxic Natural Gas has reached dangerous levels."
		elif perc["CO"] > maxCO:
			detectCO=True
			subject += 'Carbon Monoxide'
			content += "Carbon Monoxide has reached dangerous levels."
		elif perc["SMOKE"] > maxSMOKE:
			detectSMOKE=True
			subject += 'Smoke'
			content += "Smoke has reached dangerous levels."
		sendemail()
        
def sendemail():
	global username2
	global password2
	global replyto
	
	global sendto
	global sendtoShow
	global mailtext
	global content
	global subject
	global tonumber
	
	
	s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	s.ehlo()
	s.login(username2,password2)
	content += "has been detected. Please contact the fire department and/or gas company to inform them of the problem. "
	mailtext=mailtext+'Subject:'+subject+'\n'+content
	# send the email
	s.sendmail(replyto, sendto, mailtext)
	mailtext='From: '+replyto+'\nTo: '+sendtoShow+'\n'
	subject='Detected'
	
	# we're done
	# print the result
	print('Sendmail')
	
	send(content)
	
	content="Hello, \n"
	time.sleep(30 )
    

print("Press CTRL+C to abort.")
previous1 = 0
previous2 = 0
previous3 = 0
first = True
mq = MQ();

try:
	while True:
		try:
			perc = mq.MQPercentage()
		finally:
			sys.stdout.write('e')
			
		try:
                    if keyboard.is_pressed('q'):
                        print('hi')
                        sendemail()
                except:
                    sys.stdout.write('Press q to Quit')
		sys.stdout.write("\r")
		sys.stdout.write("\033[K")
		sys.stdout.write("LPG: %g ppm, CO: %g ppm, Smoke: %g ppm" % (perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
		sys.stdout.flush()
		detect(perc)
		previous1 = perc["GAS_LPG"]
		previous2 = perc["CO"]
		previous3 = perc["SMOKE"]
		first = False
		time.sleep(0.1)

finally:
	print("\nAbort by user")
	

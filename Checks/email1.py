import re
import smtplib
from smtplib import SMTP
import dns.resolver
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Address used for SMTP MAIL FROM command
fromAddress = 'max.bahdanovich@gmail.com'

# Simple Regex for syntax checking
'''regex = '^[a-z]+(\.[_a-z0-9-]+)*@college.harvard.edu'

# Email address to verify
inputAddress = input('Please enter the email Address to verify: ')
addressToVerify = str(inputAddress)

# Syntax check
match = re.match(regex, addressToVerify)
if match == None:
	print('Bad Syntax')
	raise ValueError('Bad Syntax')'''




# Get domain for DNS lookup
'''splitAddress = addressToVerify.split('@')
domain = str(splitAddress[1])
print('Domain:', domain)'''


msg = MIMEMultipart()
msg['From'] = 'max.bahdanovich@gmail.com'
msg['To'] = 'bahdanovich@college.harvard.edu'
msg['Subject'] = 'simple email in python'
message = 'here is the email'
msg.attach(MIMEText(message))

mailserver = smtplib.SMTP('smtp.gmail.com',587)
# identify ourselves to smtp gmail client
mailserver.ehlo()
# secure our email with tls encryption
mailserver.starttls()
# re-identify ourselves as an encrypted connection
mailserver.ehlo()
mailserver.login('iceberg.friends@gmail.com', '12345678ice')

mailserver.sendmail('iceberg.friends@gmail.com','bahdanovich@college.harvard.edu', message)

mailserver.quit()

# MX record lookup
records = dns.resolver.query(domain, 'MX')
mxRecord = records[0].exchange
mxRecord = str(mxRecord)


# SMTP lib setup (use debug level for full output)
server = smtplib.SMTP()
server.set_debuglevel(0)

# SMTP Conversation
server.connect(mxRecord)
server.helo(server.local_hostname) ### server.local_hostname(Get local server hostname)
server.mail(fromAddress)
code, message = server.rcpt(str(addressToVerify))
server.quit()

print(code)
print(message)

# Assume SMTP response 250 is success
if code == 250:
	print('Success')

else:
	print('Bad')

	# ttps://stackoverflow.com/questions/32056109/importerror-cannot-import-name-smtp-ssl
	# https://github.com/scottbrady91/Python-Email-Verification-Script/blob/master/src/VerifyEmailAddress.py
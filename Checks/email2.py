import smtplib

to = 'bahdanovich@college.harvard.edu'
gmail_user = 'iceberg.friends@gmail.com'
gmail_pwd = '12345678ice'
smtpserver = smtplib.SMTP("smtp.gmail.com",587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo() # extra characters to permit edit
smtpserver.login(gmail_user, gmail_pwd)
header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:testing \n'
print(header)
msg = header + '\n Your access code for Iceberg is: \n\n'
smtpserver.sendmail(gmail_user, to, msg)
print('done!')
smtpserver.quit()
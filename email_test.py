from email.message import EmailMessage
import smtplib
import ssl
email_sender = 'jploveslego101@gmail.com'
email_password = 'app password'
email_receiver = 'joshpeyton04@gmail.com'
s = "Wow, this works"
subject = 'Rain Prediction For The Next Hour'
body = s

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())

#password wrgl awoa mxvk vxkg

from django.db import models
import smtplib
from quote.views import *
from quote.models import *
from django.contrib.auth.models import User

# Create your models here.
class SignUpNotify(models.Model):
    EMAIL = ''
    
   # getting email address of users with registered queries
   #identifying chnages in query values
    def sendmail():
        querySet = Query.objects.filter(isRegistered__exact=True)
        for query in querySet:
            newResult = search(query.queryStr)
            oldResult = query.QueryResult
            if newResult != oldResult:
               u = query.user
               text = newResult
               sendToOneAddress(u.email, text)
     
        u = user.request
        SignUpNotify.EMAIL = u.email

    #sending notifications via a gmial account to users
    def sendToOneAddress(email_addr, text):
    
        TO = email_addr
        SUBJECT  = 'Updated Changes on Your Query'
        TEXT = text
       #email credentials
        email_sender = 'ist510sp14@gmail.com'
        email_passw = 'IST510sp'

        #creates connection to the sender's email server
        server = smtplib.SMTP ('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo
        server.login(email_sender, email_passw)

        BODY = '\r\n'.join([
                'To: %s' % TO,
                'From: %s' % email_sender,
                'Subject: %s' % SUBJECT,
                '' ,
                TEXT
                 ])
        try:
             server.sendmail(email_sender, [TO], BODY)
             print ('email sent')
        except:
               print ('error sending email')
	
        server.quit()  
  
  

    

    
    
   
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imaplib
import email
import time




csv_file = 'memail.csv'  
df = pd.read_csv(csv_file)

# print(df)

smtp_server = 'smtp.gmail.com'
smtp_port = 587  # SMTP port (e.g., 587 for TLS, 465 for SSL)
smtp_username = 'bhavyasrivastava012@gmail.com'  
smtp_password = 'hfbb nnsh fmlg fafq'  

#Function to send  the first mail
def sendmail_first(to_email,name):
  subject = f"{name} Hello Test Script"
  body = f"Hey {name},👋\n\nOver the past couple of years of my growth hacking experience, I've realised that there is an ever-growing and constant need for growing a secure business that gets repeat business. 💰.\n\nAt Idea Usher, We reduced operations cost by 45% for our fortune 500 clients like Gold's Gym, BuzzTime, Honda, with increased customer engagement. 📈\n\nWould you oppose listening to ideas on augmenting this for your business growth over lunch?\n\nP. S. - I'm willing to bribe you over my treat in case we connect!!"
    

  message = MIMEMultipart()
  message['From'] = smtp_username
  message['To'] = to_email
  message['Subject'] = subject
  message.attach(MIMEText(body, 'plain'))

    
  try:
      server = smtplib.SMTP(smtp_server, smtp_port)
      server.starttls()  
      server.login(smtp_username, smtp_password)

   
      server.sendmail(smtp_username, to_email, message.as_string())
      print(f"Email sent to {to_email}")
      server.quit()
  except Exception as e:
      print(f"Failed to send email to {to_email}: {str(e)}")


  attempt=1
  print(f"Attempt no. {attempt}")

#Function to send  the second mail
def sendmail_second(to_email,name):
  
  subject = f"{name} Hello Test Script"
  body = f"Hey {name},👋\n\nOver the past couple of years of my growth hacking experience, I've realised that there is an ever-growing and constant need for growing a secure business that gets repeat business. 💰.\n\nAt Idea Usher, We reduced operations cost by 45% for our fortune 500 clients like Gold's Gym, BuzzTime, Honda, with increased customer engagement. 📈\n\nWould you oppose listening to ideas on augmenting this for your business growth over lunch?\n\nP. S. - I'm willing to bribe you over my treat in case we connect!!"
    

  message = MIMEMultipart()
  message['From'] = smtp_username
  message['To'] = to_email
  message['Subject'] = subject
  message.attach(MIMEText(body, 'plain'))

    
  try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  
    server.login(smtp_username, smtp_password)

   
    server.sendmail(smtp_username, to_email, message.as_string())
    print(f"Email sent to {to_email}")
    server.quit()
  except Exception as e:
    print(f"Failed to send email to {to_email}: {str(e)}")

  attempt=2
  print(f"Attempt no. {attempt}")

#Funtion to send the third mail
def sendmail_third(to_email,name):
  subject = f"{name} Hello Test Script"
  body = f"Hey {name},👋\n\nOver the past couple of years of my growth hacking experience, I've realised that there is an ever-growing and constant need for growing a secure business that gets repeat business. 💰.\n\nAt Idea Usher, We reduced operations cost by 45% for our fortune 500 clients like Gold's Gym, BuzzTime, Honda, with increased customer engagement. 📈\n\nWould you oppose listening to ideas on augmenting this for your business growth over lunch?\n\nP. S. - I'm willing to bribe you over my treat in case we connect!!"
    

  message = MIMEMultipart()
  message['From'] = smtp_username
  message['To'] = to_email
  message['Subject'] = subject
  message.attach(MIMEText(body, 'plain'))

    
  try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  
    server.login(smtp_username, smtp_password)

   
    server.sendmail(smtp_username, to_email, message.as_string())
    print(f"Email sent to {to_email}")
    server.quit()
  except Exception as e:
    print(f"Failed to send email to {to_email}: {str(e)}")

  attempt=3
  print(f"Attempt no. {attempt}")

imap_server="imap.gmail.com"
mail = imaplib.IMAP4_SSL(imap_server)
mail.login(smtp_username,smtp_password)
mail.select("Inbox")

#Function to check if replied.
def check_response(name,email_search):
   response_list = []  # Create a list to store response content for all emails
   search_criteria = f'FROM "{email_search}"'
   print(search_criteria)
    
   result, email_ids = mail.search(None, search_criteria)
   print(email_ids)
    
   for email_id in email_ids[0].split():
       result, data = mail.fetch(email_id, "(RFC822)")
       msg = email.message_from_bytes(data[0][1])
    
       if msg.is_multipart():
           for part in msg.walk():
               if part.get_content_type() == "text/plain":
                   response_content = part.get_payload(decode=True).decode("utf-8")
                   payload = part.get_payload(decode=True)
                   if payload is not None:
                       response_content = payload.decode("utf-8")
                       print("Received response for", email_search, ":", response_content)
                       response_list.append(response_content)  # Append to the response list
                       break
       else:
           payload = msg.get_payload(decode=True)
           if payload is not None:
               response_content = payload.decode("utf-8")
               print("Received response for", email_search, ":", response_content)
               response_list.append(response_content)  # Append to the response list
   mail.logout() 
   return response_list


 # Check responses
# response = check_response()
# print(response)

#all functions take the same two parameter mail and name

for index, row in df.iterrows():
      to_email = row['Email']
      name=row['Name']

      sendmail_first(to_email,name)

      time.sleep(3 * 24 * 60 * 60) #3 days

      response= check_response(name,to_email)

      if response:
          print(response)
          break
      else:
          sendmail_second(to_email,name)

      time.sleep(3 * 24 * 60 * 60)

      response=check_response(to_email,name)

      if response:
          print(response)
          break
      else:
          sendmail_third(to_email,name)
      




        
      

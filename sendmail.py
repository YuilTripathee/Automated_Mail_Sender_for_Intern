import os
import json 
from datetime import date

# custom library (downloaded from pip) to mask password inputs
import stdiomask

# Import smtplib for the actual sending function
import smtplib

# For guessing MIME type
import mimetypes

# Import the email modules we'll need
import email
import email.mime.application
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

if __name__ == "__main__":

    # open JSON file to get the sender's data
    with open('config/sender.json', 'r', encoding='utf-8') as sender_fp:
        sender = json.load(sender_fp)
        print(sender)
        chk_sender = input("Is the given sender information correct? ")
        if chk_sender == 'y':
            pass
        else:
            sender_name = input("Enter the sender's name: ")
            sender_email = input("Enter the sender's email: ")
            sender = {"name" : sender_name, "email" : sender_email}
        sender_fp.close()
    
    # open JSON file to get the recipent's data
    with open('config/recipent.json', 'r', encoding='utf-8') as recipent_fp:
        recipent = json.load(recipent_fp)
        print(recipent)
        chk_recp = input("Is the given recipent's information correct? ")
        if chk_recp == 'y':
            pass
        else:
            recp_name = input("Enter the recipent's name: ")
            recp_email = input("Enter the recipent's email: ")
            recipent = {"name" : recp_name, "email" : recp_email}
        recipent_fp.close()
    
    # open JSON file to get the CC's list and embed CC list to mail header
    with open('config/cc_list.json', 'r', encoding='utf-8') as cc_list_fp:
        cc_list = json.load(cc_list_fp)
        if cc_list != []:
            cc_list_string = ""
            # converting to MIME usable format
            for data in cc_list:
                cc_list_string += data["name"] + " <" + data["email"] + ", "
            msg['CC'] = cc_list_string
        print(cc_list)
        chk_cc = input("Is the given cc list information correct? ")
        if chk_cc == 'y':
            pass
        else:
            cc_list == []
        cc_list_fp.close()

    # Initializing mail headers
    msg = MIMEMultipart()
    msg['From'] = sender["name"] + " <" + sender["email"] + ">"
    msg['To'] = recipent["name"] + " <" + recipent["email"] + ">"
    # msg['CC'] = cc_list_string
    # For date of update
    dateToday = date.today()
    dateStr = str(dateToday.month)+ "/" + str(dateToday.day) + "/" + str(dateToday.year)
    msg['Subject'] = "Intern: Status Update: " + dateStr

    # run html_mail_writer.py to write HTML mail into a file (saving is done for backup purposes)
    # i.e. run other python file within the python file
    os.system('python3 html_mail_writer.py')

    # importing HTML page for mail
    with open('mail/mail.html', 'r', encoding='utf-8') as mailPage_fp:
        mail_page = mailPage_fp.read().replace('\n', '')
        mailPage_fp.close()

    # embedding HTML file into the mail
    mail_html_content = MIMEText(mail_page, 'html')
    msg.attach(mail_html_content)

    # sample footer text
    # text = """This email is sent from Yuil Tripathee
    # Software Engineer Intern at Dynamics Softech Computer Solutions.
    # """
    # txt = MIMEText(text, 'plain')
    # msg.attach(txt)

    # Embedding images into the mail
    # Getting the list of paths for the image in snapshots folder
    files = []
    # folders = []
        # folders.extend(os.path.join(path, name) for name in dirnames)
    for (path, dirnames, filenames) in os.walk('snapshots'):
        files.extend(os.path.join(path, name) for name in filenames)

    
    for imge_ci in range(0, len(files)):
        image_ci = str(imge_ci + 1)
        img_fp = open(files[imge_ci], 'rb')
        msgImage = MIMEImage(img_fp.read())
        img_fp.close()
        image_value = "<image" + image_ci + ">"
        msgImage.add_header('Content-ID', image_value)
        msg.attach(msgImage)

    # Firing up the mail engine
    try:
        with smtplib.SMTP('smtp.gmail.com:587') as mail_sys:
            mail_sys.ehlo()
            mail_sys.starttls()
            print("Yuil, you have to provide your e-mail password in order to login to SMTP.")
            password = stdiomask.getpass()
            mail_sys.login(sender["email"],password)
            print("Logged in sucessfully!")
            print("Sending mail...")
            mail_sys.sendmail(sender["email"],[recipent["email"]], msg.as_string())
            print('Mail sent sucessfully')
            pass
    except Exception:
        print('Mail failed to transfer')
        raise
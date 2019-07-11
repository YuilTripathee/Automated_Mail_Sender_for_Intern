# extended version of mail sender bot

import os
import json
from datetime import date
import socket

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
from email.mime.application import MIMEApplication

# method for sending mail in MIME format
def send_mail(sender, recipent, msg):
    try:
        with smtplib.SMTP('smtp.gmail.com:587') as mail_sys:
            mail_sys.ehlo()
            print("Established SMTP connection with the mail server!")
            mail_sys.starttls()
            print("TLS connection established!")
            print(
                "Yuil, you have to provide your e-mail password in order to login to SMTP.")
            password = stdiomask.getpass()
            mail_sys.login(sender, password)
            print("Logged in sucessfully!")
            print("Sending mail...")
            mail_sys.sendmail(sender,
                              recipent, msg.as_string())
            print('Mail sent sucessfully')
            pass
    except smtplib.SMTPAuthenticationError:
        print("\nUsername or password may be invalid.")
        send_mail(sender, recipent, msg)
    except socket.gaierror:
        print("\nConnectivity Problem.")
    except Exception:
        print('Mail failed to transfer')
        raise

if __name__ == "__main__":

    print("\n[sendmail.py]\n")

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
            sender = {"name": sender_name, "email": sender_email}
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
            recipent = {"name": recp_name, "email": recp_email}
        recipent_fp.close()

    # start to compile mail
    msg = MIMEMultipart()

    # open JSON file to get the CC's list and embed CC list to mail header
    with open('config/cc_list.json', 'r', encoding='utf-8') as cc_list_fp:
        cc_list = json.load(cc_list_fp)
        if cc_list != []:
            cc_list_string = ""
            # converting to MIME usable format
            for data in cc_list:
                cc_list_string += data["name"] + " <" + data["email"] + ">, "
        print(cc_list)
        chk_cc = input("Is the given cc list information correct? ")
        if chk_cc == 'y':
            msg['CC'] = cc_list_string
        else:
            cc_list == []
        cc_list_fp.close()

    # Initializing mail headers
    msg['From'] = sender["name"] + " <" + sender["email"] + ">"
    msg['To'] = recipent["name"] + " <" + recipent["email"] + ">"
    # msg['CC'] = cc_list_string
    # For title of the mail
    with open('message/title.json', 'r', encoding='utf-8') as title_fp:
        title_list = json.load(title_fp)
        title_fp.close()

    print("\nAvailable titles:")
    print("=================")
    # List of titles (numbered)
    for t_i in range(0, len(title_list)):
        print(str(t_i) + ": " + title_list[t_i]["text"])

    title_prompt1 = input(
    "\nWould you choose to use title from template or write on your own? [y/n]\n")
    # if you consider using the predefined template
    if title_prompt1 == 'y':
        title_id = int(input("\nEnter the title id: "))
        mail_title = title_list[title_id]["text"]
    else:
        mail_title = input("Enter your own title: ")
        if mail_title == '':
            mail_title = 'Status Update'

    # For date of update
    dateToday = date.today()
    dateStr = str(dateToday.month) + "/" + \
        str(dateToday.day) + "/" + str(dateToday.year)
    msg['Subject'] = mail_title + ": " + dateStr

    print("Writing your email!")
    # run html_mail_writer.py to write HTML mail into a file (saving is done for backup purposes)
    # i.e. run other python file within the python file
    mail_writer = 'python3 html_mail_writer.py "%s"' % mail_title
    os.system(mail_writer)

    # importing HTML page for mail
    with open('mail/mail.html', 'r', encoding='utf-8') as mailPage_fp:
        mail_page = mailPage_fp.read().replace('\n', '')
        mailPage_fp.close()

    # embedding HTML file into the mail
    mail_html_content = MIMEText(mail_page, 'html')
    msg.attach(mail_html_content)

    # Code for normal MIME text (unused)
    '''
        text = """This email is sent from Yuil Tripathee
        Software Engineer Intern at Dynamics Softech Computer Solutions.
        """
        txt = MIMEText(text, 'plain')
        msg.attach(txt) 
    '''

    # Embedding images into the mail
    # Getting the list of paths for the image in snapshots folder
    files = []
    print("\nInserting images:")
    print("=================")
    # folders = []
    # folders.extend(os.path.join(path, name) for name in dirnames)
    for (path, dirnames, filenames) in os.walk('snapshots'):
        files.extend(os.path.join(path, name) for name in filenames)
    # writing each image file into mail page
    for imge_ci in range(0, len(files)):
        image_ci = str(imge_ci + 1) # special numbering for content id in HTML page image cid
        img_fp = open(files[imge_ci], 'rb') # image file binary for network stream
        img_filename = os.path.basename(files[imge_ci]) # file name of the particular image file
        msgImage = MIMEImage(img_fp.read(), img_filename) # encoding image into MIME format
        img_fp.close()
        image_value = "<image" + image_ci + ">"
        msgImage.add_header('Content-ID', image_value) # MIME header for Content-ID
        msgImage.add_header('Content-Disposition', # MIME header for Content-Disposition
                            'inline', filename=img_filename)
        msg.attach(msgImage) # attaching image to the main MIME email object
        print("Image inserted: " + files[imge_ci])

    # Inserting mail attachments
    attaches = []
    print("\nAttaching files:")
    print("================")
    # Getting down the list
    for (path, dirnames, filenames) in os.walk('attachments'):
        attaches.extend(os.path.join(path, name) for name in filenames)
    # Attaching files into the Mail
    for attach_ci in range(0, len(attaches)):
        # file path for the file to be attached
        attach_file = attaches[attach_ci]
        attach_file_fp = open(attach_file, 'rb')  # file binary to be attached
        # file name of the file to be attached
        attFileName = os.path.basename(attach_file)
        # encoding file for attachment
        attFile = MIMEApplication(attach_file_fp.read(), Name=attFileName)
        attach_file_fp.close()  # closing the file pointer
        attFile.add_header('Content-Disposition', 'attachment',
                           filename=attFileName)  # adding the attachment file
        msg.attach(attFile)
        print("File attached: " + attach_file)

    # Firing up the mail engine
    print("\nSending mail...")
    send_mail(sender["email"], recipent["email"], msg)
    return_string = input("Press any key to continue")

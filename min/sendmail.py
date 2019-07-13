# minified version of mail sender bot

import os
import sys
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

# import custom written html mail writer
import html_mail_writer as hwriter
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..'))) # for importing file for parent directory (up A level directory)
import mail_util # mail utility scripts

if __name__ == "__main__":
    
    mail_util.hello(__file__, bot_type='min')

    # open the template file
    with open('min/data/main.json', 'r', encoding='utf-8') as data_fp: # top level invoking requires locating file from the shell's localtion (i.e. project directory)
        data = json.load(data_fp)
        data_fp.close()

    # selecting data template
    print("\nAvailable templates:")
    print("====================")
    for c_i in range(0, len(data)):
        print(str(c_i) + ": " + data[c_i]["ref"])
    
    # getting and validating data reference from JSON array
    try:
        data_id = int(input("\nEnter the data 'id' for the required format: "))
        dataset = data[data_id]
        print(dataset["ref"])
        print("Data id: " + str(data_id) + " is available.")
    except ValueError: # still one chance for correction
        data_id = int(input("\nEnter the data 'id' for the required format: "))
        dataset = data[data_id]
        print(dataset["ref"])
        print("Data id: " + str(data_id) + " is available.")
    except Exception:
        raise

    # start to compile mail
    msg = MIMEMultipart()

    # Initializing mail headers
    msg["From"] = dataset["sender"]["name"] + " <" + dataset["sender"]["email"] + ">"
    msg['To'] = dataset["recipent"]["name"] + " <" + dataset["recipent"]["email"] + ">"

    # embedding CC list to mail header
    cc_list = dataset["cc"]
    if cc_list != []:
        cc_list_string = ""
        # converting CC data to MIME usable format
        for cc_unit in cc_list:
            cc_list_string += cc_unit["name"] + " <" + cc_unit["email"] + ">, "
        msg['CC'] = cc_list_string
    else:
        cc_list == []

    # inserting mail subject
    mail_title = dataset["message"]["title"]
    dateToday = date.today() # for date of update mail sent
    msg['Subject'] = mail_title + ": " + str(dateToday.month) + "/" + \
        str(dateToday.day) + "/" + str(dateToday.year)
    
    print("Headers initialized sucessfully")
    print("Writing your email!")
    # run html_mail_writer.py to write HTML mail into a file (saving is done for backup purposes)
    mail_page = hwriter.write_mail(dataset["message"])

    # # importing HTML page for mail
    # with open('mail/min.html', 'r', encoding='utf-8') as mailPage_fp:
    #     mail_page = mailPage_fp.read().replace('\n', '')
    #     mailPage_fp.close()
    
    # embedding HTML file into the mail
    mail_html_content = MIMEText(mail_page, 'html')
    msg.attach(mail_html_content)

    # Embedding images into the mail
    # Getting the list of paths for the image in snapshots folder
    files = []
    print("\nInserting images:")
    print("=================")
    
    # accessing files and appending into file list
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
    mail_util.send_mail(dataset['sender']['email'], dataset['recipent']['email'], msg)
    return_string = input("Press any key to continue")

    
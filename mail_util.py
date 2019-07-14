# Utilities scripts for mailer bot

import time
import socket
import os
import shutil
import json
import smtplib
from datetime import datetime
from pathlib import Path

# custom library (downloaded from pip) to mask password inputs
import stdiomask

# Common components for all scripts
# identifier for which python script is being executed


# takes filename and bot_type and prints which script is being executed
def hello(file_name, bot_type='ext'):
    if bot_type == 'min':
        print('\n[min: ' + file_name + ']\n')
    elif bot_type == 'ext':
        print('\n[ext: ' + file_name + ']\n')
    else:
        print("Invalid parameter passed to the method hello() in mail_util.py")

# Common components for html mail writer script


def hold_file_import():  # holds files import for confirmation before file's going to be attached
    print("\nWarning!")
    print("Please check if files to be imported are set correctly. These file include attachments and snapshots.")
    return input("If confirmed, press any key to continue...")


# function to take week number to return week day (starting Monday as 0)
def get_week_name(week_number):
    if week_number == 0:
        week_name = "Monday"
    elif week_number == 1:
        week_name = "Tuesday"
    elif week_number == 2:
        week_name = "Wednesday"
    elif week_number == 3:
        week_name = "Thursday"
    elif week_number == 4:
        week_name = "Friday"
    elif week_number == 5:
        week_name = "Saturday"
    elif week_number == 6:
        week_name = "Sunday"
    else:
        week_name = "Invalid weekday() input"
    return week_name

# Common components for mail sender script


def send_mail(sender, recipent, msg, bot_type='ext'):  # method for sending mail in MIME format
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
    except smtplib.SMTPAuthenticationError:
        print("\nUsername or password may be invalid.")
        send_mail(sender, recipent, msg)
    except socket.gaierror:
        print("\nConnectivity Problem.")
    except Exception:
        print('Mail failed to transfer')
        raise
    finally:
        print('Mail sent sucessfully')


# updates stats of mail sent using the bot for analytics purposes
def update_stats(mail_time, msg, bot_type='ext'):
    # selects stats file
    if bot_type == 'min':
        stats_file_addr = 'min/data/stats.json'
    elif bot_type == 'ext':
        stats_file_addr = 'stats.json'
    else:
        print("Invalid bot variant parameter passed to the stats updater function.")
        return
    # attempts update for stats
    try:
        # loads the stats
        with open(stats_file_addr, 'r', encoding='utf-8') as fp:
            stats_data = json.load(fp)
            fp.close()
        stats_data["count"] = len(stats_data["log"]) + 1
        stats_data["log"].append({
            "timestamp": mail_time,
            "title": msg["Subject"],
            "sender": msg["From"],
            "recipent": msg["To"],
            "cc": msg["CC"]
        })
        # write into file with new stats
        with open(stats_file_addr, 'w', encoding='utf-8') as fp:
            json.dump(stats_data, fp, indent=4)
    except Exception:
        raise
    finally:
        print("Stats updated.")
        fp.close()


# disposes files into other directory and clean the staging area for snapshots and attachments
def clean_files(snapshots=None, attachments=None):
    try:
        if snapshots != None:
            move_file('archive/snapshots', snapshots)
        if attachments != None:
            move_file('archive/attachments', attachments)
    finally:
        print("Files cleaned.")

# add-on for file cleaner (to move file)


def move_file(target_directory, files):
    target_folder = os.path.join(target_directory, str(
        datetime.now().strftime("%Y-%m-%d")))
    # create a folder if not exists (snapshots or attachments)
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    for file in files:
        src = file
        destination = os.path.join(target_folder, os.path.basename(file))
        shutil.move(src, destination)

    # Note: Use cleaner apart from send_mail()

# extension for html_mail_writer.py to render highlights contents based on snapshot filename


def render_img_highlights(files):
    highlights = """"""
    highlights_part1 = """
    <h4> Highlights </h4>
    <ul>
    """
    highlights += highlights_part1
    for file in files:
        filename = Path(file).stem # gets filename
        highlights_content = """
        <li>%s</li>
        """ % filename # builds list
        highlights += highlights_content
    highlights_part2 = """
    </ul>
    """
    highlights += highlights_part2
    return highlights # return whole string


'''
1. Auto content generation (based on snapshot)

Algorithm:
1. Get the snapshot index earlier (before embedding snapshot)
2. Generate rendering from template.
    a. For each file: slice out the filename.
    b. Generate the list
3. Return multi line template.

Task:
1. Add utility function
2. Modify mailer bot to adapt this feature. [load files by initials]

In mail_util.py:
get_snap_highlights(list_type, list) => multi line template

list_type: snapshot, file attachment [still attachment has no meaning]
list: list of files (array of file location)

Future version: Image Recognition
'''

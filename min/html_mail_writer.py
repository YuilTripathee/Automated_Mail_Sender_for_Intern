# minified version of html_mail_writer.py, support script for mail sender bot

import os
import time
from datetime import date

import sys
from os.path import dirname, join, abspath
# for importing file for parent directory (up A level directory)
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
import mail_util # mail utility scripts

# mail writer function
def write_mail(message):
    mail_util.hello(__file__,bot_type='min')  # notifies initiation of mail writer script (bot engine)

    # empty mail page container
    mail_html_page = """"""
    # initial part of mail page
    html_page_part1 = """
        <!DOCTYPE html>
        <html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
        <head>
            <meta charset="utf-8"> <!-- utf-8 works for most cases -->
            <meta name="viewport" content="width=device-width"> <!-- Forcing initial-scale shouldn't be necessary -->
            <meta http-equiv="X-UA-Compatible" content="IE=edge"> <!-- Use the latest (edge) version of IE rendering engine -->
            <meta name="x-apple-disable-message-reformatting">  <!-- Disable auto-scale in iOS 10 Mail entirely -->
            <title>""" + message["title"] + """</title> <!-- The title tag shows in email notifications, like Android 4.4. -->

        </head>

        <body width="100%" style="margin: 0; padding: 0 !important; font-family: 'Courier New', Courier, monospace, sans-serif;">
            <center style="width: 100%;">
            <div style="display: none; font-size: 1px;max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; mso-hide: all; font-family: sans-serif;">
            &zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;
            </div>
            <div style="max-width: 600px; margin: 0 auto;">
                <!-- BEGIN BODY -->
            <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: auto;">
                <tr>
                    <td>
                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                        <tr>
                            <td>
                                <div style="padding: 0 30px;">
                                <h2 style="text-align: center;">""" + message['title'] + """</h2>
                                <p>Hi,</p>
                                <p>
    """

    # Adding initial part into the mail page
    mail_html_page += html_page_part1  # initial section

    # Adding message into the mail page
    mail_html_page += message["message"]

    # If you consider adding up extra text after a template (or either without using it.)
    add_para_prompt = input(
        "Do you need to add extra text other than tempate? [y/n]\n")
    if add_para_prompt == 'y':
        # like <b> for bold, <i> for italics and so on
        print("\nFeel comfortable writing text in HTML format:")
        print("===============================================\n")
        add_contents = []
        while True:
            line = input()
            if line == '':
                break
            add_contents.append(line)
        add_content_para = "<p>" + '<br>'.join(add_contents) + "</p>"
        mail_html_page += add_content_para
    # If you consider not writing additional texts...
    else:
        pass

    # For date of update
    dateToday = date.today()
    dateStr = "<b>" + str(dateToday.month) + "/" + str(dateToday.day) + "/" + str(dateToday.year) + " " + \
        mail_util.get_week_name(dateToday.weekday()) + "</b><br>Time: <b>" + \
        time.strftime("%I:%M %p %z") + "</b>"
    mail_html_page += "<p> Date: " + dateStr + "</p>"

    # container for embedding images
    mail_util.hold_file_import() # for last file attachment confirmation
    files = []
    for (path, dirnames, filenames) in os.walk('snapshots'):
        files.extend(os.path.join(path, name) for name in filenames)
    print("\nEmbedding image reference...")
    if len(files) != 0:
        mail_html_page += mail_util.render_img_highlights(files)
        print("Highlights rendered sucessfully.")
        mail_html_page += "<h3> Some snapshots </h3>"
    for img_ci in range(0, len(files)):
        image_ci = img_ci + 1
        mail_html_page += '<p><img src="cid:image' + \
            str(image_ci) + '" alt="Snapshot" style="max-width: 100%;"><br><i>' + \
            files[img_ci] + '</i></p>'
        print("<image:" + str(image_ci) + "> :"+files[img_ci])
    print("\nImage reference added sucessfully!")
    # footer part of the html mail page
    html_page_part2 = """</p>
                        </div>                       
                      </td>
                    </tr><!-- end: tr -->

                  </table>

                </td>
              </tr><!-- end:tr -->
            <!-- 1 Column Text + Button : END -->
            </table>
            <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: auto; padding: 0 30px;">
              <tr>
                <td valign="middle">
                  <table>
                    <tr>
                      <td valign="top" style="padding-top: 20px;">
                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                          <tr>
                            <td style="text-align: left; padding-right: 10px;">
                              <h3>About</h3>
                              <p>""" + message["about"] + """</p><p><b>Thanks for watching</b></p>
                            </td>
                          </tr>
                        </table>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr><!-- end: tr -->
              
            </table>
            <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: auto; padding: 0 30px;">
              <tr>
                <td valign="middle">
                  <table>
                    <tr>
                      
                      <td valign="top" style="padding-top: 20px;">
                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                          <tr>
                            <td style="text-align: left; padding-left: 5px; padding-right: 5px;">
                              <h3>Contact Info</h3>
                              <img src="https://media.licdn.com/dms/image/C5103AQGPnRGooXJusQ/profile-displayphoto-shrink_800_800/0?e=1564617600&v=beta&t=YTb3XoDzPtnIPOgrOaqJZEYxWBTGxZ3RZF2eaaXhgVc" width="128px" alt="mypicture" style="border-radius: 10px;">
                              <ul>
                                <li><span>Yuil Tripathee <i>@YuilTripathee</i></span></li>
                                <li><span>yuiltripathee79@gmail.com</span></li>
                                <li><span>+977 (982)5158989</span></a></li>
                              </ul>
                            </td>
                          </tr>
                        </table>
                      </td>
                      
                    </tr>
                  </table>
                </td>
              </tr><!-- end: tr -->
              
            </table>
            <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: auto; padding: 0 30px;">
              <tr>
                <td valign="middle">
                  <table>
                    <tr>
                      <td valign="top" style="padding-top: 20px;">
                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                          <tr>
                            <td style="text-align: left; padding-left: 10px;">
                              <h3>Useful Links</h3>
                              <p align="center"><a href="https://yuiltripathee.github.io/">Website</a>&nbsp; <a href="https://github.com/YuilTripathee">GitHub</a>&nbsp; <a href="https://www.linkedin.com/in/yuiltr/">LinkedIn</a>
                              </p>
                            </td>
                          </tr>
                        </table>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr><!-- end: tr -->
              
            </table>
          </div>
        </center>
      </body>
      </html>
    """
    mail_html_page += html_page_part2

    # writing entire template into a file
    # will keep this feature for testing reasons only
    # with open('mail/min.html', 'w', encoding="utf-8") as mail_page_fp:
    #     mail_page_fp.write(mail_html_page)
    #     mail_page_fp.close()

    print("\nMail page written sucessfully!")
    return mail_html_page

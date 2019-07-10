import os
import time
import json
import sys
from datetime import date

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


# mail function
if __name__ == "__main__":

    print("\n[html_mail_writer.py]\n")
    # empty mail page container
    mail_html_page = """"""
    html_page_title = sys.argv[1]
    # initial part of mail page
    html_page_part1 = """
        <!DOCTYPE html>
        <html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
        <head>
            <meta charset="utf-8"> <!-- utf-8 works for most cases -->
            <meta name="viewport" content="width=device-width"> <!-- Forcing initial-scale shouldn't be necessary -->
            <meta http-equiv="X-UA-Compatible" content="IE=edge"> <!-- Use the latest (edge) version of IE rendering engine -->
            <meta name="x-apple-disable-message-reformatting">  <!-- Disable auto-scale in iOS 10 Mail entirely -->
            <title>"""

    html_page_part2 = """</title> <!-- The title tag shows in email notifications, like Android 4.4. -->

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
                                <h2 style="text-align: center;">Intern: status update</h2>
                                <p>Hi,</p>
                                <p>
    """

    # Adding initial part into the mail page
    mail_html_page += html_page_part1
    mail_html_page += html_page_title
    mail_html_page += html_page_part2

    # Adding message into the mail page
    temp_usage_prompt = input("Would you consider using a template? [y/n]\n")
    # If you choose to use template or even write a new template
    if temp_usage_prompt == 'y':
        with open('message/templates.json', 'r', encoding='utf-8') as tmp_fp:
            template_list = json.load(tmp_fp)
            tmp_fp.close()

        print("\nAvailable templates:")
        print("====================")

        for c_i in range(0, len(template_list)):
            print(str(c_i) + ": " + template_list[c_i]["label"])

        ans_prompt1 = input(
            "\nWould you choose to use template or write on your own? [y/n]\n")
        # if you consider using the pre-defined template
        if ans_prompt1 == "y":
            temp_id = int(input("\nEnter the template id: "))
            temp_text = template_list[temp_id]["text"]
        # If you consider writing custom message and saving it to a template
        else:
            print("\nFeel comfortable writing text in HTML format:")
            print("===========================================\n")
            contents = []
            while True:
                line = input()
                if line == '':
                    break
                contents.append(line)
            temp_text = '<br>'.join(contents)
            new_temp_text = temp_text
            new_temp_label = input("\nPlease provide a label: ")

            # If you didn't provided any templates
            if new_temp_label != '' or new_temp_text != '':
                with open('message/templates.json', 'w', encoding='utf-8') as msg_tmp_fp:
                    template_list.append(
                        {"label": new_temp_label, "text": new_temp_text})
                    json.dump(template_list, msg_tmp_fp, indent=4)
                    msg_tmp_fp.close()
        mail_html_page += temp_text
    # If you consider not using templates
    else:
        pass

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

    print("Template written sucessfully!")
    # For date of update
    dateToday = date.today()
    dateStr = "<b>" + str(dateToday.month) + "/" + str(dateToday.day) + "/" + str(dateToday.year) + " " + \
        get_week_name(dateToday.weekday()) + "</b><br>Time: <b>" + \
        time.strftime("%I:%M %p %z") + "</b>"
    mail_html_page += "<p> Date: " + dateStr + "</p>"

    mail_html_page += "<h3> Some snapshots </h3>"
    # container for embedding images
    files = []
    for (path, dirnames, filenames) in os.walk('snapshots'):
        files.extend(os.path.join(path, name) for name in filenames)
    print("\nEmbedding image reference...")
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
                              <p>The email is hereby sent to you for the purpose of status update of the activities under the operation of internship.</p><p><b>Thanks for watching</b></p>
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

    with open('mail/mail.html', 'w', encoding="utf-8") as mail_page_fp:
        mail_page_fp.write(mail_html_page)
        mail_page_fp.close()

    print("\nMail page written sucessfully!")

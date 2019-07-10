import os


def chk_send_mail():
    ans = input("Would you like to send status update e-mail: [y/n]\n")
    if ans == 'y':
        send_mail()
        msg_farewell()
    elif ans == 'n':
        msg_farewell()
        pass
    else:
        chk_send_mail()


def msg_farewell():
    print("################################")
    print("#       Thanks for using       #")
    print("################################")


def send_mail():
    os.system("python3 sendmail.py")


if __name__ == "__main__":
    print("\n[mail_confirm.py]\n")
    chk_send_mail()

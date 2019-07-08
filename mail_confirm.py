import os


def chk_send_mail():
    ans = input("Would you like to send status update e-mail: [y/N]\n")
    if ans == 'y':
        send_mail()
        msg_farewell()
    elif ans == 'N':
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
    chk_send_mail()

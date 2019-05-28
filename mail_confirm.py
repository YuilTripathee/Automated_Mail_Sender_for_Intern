import os

def chk_send_mail():
    ans = input("Would you like to send status update e-mail: [y/N]\n")
    if ans == 'y':
        send_mail()
    elif ans == 'N':
        pass
    else:
        chk_send_mail()

def send_mail():
    os.system("python3 sendmail.py")

if __name__ == "__main__":
    chk_send_mail()

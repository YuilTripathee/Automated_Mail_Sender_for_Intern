import os

# def chk_send_mail():
#     ans = input("Would you like to send status update e-mail: [y/n]\n")
#     if ans == 'y':
#         select_mail()
#         msg_farewell()
#     elif ans == 'n':
#         msg_farewell()
#         pass
#     else:
#         chk_send_mail()

def select_mail():
    print("You've got the following variant of mail sending bot:")
    print("=====================================================\n0:\tMinified\n1:\tExtended")
    print("=====================================================\n")
    choice = int(input("Enter the 'id' of the bot you wished: "))
    send_mail(choice)

def msg_farewell():
    print("################################")
    print("#       Thanks for using       #")
    print("################################")


def send_mail(id):
    if id == 0:
        os.system("python3 min/sendmail.py")
    elif id == 1:
        os.system("python3 sendmail.py")
    else:
        select_mail()


if __name__ == "__main__":
    print("\n[mail_confirm.py]\n")
    # chk_send_mail()
    select_mail()

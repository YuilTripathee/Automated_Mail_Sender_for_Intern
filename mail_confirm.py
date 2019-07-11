import os

# checks if you're desiring to send mail
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

# method for selection of the mailer bot variant (i.e. minified or extended)
def select_mail():
    print("You've got the following variant of mail sending bot:")
    print("=====================================================\n0:\tMinified\n1:\tExtended")
    print("=====================================================\n")
    choice = int(input("Enter the 'id' of the bot you wished: "))
    send_mail(choice)

# returns thank you message
def msg_farewell():
    print("################################")
    print("#       Thanks for using       #")
    print("################################")

# executes script for sending mail
def send_mail(id):
    if id == 0:
        os.system("python3 min/sendmail.py")
    elif id == 1:
        os.system("python3 sendmail.py")
    else:
        select_mail()


if __name__ == "__main__":
    print("\n" + __file__ + "\n")
    # chk_send_mail() # depreciated due to inconvenience (can return if needed permissive functionality)
    select_mail()

figlet "Status Update Tool" -f banner

cd $HOME/Programs/MailerAuto/ # or the program directory
pwd

sleep 3
tree

echo ""
echo "Automated intern status update tool based on email"
echo "=================================================="

python3 mail_confirm.py

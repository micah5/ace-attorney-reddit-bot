import praw
from server import get_request

import random

import os
import sys
from os.path import exists

# return address should be the same you set on your reddit apps
IP = 'localhost'
PORT = 8080

# getting client_id and client_secret from enviroment variables
reddit_client_id = os.environ.get("reddit_client_id")
reddit_client_secret = os.environ.get("reddit_client_secret")

# creating the reddit instance
reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    redirect_uri=f"http://{IP}:{PORT}",
    user_agent="/u/objection-bot v0.0"
)

# State is a random string created to prevent nefarious activity from going through. 
state = str(random.randint(0, 65000))

# this grants identity, read and submit permissions to the app
print('please go to the URL below to authenticate app')
print(reddit.auth.url(["identity", "read", "submit"], state, "permanent"))

# awaiting for response to IP:PORT
response = get_request(IP, PORT)

# parsing the response output to get the state and code variables
state_new, code = response.strip('/?').split('&')
state_new = state.split('=')[0]
code = code.split('=')[1]

# checking if state was changes and if so abort
if state_new != state:
    print('state changed. possible nefarious activity. running not reccomended')
    sys.exit()

try:
    with open('.refresh_token.txt', 'w') as token_file:
        # begin authorization with code and write the key to .refresh_token.txt
        token_file.write(reddit.auth.authorize(code))
    
    print('Authorization Successful')

except Exception as e:
    print('ERROR: Something went wrong')
    print(e)
    sys.exit()


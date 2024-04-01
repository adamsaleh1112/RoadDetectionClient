import requests  # Importing requests, a library that allows commands to be sent to ip's
from datetime import datetime  # Importing a dat time library, allows date and time to be accessed
from logdefiner import get_log_name

filename = get_log_name()


def forward():  # Forward command
    # url = 'http://192.168.1.34:5000/forward'  # Sending command to ip route forward
    # data = {'command': 'forward'}  # Sending forward command
    # response = requests.post(url, data=data)  # Making the data being sent = forward

    with open('usernamelog.txt', 'r') as f:  # Opening usernamelog.txt to read
        username = str(f.readlines()[-1:])  # Reading it
        username = username.strip("['")  # Removing unwanted characters
        username = username.strip("']")

    with open(filename, 'a') as f:  # Opening log.txt to append
        now = datetime.now()  # Getting date and time
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")  # Setting date and time string
        f.write(username + ": " + dt_string + ' Move forward \n')  # Combing strings and sending it to log.txt


def backward():  # Same as forward command, but command being sent is 'backward'
    # url = 'http://192.168.1.34:5000/backward'
    # data = {'command': 'backward'}
    # response = requests.post(url, data=data)

    with open('usernamelog.txt', 'r') as f:
        username = str(f.readlines()[-1:])
        username = username.strip("['")
        username = username.strip("']")

    with open(filename, 'a') as f:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        f.write(username + ": " + dt_string + ' Move backward \n')


def left():  # Same as forward command, but command being sent is 'left'
    # url = 'http://192.168.1.34:5000/left'
    # data = {'command': 'left'}
    # response = requests.post(url, data=data)

    with open('usernamelog.txt', 'r') as f:
        username = str(f.readlines()[-1:])
        username = username.strip("['")
        username = username.strip("']")

    with open(filename, 'a') as f:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        f.write(username + ": " + dt_string + ' Move left \n')


def right():  # Same as forward command, but command being sent is 'right'
    # url = 'http://192.168.1.34:5000/right'
    # data = {'command': 'right'}
    # response = requests.post(url, data=data)

    with open('usernamelog.txt', 'r') as f:
        username = str(f.readlines()[-1:])
        username = username.strip("['")
        username = username.strip("']")

    with open(filename, 'a') as f:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        f.write(username + ": " + dt_string + ' Move right \n')


def stop():  # Same as forward command, but command being sent is 'stop'
    # url = 'http://192.168.1.34:5000/stop'
    # data = {'command': 'stop'}
    # response = requests.post(url, data=data)

    with open('usernamelog.txt', 'r') as f:
        username = str(f.readlines()[-1:])
        username = username.strip("['")
        username = username.strip("']")

    with open(filename, 'a') as f:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        f.write(username + ": " + dt_string + ' Stop \n')


def go():  # Same as forward command, but command being sent is 'go'
    # url = 'http://192.168.1.34:5000/go'
    # data = {'command': 'go'}
    # response = requests.post(url, data=data)

    with open('usernamelog.txt', 'r') as f:
        username = str(f.readlines()[-1:])
        username = username.strip("['")
        username = username.strip("']")

    with open(filename, 'a') as f:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        f.write(username + ": " + dt_string + ' Go \n')

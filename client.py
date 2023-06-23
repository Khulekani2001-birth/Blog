from socket import *
import os
from datetime import date
import ast
import threading

user = { "Method": "", "S_Username": "", "S_Address": "", "S_Port": "", "D_Username": "", "Message": "", "Status":"", "MessageHistory": ">>>>\tI N B O X\t<<<<\n"}
servername = '172.31.84.230' #gethostbyname(gethostname())
serverPort = 9323
cSocket = socket(AF_INET, SOCK_DGRAM)

# Fuction to prompt the user when you chat app starts.
def Welcome():
    os.system("CLS")
    print("Welcome to the chat app!")
    print("1. Login\n2. Register")
    a = input()
    print("Please enter your username:")
    name = input()
    if (a == "1"):
        userInfo = updateUser(name)
    else:
        userInfo = CreateUser(name) #Instantiate dictionary with user information
    cSocket.sendto(str(userInfo).encode(), (servername,serverPort)) #Send user details to server as string dictionary
    os.system("CLS") #ClearScreen
    clientDetails, serverAddr = cSocket.recvfrom(2048) #1st server response with this client address as msg
    clientDetails = ast.literal_eval(clientDetails.decode())
    user['S_Port'] = clientDetails[1] #Update Port with client one received from server
    user["S_Address"]= clientDetails[0] #Update Address with client one received from server

def updateUser(Username):
    user['Method'] = "UPDATE"           # Requests serever to login user and allow them to send messages continuously.
    user['S_Username'] = Username
    user['Status'] = "Online"
    return user

# Method that creates a dictionary with data entries that will be useful for communicting with server.
def CreateUser(Username):
    user['Method'] = "CREATE"           # Requests serever to create user and allow them to send messages continuously.
    user['S_Username'] = Username
    user['Status'] = "Online"
    return user

# Method for creating a 1 on 1 chat with a user.


# Method to update user data entries in dictionary when user wants to go offline.
def offLine(Username):
    user['Method'] = 'OFF'
    user['Username'] = Username
    user['Status'] = "Offline"
    user['Message'] = "Going offline"
    return user

# Method to update user data entries when an existing user (currently offline) wants to come back online.
def onLine(Username):
    user['Method'] = 'ON'
    user['Username'] = Username
    user['Status'] = "Online"
    user['Message'] = "Back Online"
    return user

# Method for sending a message to the server.
def SendMsg(Msg):
    user['Method'] = "SEND"
    user['Message'] = Msg
    return user

# Fuction to receive messages from the sever and print it to the client's screen.
def recThread():
    while True:
        res , c = cSocket.recvfrom(2048)
        global textIn
        textIn = res.decode()
        print(textIn)


def main():
    Welcome()
    chatInit, serverAddr= cSocket.recvfrom(2048)  # Receives response sent by client to create new user/ go online.

    if chatInit.decode() == "online":
        print("Welcome to the Chat App!")
        today = date.today()
        print(today.strftime("%B %d, %Y"))
        print("Options:\n[!0]-- Disconnect\n[!1]-- Reconnect\n[!PM]-- Access Private Chat\n[!GC]-- Access Group Chat")
        while True:      
            threading.Thread(target=recThread, args=()).start()  # Calls on the recThread fuction to listen for messages from server
                                                                # to allow client to keep sending messages while still listening for messages from the server.
            sendTXT = input()
            if(sendTXT == "!0"):
                sendTXT = offLine(user["S_Username"])
            elif (sendTXT == "!1"):
                sendTXT = onLine(user["S_Username"])
            else:
                sendTXT = SendMsg(sendTXT)
            cSocket.sendto(str(sendTXT).encode(), serverAddr)

if __name__=="__main__":
    main()
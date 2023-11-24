import subprocess
#import napalm
from napalm import get_network_driver
import requests
from requests.auth import HTTPBasicAuth
import json
import base64
#Imports the SMTP and SSL libraries for the email notication
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Function that retrieves the user info from a json file.
def get_user(name):
    #tries to open a json file that has encoded data.
    try:
        
        with open("/var/www/Network_Tool_Napalm/jsonfile."+name+".json", "r") as f:
	    #f= open(jsonfile.{name}.json, "r")
            #injests this json file and converts it to a python dictionary
            data = json.load(f)
            print(data)
            #makes sure its a dictionary
        assert type(data) is dict
            
        #returns the dictionary
        print(data['salt1'])
        #Decodes the data
        base64_message = data['salt1']
        base64_bytes = base64_message.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        username = message_bytes.decode('ascii')

        print(data['salt2'])
        #Decodes the the data
        base64_message2 = data['salt2']
        base64_bytes2 = base64_message2.encode('ascii')
        message_bytes2 = base64.b64decode(base64_bytes2)
        password = message_bytes2.decode('ascii')
        return username, password
    except:
        #if it does't exist, it returns nothing.
        
        return None



 
## call date command ##
p = subprocess.Popen("arp | grep 192.168.33.1", stdout=subprocess.PIPE, shell=True)
 
## Talk with date command i.e. read data from stdout and stderr. Store this info in tuple ##
## Interact with process: Send data to stdin. Read data from stdout and stderr, until end-of-file is reached.  ##
## Wait for process to terminate. The optional input argument should be a string to be sent to the child process, ##
## or None, if no data should be sent to the child.
(output, err) = p.communicate()
 
## Wait for date to terminate. Get return returncode ##
p_status = p.wait()
print (output)
output=output.split()
macaddress=output[2]

macaddress=macaddress.decode('UTF-8')
#macaddress="b8:27:eb:1c:19:4a" 
macaddress=str(macaddress)
print(macaddress+'after mac address')
print('Almost at if statement')
#macaddress=macaddress.upper()

if macaddress == "f8:0b:cb:d5:77:d1":
    print ("ARP Entry valid. No change")

else:
    print('inside else statement')
    macaddress=macaddress.upper()
    print(macaddress)
    username,password=get_user('network')
    #username = 'lswisher'
    #password = 'Jojo6512!!Jojo2023!!!'
    print('Potentially AP spoofing attack detected. ARP entry is: ', macaddress)
    driver=get_network_driver('ios')
    iosvl2 = driver('192.168.33.2', username, password)


    iosvl2.open()

    macaddresstable = iosvl2.get_mac_address_table()
    print(macaddresstable)
    iosvl2.close()    

    for mac in macaddresstable:
        print(mac)
        if mac['mac'] == macaddress:
            print('MAC address found on switchport: ', mac['interface'])
            interface=mac['interface']
            print(interface)
            interface=interface.strip('Gi')
            print(interface)
            headers = {'Accept': 'application/yang-data+json','Content-Type':'application/yang-data+json'}
            payload={
            "Cisco-IOS-XE-native:GigabitEthernet": {
                "name": interface,
                "shutdown": '',
                
                    
                }}
            #Changes the interface number format to match the syntax for the RESTCONF call
            interfacerestnumber=interface.replace('/','%2F')
            print(interfacerestnumber)
            
            token = requests.put ("https://192.168.133.2/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet="+interfacerestnumber, headers=headers,json=payload, auth=HTTPBasicAuth(username, password), verify=False)##This works. 
            
            #headers=headers,
            print(token)
            print(token.text)
            
            #Grabs the creds for the email SMTP relay
            email_john,emailp=get_user("email")

            #Defines the email sender
            sender = "John's Data Center<app@example.com>"
            #Defines the email reciever
            receiver = "testemail@gmail.com"

            #If the email can't be formulated in HTML, text is also defined as a backup.
            text = " John's Data Center SECURITY ALERT!!"

            text += "Notification!"

            text += "An ARP Spoofing attack was detected on the network. The MAC address "+macaddress+" was found on the switchport "+interface+"."

            text += " This port has been disabled to prevent further attacks."
                

            text +=" Thanks! "

            text += " The admins.."

            #Creates the HTML message for the body of the email. Adds variables where needed.
            html = "<html>"
            html += "<body>"
            html +=  "<h3>Notification!</h3>"
            html += "<p>John's Data Center SECURITY ALERT!! </p>"


            html += "<p> An ARP Spoofing attack was detected on the network. The MAC address "+macaddress+" was found on the switchport "+interface+". </p>"

            html +="<p> This port has been disabled to prevent further attacks.</p>"
                

            html += "<p>-Thank you!<br>John Strasser</p>"
            html += "</body>"
            html += "</html>"
            
            #Defines message
            message = MIMEMultipart("alternative")
            #Tacks on a subject to the message and adds the sender and receiver info, as well
            message["Subject"] = "John's Data Center SECURITY ALERT!!"
            message["From"] = sender
            message["To"] = receiver

            #Attaches both a plain text message and an HTML version for the recieving email client
            message.attach(MIMEText(text,"plain"))
            message.attach(MIMEText(html,"html"))

            context = ssl.create_default_context()
            #Sends the email using the mail trap could service. I updated the login with my personal credentials provided by mail trap.
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                #Logs in using the email info and creds grabbed above.
                server.login(email_john, emailp)
                #Sends the actual email.
                server.sendmail(sender, receiver, message.as_string())



     


           



print ("Command exit status/return code : ", p_status)

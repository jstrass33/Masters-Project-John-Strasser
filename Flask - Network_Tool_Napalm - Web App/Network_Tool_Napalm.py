#Master's Project
#Author: John (Omitted Last name for privacy)
#Professor Allouzi
#Date: Fall 2023
#Description: This web applciations purpose is the create a portal so VLAN and description changes
    #can be applied to switches in my test data center. It pulls the info via Napalm and makes changes
    #via a RESTCONF API.

#Imports the requests library for API calls
import requests
#Imports the requests auth function for API calls
from requests.auth import HTTPBasicAuth

#Imports Flask libary for flask web framework
from flask import Flask, redirect, url_for, render_template, request, make_response

#Authentication piece of Flask
from flask_httpauth import HTTPBasicAuth
#import flask_httpauth
from werkzeug.security import generate_password_hash, check_password_hash

#Imports the string function
import string

#Imports the json function. This is needed for the rest API calls.
import json

#Imports base64 for decoding
import base64

#Imports the randon function
import random

#Imports the string function
import string

#Imports Nampalm Libary for grabbing info from the switches
import napalm
from napalm import get_network_driver

#Imports the SMTP and SSL libraries for the email notication
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#Function that retrieves the user info from a json file.
def get_user(name):
    #tries to open a json file that has encoded data.
    try:
        with open(f"/var/www/Network_Tool_Napalm/jsonfile.{name}.json", "r") as f:
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
        print('Couldnt open up file.')
        return None

#Grabs credentials for the web app to authenticate against
#username,password=get_user("network")

#print(username)
#print(password)
#Initializes Flask APP
app = Flask(__name__)

    
#Creates empty dictionary that can be used as a global variable
interface_dictionary={}


#Main route for the root /. Accepts GET and POST. GET for the intial page load and POST for the form submission.
@app.route("/",methods=['GET','POST'])
#Requires basic authentication to load the / page.
#@auth.login_required
#Main function for the root rout
def home():
    #Injects the global variables outlined above.
    global interface_dictionary
   
    
    

    #Defines actions depending if the method for the route is POST
    if request.method=='POST':
        #Defines code if the POST form submission has the "submit" ID in it.
        if  "submit" in request.form:
            print('Submit if statement 1.')
            
            #Sets the VLAN variable to none so that the change VLAN form doesnt appear on the html page
            vlan=None
            print('About to print VLAN:')
            print(vlan)
            #Grabs the IP address from the HTML form
            IP = request.form.get('IP')
            #Calls the function that pulls all of the interface and version information from the switch and returns the variables
            interface_dictionary, hostname, version, serial_number, model, vendor= get_switch_stats(IP)
            
            #Returns the template with the dynamic content injected into the Jinga template
            return render_template("response.tpl", data=interface_dictionary, hostname=hostname, vendor=vendor, version=version, IP=IP,  model=model, serial_number=serial_number, vlan=vlan)
        
        #If the main index POST form pointing to the site response page is triggered, this code executes
        if  "siteresponse" in request.form:
            
            print('Inside the site response if statement')
            #Returns the site response HTML template.
            return render_template("site_response.tpl")

        #If the form on the response page is submitted with the changevlan ID in it, it triggers this code.
        if  "changevlan" in request.form:

            print('Submit if statement 2 - changevlan')
            #Grabs the VLAN info from the form that was submitted
            vlan= request.form.get('vlan')
            print('About to print VLAN:')
            print(vlan)
            #Grabs the hostname from the embedded input information in the form.
            hostname= request.form.get('formhostname')
            #Grabs the interface from the embedded input information in the form.
            inter= request.form.get('forminterface')
            #Grabs the version from the embedded input information in the form.
            version= request.form.get('version')
            #Grabs the vendor from the embedded input information in the form.
            vendor= request.form.get('vendor')
            #Grabs the model from the embedded input information in the form.
            model= request.form.get('model')
            #Grabs the serial number from the embedded input information in the form.
            serial_number= request.form.get('serial_number')
            #Grabs the IP address from the embedded input information in the form.
            IP= request.form.get('ipaddress')
            print(version)
            print(vendor)
            print(model)
            print(serial_number)
        
            print('about to print form dictionary')
            #Uses the global interface_dictionary that was already delivered when the page initially was loaded
            print(interface_dictionary)

            #Responds with the same template except with added VLAN info and interface info. This change triggers the hidden form to appear
            return render_template("response.tpl", data=interface_dictionary, hostname=hostname, vlan=vlan, IP=IP, interface=inter, version=version, vendor=vendor, model=model, serial_number=serial_number)
        
        if "submit2" in request.form:
            print('Inside submit2 if statement.')
            #Grabs the VLAN that the user wishes to change the port to from the form.
            vlan= request.form.get('vlanchangenumber')
            #Grabs the description to be used on the port from the form.
            if vlan != int:
                error='Please enter a valid VLAN number.'
                render_template("error.tpl", error=error)
            reason= request.form.get('changereason')
            print('About to print VLAN:')
            print(vlan)
            #Grabs the interface from the embedded input information in the form.
            inter= request.form.get('forminterface')
            #Grabs the IP address from the embedded input information in the form.
            IP= request.form.get('ipaddress')
            
            #Calls the send config function. This makes the VLAN change with the added parameters
            send_config(IP,inter,vlan,reason)

            #Executes the get switch stats function to pull in the updated switch interface info
            interface_dictionary, hostname, version, serial_number, model, vendor= get_switch_stats(IP)
            #Changes the VLAN back to none so that the VLAN change form doesnt display initially.
            vlan=None

            #Returns the response template with the dynamic content defined.
            return render_template("response.tpl", data=interface_dictionary, hostname=hostname, vendor=vendor, version=version, IP=IP, interface=inter, model=model, serial_number=serial_number, vlan=vlan)


    
    #The template that is rendered when the default GET method is issued.
    return render_template("index.tpl")

#Route for /switch_ip route that takes the IP as a paramenter that can be used in the function
@app.route("/switch_ip/<IP>")
def get_switch_stats(IP):
   #Sets the VLAN variable to none so that VLAN change form isn't populated.
    vlan=None

    #Calls the get switchs stats function to gather switch info.
    interface_dictionary, hostname, version, serial_number, model, vendor= get_switch_stats(IP)
    #Returns the template with the dynamic content injected into the Jinga template
    return render_template("response.tpl", data=interface_dictionary, hostname=hostname, vendor=vendor, version=version, IP=IP,  model=model, serial_number=serial_number, vlan=vlan)
        
#Defines function that changes VLAN on switch
def send_config(IP,inter,vlan,reason):

    #Calls function to get creds
    username,password=get_user("network")
    print('Inside send config function.')
    print(inter)
    print(vlan)
    #Removes GigabitEthernet and just leaves the interface number
    internumber=inter.strip('GigabitEthernet')
    print(internumber)
    
    #Defines the header used for the REST Call
    headers = {'Accept': 'application/yang-data+json','Content-Type':'application/yang-data+json'}
    #Defines the payload of data to use in the rest call. This json data changes the VLAN to the user defined VLAN.
    payload={
    "Cisco-IOS-XE-native:GigabitEthernet": {
        "name": internumber,
        "description": reason,
        "switchport": {
        "Cisco-IOS-XE-switch:access": {
            "vlan": {
            "vlan": int(vlan) }
            
        }}}}
    
    #Changes the interface number format to match the syntax for the RESTCONF call
    interfacerestnumber=internumber.replace('/','%2F')

    
    print(interfacerestnumber)

    print(payload)
    #Imports the seperate requests HTTPBasicAuth libary. Needed to be done here since HTTPBasic Auth was already imported for Flask
    from requests.auth import HTTPBasicAuth
    #Forms auth object from the HTTPBasicAuth function and given creds
    auth = HTTPBasicAuth(username, password)

    #Performs the RESTCONF call with the appropriate parameters
    changedresults = requests.put ("https://"+IP+"/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet="+interfacerestnumber, headers=headers,json=payload, auth=auth, verify=False)##This works. 
    #headers=headers,
    print(changedresults)
    print(changedresults.text)

    #Calls the email alert function to let the admin know of the changes
    email_alert(IP,inter,vlan,reason)

    
#Creates the get switch stats function to gather info from the switch
def get_switch_stats(IP):

    #Gets creds using the get user function
    username,password=get_user("network")

    print('Inside switch stats function')
    print(username)
    print(password)

    #Defines the driver for napalm connection.
    driver=get_network_driver('ios')
    
    #Establishes napalm object for the connection.
    iosvl2 = driver(IP, username, password)

    #Opens the napalm connection to the IP provided by the user
    iosvl2.open()

    #Grabs interface information from the switch
    ios_outputs = iosvl2.get_interfaces()
    #Grabs VLAN information from the switch
    vlans=iosvl2.get_vlans()
    #Gathers general facts from the switch like version, model, etc
    facts=iosvl2.get_facts()
    #Grabs additional info from the switch.
    environment=iosvl2.get_environment()

   
    #Injects the global interface dictionary into the function for use.
    global interface_dictionary
    
    #For loop for building the dictionary based off interfaces in dictionary
    for interface in ios_outputs:
        print(interface)
        #Excludes unnecassary interfaces in the dictionary
        if 'Vlan' in interface or "Virtual" in interface or 'AppGigabitEthernet' in interface or 'GigabitEthernet0/0' in interface or 'FastEthernet0' in interface:
            
            print(ios_outputs[interface]['is_up'])
        
            
        else: 
            #Updates the dictionary with the interface namea s the key and the description and connected status as items.
            interface_dictionary.update({
                            interface:{
                                
                                "Description": ios_outputs[interface]['description'] ,
                                "Connected": ios_outputs[interface]['is_up'],
                                
                                
                            }
                        })
        
    #Loops through the VLANs object to add them to the dictionary    
    for vlan in vlans:
        #Loops through the interfaces in the VLAN list
        for interface in vlans[vlan]['interfaces']:
            
            #If the interface is part of the interface dictionary, it adds the VLAN as a key under the interface.
            if interface in interface_dictionary:
                interface_dictionary[interface]['Vlan']=vlan
            

    print('About to print dictionary')
    print(interface_dictionary)

    #Grabs the vendor, version, serial number, model, and hostname from the facts object.
    vendor=facts['vendor']
    version=facts['os_version']
    serial_number=facts['serial_number']
    model=facts['model']
    hostname=facts['hostname']
    
    #Returns the interface dictionary and the other objects.
    return interface_dictionary, hostname, version, serial_number, model, vendor

#Creates and email alert function for notifying the data center admins
def email_alert(IP,inter,vlan,reason):
    
    #Grabs the creds for the email SMTP relay
    email_john,emailp=get_user("email")

    #Defines the email sender
    sender = "John's Data Center<app@example.com>"
    #Defines the email reciever
    receiver = f"My email at Kent.edu"

    #If the email can't be formulated in HTML, text is also defined as a backup.
    text = f"""\
        John's Data Center Network Changes

        Notification!

        The VLAN on Switch: {IP} Port: {inter} was changed to VLAN: {vlan}.

        The reason for this change was: {reason}
        

        Thanks! 

        The admins..
    """

    #Creates the HTML message for the body of the email. Adds variables where needed.
    html = f"""\
        <html>
        <body>
        <h3>Noticiation!</h3>
        <p>John's Data Center Network Changes </p>


        <p> The VLAN on Switch: {IP} Port: {inter} was changed to VLAN: {vlan}. </p>

        <p> The reason for this change was: {reason} </p>
        

        <p>-Thank you!<br>My Name</p>
        </body>
        </html>
    """
    #Defines message
    message = MIMEMultipart("alternative")
    #Tacks on a subject to the message and adds the sender and receiver info, as well
    message["Subject"] = "John's Data Center Network Changes Alert"
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


if __name__ == '__main__':
	app.run()

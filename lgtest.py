import httplib
import xml.etree.ElementTree as etree
import socket
import re
lgtv = {}
dialogMsg =""
headers = {"Content-Type": "application/atom+xml"}

lgtv["pairingKey"] = "267285"
lgtv["ipaddress"] = "10.50.147.121"
lgtv["port"] = 8080

command="26"

def getip():
    strngtoXmit =   'M-SEARCH * HTTP/1.1' + '\r\n' + \
                    'HOST: 239.255.255.250:1900'  + '\r\n' + \
                    'MAN: "ssdp:discover"'  + '\r\n' + \
                    'MX: 2'  + '\r\n' + \
                    'ST: urn:schemas-upnp-org:device:MediaRenderer:1'  + '\r\n' +  '\r\n'
    bytestoXmit = strngtoXmit.encode()
    sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    sock.settimeout(3)
    found = False
    gotstr = 'notyet'
    i = 0
    ipaddress = None
    sock.sendto( bytestoXmit,  ('239.255.255.250', 1900 ) )
    while not found and i <= 5 and gotstr == 'notyet':
        try:
            gotbytes, addressport = sock.recvfrom(512)
            gotstr = gotbytes.decode()
        except:
            i += 1
            sock.sendto( bytestoXmit, ( '239.255.255.250', 1900 ) )
        if re.search('LG', gotstr):
            ipaddress, _ = addressport
            found = True
        else:
            gotstr = 'notyet'
        i += 1
    sock.close()
    if not found :
        print "Lg TV not found"
    return ipaddress

def displayKey():
    conn = httplib.HTTPConnection( lgtv["ipaddress"], port=lgtv["port"])
    reqKey = "<!--?xml version=\"1.0\" encoding=\"utf-8\"?--><auth><type>AuthKeyReq</type></auth>"
    conn.request("POST", "/roap/api/auth", reqKey, headers=headers)
    httpResponse = conn.getresponse()
    if httpResponse.reason != "OK" :
        print "LG TV: Network error"
    return httpResponse.reason
def getSessionid():
    conn = httplib.HTTPConnection( lgtv["ipaddress"], port=lgtv["port"])
    pairCmd = "<!--?xml version=\"1.0\" encoding=\"utf-8\"?--><auth><type>AuthReq</type><value>" + lgtv["pairingKey"] + "</value></auth>"
    conn.request("POST", "/roap/api/auth", pairCmd, headers=headers)
    httpResponse = conn.getresponse()
    if httpResponse.reason != "OK" :
        return httpResponse.reason
    tree = etree.XML(httpResponse.read())
    return tree.find('session').text
def getPairingKey():
    displayKey()
def handleCommand(cmdcode):
    conn = httplib.HTTPConnection( lgtv["ipaddress"], port=lgtv["port"])
    cmdText = "<!--?xml version=\"1.0\" encoding=\"utf-8\"?--><command><name>HandleKeyInput</name><value>"+cmdcode+"</value></command>"
    conn.request("POST", "/roap/api/command", cmdText, headers=headers)
    httpResponse = conn.getresponse()
#main()
#lgtv["ipaddress"] = getip()
print "LG TV IP: "+lgtv["ipaddress"]
theSessionid = getSessionid()
while theSessionid == "Unauthorized" :
    getPairingKey()
    theSessionid = getSessionid()
if len(theSessionid) < 8 :
    print "LG TV: Could not get Session Id: " + theSessionid
lgtv["session"] = theSessionid
result = command
handleCommand(result)

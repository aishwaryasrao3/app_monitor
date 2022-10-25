Skip to content
Search or jump to…
Pull requests
Issues
Marketplace
Explore
 
@aishwaryasrao3 
aishwaryasrao3
/
apmonitor
Private
Code
Issues
Pull requests
Actions
Projects
Security
Insights
Settings
apmonitor/monitor.py /
@aishwaryasrao3
aishwaryasrao3 Add files via upload
Latest commit c2c3ea3 on 25 Jul 2021
 History
 1 contributor
60 lines (55 sloc)  1.97 KB

import json as js
import time
import socket
from copy import deepcopy
port = 9549
LIMIT = 5
file_to_monitor = ('access_points.json')
oldfile = open(file_to_monitor,'rb')
old = js.load(oldfile)
 
def send_report(output_str):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    host = socket.gethostbyname("localhost")
    s.connect((host, port))
    s.sendall(output_str.encode())
def find_change(old,new):
    if old is None or new is None:
        return 'Empty'
    data_init = old['access_points']
    data_changed = new['access_points']
    output_str = ''
    for config in data_init:
            if config['ssid'] in [ sub['ssid'] for sub in data_changed ]:
                for test in data_changed:
                    if config['ssid']==test['ssid']:
                        if config['snr']!=test['snr']:
                            output_str += config['ssid']+"'s SNR value changed from "+str(config['snr'])+" to "+str(test['snr'])+"\n"
                        if config['channel']!=test['channel']:
                            output_str += config['ssid']+"'s Channel value changed from "+str(config['channel'])+" to "+str(test['channel'])+"\n"
       	    else:
                output_str += config['ssid'] ,"is removed from the list\n"
    for test in data_changed:
            if test['ssid'] not in [pat['ssid'] for pat in data_init ]:
                output_str += test['ssid'],"is newly added to the list\n"
    if output_str == '':
        pass
    else:
        send_report(output_str)
    old = deepcopy(new)

def detect_change():
    changed = open(file_to_monitor,'rb') 
    new = js.load(changed)
    find_change(old,new)

if __name__ == '__main__':
#    if(LIMIT<0):
#        while True:
 #           detect_change()
 #           time.sleep(5)
    file1 = oldfile.readlines()
    changed = open(file_to_monitor,'rb')
    
    file2 = changed.readlines()
    while LIMIT >= 5:
        if file2!=file1:
            detect_change()
            time.sleep(5)
            LIMIT+=5
Footer
© 2022 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About

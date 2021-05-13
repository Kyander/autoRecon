import tkinter as tk
import tkinter.ttk as ttk
import subprocess
from tkinter.messagebox import showwarning
import nmap3
import pydirbuster
import argparse
import os
import sys
import threading
from ftplib import FTP
from bs4 import BeautifulSoup, Comment
import requests
import smbclient

global ibuster,inikto
ibuster = 0
inikto = 0

global busterList,niktoList
niktoList = []
busterList = []

global smbCheckCmd
global bruteSMBcmd
global bruteFTPcmd
global bruteSSHcmd
global rootDir

def btnAlotNikto(frame):
    global inikto
    if inikto > 3:
        inikto = 0
    else:
        pass
    print(inikto)
    print(frame["nikto"][inikto])
    raise_frame(frame["nikto"][inikto])
    inikto += 1


def btnAlotBuster(frame):
    global ibuster
    if ibuster > 3:
        ibuster = 0
    else:
        pass
    print(ibuster)
    print(frame["buster"][ibuster])
    raise_frame(frame["buster"][ibuster])
    ibuster += 1

def raise_frame(frame):
    frame.tkraise()

class NewprojectApp:
    def __init__(self,listing, master=None):
        # build ui
        self.mainFrame = ttk.Frame(master)
        self.BtnFrame = ttk.Frame(self.mainFrame)
        self.bnikto = ttk.Button(self.BtnFrame)
        self.bnikto.configure(text='Nikto')
        self.bnikto.pack(side='top')
        self.bnikto.configure(command=lambda:btnAlotNikto(self.frameDict))
        self.bsshBrute = ttk.Button(self.BtnFrame)
        self.bsshBrute.configure(text='SSH Brute')
        self.bsshBrute.configure(command=lambda:raise_frame(self.fsshBrute))
        self.bsshBrute.pack(side='top')
        self.bftpBrute = ttk.Button(self.BtnFrame)
        self.bftpBrute.configure(text='FTP Brute')
        self.bftpBrute.configure(command=lambda:raise_frame(self.fFtpBrute))
        self.bftpBrute.pack(side='top')
        self.bsmbBrute = ttk.Button(self.BtnFrame)
        self.bsmbBrute.configure(text='SMB Brute')
        self.bsmbBrute.configure(command=lambda:raise_frame(self.fsmbBrute))
        self.bsmbBrute.pack(side='top')
        self.bdirbuster = ttk.Button(self.BtnFrame)
        self.bdirbuster.configure(text='Dirbuster')
        self.bdirbuster.configure(command=lambda:btnAlotBuster(self.frameDict))
        self.bdirbuster.pack(side='top')
        self.bsmbCheck = ttk.Button(self.BtnFrame)
        self.bsmbCheck.configure(text='SMBCheck')
        self.bsmbCheck.configure(command=lambda:raise_frame(self.fSmbChecker))
        self.bsmbCheck.pack(side='top')
        self.bNmapView = ttk.Button(self.BtnFrame)
        self.bNmapView.configure(text='View NMAP')
        self.bNmapView.configure(command=lambda:raise_frame(self.fNmap))
        self.bNmapView.pack(side='top')
        self.BtnFrame.configure(height='200', width='200')
        self.BtnFrame.grid(column='0', row='1')
        self.fSmbChecker = ttk.Frame(self.mainFrame)
        self.fSmbChecker.configure(height='600', width='600')
        self.fSmbChecker.grid(column='1', row='1')
        self.fNikto1 = ttk.Frame(self.mainFrame)
        self.fNikto1.configure(height='600', width='600')
        self.fNikto1.grid(column='1', row='1')
        self.fNikto2 = ttk.Frame(self.mainFrame)
        self.fNikto2.configure(height='600', width='600')
        self.fNikto2.grid(column='1', row='1')
        self.fNikto3 = ttk.Frame(self.mainFrame)
        self.fNikto3.configure(height='600', width='600')
        self.fNikto3.grid(column='1', row='1')
        self.fNikto4 = ttk.Frame(self.mainFrame)
        self.fNikto4.configure(height='600', width='600')
        self.fNikto4.grid(column='1', row='1')
        self.fbuster1= ttk.Frame(self.mainFrame)
        self.fbuster1.configure(height='600', width='600')
        self.fbuster1.grid(column='1', row='1')
        self.fbuster2 = ttk.Frame(self.mainFrame)
        self.fbuster2.configure(height='600', width='600')
        self.fbuster2.grid(column='1', row='1')
        self.fbuster3 = ttk.Frame(self.mainFrame)
        self.fbuster3.configure(height='600', width='600')
        self.fbuster3.grid(column='1', row='1')
        self.fbuster4 = ttk.Frame(self.mainFrame)
        self.fbuster4.configure(height='600', width='600')
        self.fbuster4.grid(column='1', row='1')
        self.fsshBrute = ttk.Frame(self.mainFrame)
        self.fsshBrute.configure(height='600', width='600')
        self.fsshBrute.grid(column='1', row='1')
        self.fFtpBrute = ttk.Frame(self.mainFrame)
        self.fFtpBrute.configure(height='600', width='600')
        self.fFtpBrute.grid(column='1', row='1')
        self.fsmbBrute = ttk.Frame(self.mainFrame)
        self.fsmbBrute.configure(height='600', width='600')
        self.fsmbBrute.grid(column='1', row='1')
        self.mainFrame.configure(height='200', width='200')
        self.mainFrame.pack(side='top')
        self.fNmap = ttk.Frame(self.mainFrame)
        self.fNmap.configure(height='600', width='600')
        self.fNmap.grid(column='1', row='1')
        self.niktoFrames = [self.fNikto1,self.fNikto2,self.fNikto3,self.fNikto4]
        self.busterFrames = [self.fbuster1,self.fbuster2,self.fbuster3,self.fbuster4]
        self.frameDict = {"nikto":self.niktoFrames,"buster":self.busterFrames}
        self.idListBuster = [self.fbuster1.winfo_id(),self.fbuster2.winfo_id(),self.fbuster3.winfo_id(),self.fbuster4.winfo_id()]
        self.idListNikto = [self.fNikto1.winfo_id(),self.fNikto2.winfo_id(),self.fNikto3.winfo_id(),self.fNikto4.winfo_id()]
        self.idSmbCheck = self.fSmbChecker.winfo_id()
        self.idSmbBrute = self.fsmbBrute.winfo_id()
        self.idFtpBrute = self.fFtpBrute.winfo_id()
        self.idSshBrute = self.fsshBrute.winfo_id()
        self.idNamp = self.fNmap.winfo_id()
        # Main widget
        self.mainwindow = self.mainFrame

        '''
        DIRBUSTER 
        '''

        try:
            i = 0
            for cmd in busterList:
                p = subprocess.Popen(
                    ["xterm", "-into", str(self.idListBuster[i]), "-geometry", "100x100","-hold","-e","{}".format(cmd)],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                i += 1
            if i < 4:
                newI = 4 - i
                for notAv in range(0,newI):
                    if i == 5:
                        break
                    else:
                        pass
                    p = subprocess.Popen(
                        ["xterm", "-into", str(self.idListBuster[i]), "-geometry", "100x100", "-hold", "-e",
                         "echo '[!] Nothing here!'"],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                    i +=1
            '''
            DIRBUSTER ^^^^^
            '''

            '''
            NIKTO 
            '''

            try:
                i = 0
                for cmd in niktoList:
                    p = subprocess.Popen(
                        ["xterm", "-into", str(self.idListNikto[i]), "-geometry", "100x100", "-hold", "-e",
                         "{}".format(cmd)],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                    i += 1
                if i < 4:
                    newI = 4 - i
                    for notAv in range(0, newI):
                        if i == 5:
                            break
                        else:
                            pass
                        p = subprocess.Popen(
                            ["xterm", "-into", str(self.idListNikto[i]), "-geometry", "100x100", "-hold", "-e",
                             "echo '[!] Nothing here!'"],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                        i += 1
            except:
                pass


            '''
            NIKTO ^^^^
            '''

            '''
            SMBCHECK
            '''
            global smbCheckCmd
            try:
                p2 = subprocess.Popen(
                    ["xterm", "-into", str(self.idSmbCheck), "-geometry", "100x100", "-hold", "-e", "{}".format(smbCheckCmd)],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            except:
                self.bsmbCheck.pack_forget()

            global bruteSMBcmd
            try:
                p2 = subprocess.Popen(
                    ["xterm", "-into", str(self.idSmbBrute), "-geometry", "100x100", "-hold", "-e", "{}".format(bruteSMBcmd)],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            except:
                self.bsmbBrute.pack_forget()

            global bruteFTPcmd
            try:
                p2 = subprocess.Popen(
                    ["xterm", "-into", str(self.idFtpBrute), "-geometry", "100x100", "-hold", "-e",
                     "{}".format(bruteFTPcmd)],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            except:
                self.bftpBrute.pack_forget()
            global bruteSSHcmd
            try:
                p2 = subprocess.Popen(
                    ["xterm", "-into", str(self.idSshBrute), "-geometry", "100x100", "-hold", "-e",
                     "{}".format(bruteSSHcmd)],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            except:
                self.bsshBrute.pack_forget()
            global rootDir
            try:
                p2 = subprocess.Popen(
                    ["xterm", "-into", str(self.idNamp), "-geometry", "100x100", "-hold", "-e", "cat {}/nmap/nmap_scan.txt".format(rootDir)],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            except:
                pass
            '''
            p2 = subprocess.Popen(
                ["xterm", "-into", str(self.idList[1]), "-geometry", "100x100","-hold", "-e", "ping -c 4 localhost"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            p3 = subprocess.Popen(
                ["xterm", "-into", str(self.idList[2]), "-geometry", "100x100"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            p4 = subprocess.Popen(
                ["xterm", "-into", str(self.idList[3]), "-geometry", "100x100", "-e", "ping localhost"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            '''
        except FileNotFoundError:
            showwarning("Error", "xterm is not installed")
            raise SystemExit

    def lol(self):
        pass

    def run(self):
        self.mainwindow.mainloop()


def doNikto(logfile, url):
    global niktoList
    newlogfile = logfile.replace('dirbust','nikto')
    rootfile = logfile.split("dirbust")[0]
    print(rootfile)
    print(newlogfile)
    try:
        os.mkdir("{}/nikto".format(rootfile))
    except:
        pass
    #cords =cordsManager("nikto")
    command = "nikto -host={} -o {}".format(url,newlogfile)
    niktoList.append(command)
    #os.system("xterm -T 'Nikto!' -geometry {} -e {}".format(cords,command))

def commentGrabber(logfile, host, dir):
    global commentsExists
    try:
        os.mkdir("{}/html".format(dir))  # Creates the "HTML" directory
    except:
        pass
    fileComments = os.path.join("{}/html/".format(dir), "comments.txt")  # the comments.txt path

    with open(logfile) as a:  # Puts every gobusted findings from the file inside a list
        content = a.readlines()

    content = [x.strip() for x in content]
    urls = []

    for file in content:  # Creates the urls (appends gobusted findings to url) for requests
        fileFormat = file.split(' ')[0]
        urls.append("{}{}".format(host, fileFormat))

    if commentsExists == False:
        f = open(fileComments, "w+")  # Creates the comments.txt file
        f.write("ALL THE COMMENTS EXTRACTED :\n\n")
        f.close()
        commentsExists = True
    else:
        pass
    for url in urls:  # Grabs all comments and writes it to comments.txt
        r = requests.get(url, verify=False)
        content = r.text
        soup = BeautifulSoup(content, 'html.parser')
        f = open(fileComments, "a")
        f.write("{} :\n\n".format(url))
        f.close()
        for x in soup.findAll(text=lambda text: isinstance(text, Comment)):
            f = open(fileComments, "a")
            f.write(x)
            f.close()


def bust(url, wordlist, logfile, dir):  # THIS IS THE THREADED FUNCTION
    global busterList
    # print(Debug)
    command = "python3 ./busterScript.py --url {} --wordlist {} --output {} --rootDir {}".format(url, wordlist, logfile,dir)
    busterList.append(command)
    if Debug == True:
        print("DEBUG INFO ------- DIRBUST -------\n")
        print("URL : {}\nWORDLIST : {}\nLOGFILE : {}\nCOMMAND : {}".format(url, wordlist, logfile, command))
    else:
        pass
    #cords = cordsManager("dirbust")
    #os.system("xterm -T 'dirbuster!' -geometry {} -e {}".format(cords,command))


def dirbuster(urls, wordlist, logfiles, dir):  # This starts the threads, passing it all it needs.
    i = 0
    for url in urls:
        tnikto = threading.Thread(target=doNikto, args=(logfiles[i], url,))  # FOR NIKTO!
        tdirbust = threading.Thread(target=bust, args=(url, wordlist, logfiles[i], dir)) # FOR DIRBUST!
        tdirbust.start()
        tnikto.start()
        i += 1
'''
def bruteSSH(rootDir, host):
    try:
        os.mkdir("{}/brute".format(rootDir))  # Creates the "brute" directory
    except:
        pass
    cords = cordsManager("brute")
    command = "hydra -s 22 -L ./wordlist/top-usernames-shortlist.txt -P ./wordlist/UserPassCombo-Jay.txt -V ssh://{} -o {}/brute/SSH.txt -I ".format(
        host, rootDir)
    os.system("xterm -T 'bruteforcing SSH!' -geometry {} -e {}".format(cords,command))

def bruteSMB(rootDir, host):
    try:
        os.mkdir("{}/brute".format(rootDir))  # Creates the "brute" directory
    except:
        pass
    cords = cordsManager("brute")
    command = "hydra -t 1 -L ./wordlist/top-usernames-shortlist.txt -P ./wordlist/UserPassCombo-Jay.txt -V {} smb -o {}/brute/SMB.txt -I".format(host,rootDir)
    os.system("xterm -T 'bruteforcing SMB!' -geometry 100x100 -hold -e {}".format(cords,command))

'''
def smbCheck(host,rootDir):
    global smbCheckCmd
    command = "python3 smbCheck.py --host {} --output {}".format(host,rootDir)
    smbCheckCmd = command
    #os.system("xterm -T 'SMB Checker!' -geometry 90x30+0+1080 -hold -e {}".format(command))
'''
def bruteFTP(rootDir, host):
    try:
        os.mkdir("{}/brute".format(rootDir))  # Creates the "brute" directory
    except:
        pass
    command = "hydra -s 21 -t 20 -L ./wordlist/top-usernames-shortlist.txt -P ./wordlist/UserPassCombo-Jay.txt -vV ftp://{} -o {}/brute/FTP.txt -I ".format(host,rootDir)
    os.system("xterm -T 'bruteforcing FTP!' -geometry 90x30+1920+1080 -e {}".format(command))

'''

class nmapScan:
    '''
    __INIT__ :
    Initiate the nmap3 object and host variable.
    Do an -sV scan and save it to self.result.
    Format the result into a list self.openPorts.

    '''

    def __init__(self, host, rootDir, *args, **kwargs):
        global Debug  # Boolean to skip nmap scan
        Debug = kwargs.get('Debug')
        try:
            os.mkdir(os.path.join(rootDir, "nmap"))
        except:
            pass
        self.rootDir = rootDir  # This is where all the files of the scan will be outputed
        #self.webServices = ["Microsoft IIS httpd", "Apache httpd", "nginx", "Apache Tomcat", "MiniServ",
         #                   "lighttpd","Microsoft HTTPAPI httpd","http-proxy",'httpd','http']
        self.webServices = ["http-proxy",'httpd','http']
        # Let's only do common webservices.
        self.host = host
        self.nmap = nmap3.Nmap()
        if Debug == True:
            self.result = {'192.168.241.116': {'osmatch': {}, 'ports': [{'protocol': 'tcp', 'portid': '22', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '63', 'service': {'name': 'ssh', 'product': 'OpenSSH', 'version': '7.4', 'extrainfo': 'protocol 2.0', 'method': 'probed', 'conf': '10'}, 'cpe': [{'cpe': 'cpe:/a:openbsd:openssh:7.4'}], 'scripts': []}, {'protocol': 'tcp', 'portid': '80', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '63', 'service': {'name': 'http', 'product': 'Apache httpd', 'version': '2.4.6', 'extrainfo': '(CentOS)', 'method': 'probed', 'conf': '10'}, 'cpe': [{'cpe': 'cpe:/a:apache:http_server:2.4.6'}], 'scripts': []}, {'protocol': 'tcp', 'portid': '139', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '63', 'service': {'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: SAMBA', 'hostname': 'CASSIOS', 'method': 'probed', 'conf': '10'}, 'cpe': [{'cpe': 'cpe:/a:samba:samba'}], 'scripts': []}, {'protocol': 'tcp', 'portid': '445', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '63', 'service': {'name': 'netbios-ssn', 'product': 'Samba smbd', 'version': '3.X - 4.X', 'extrainfo': 'workgroup: SAMBA', 'hostname': 'CASSIOS', 'method': 'probed', 'conf': '10'}, 'cpe': [{'cpe': 'cpe:/a:samba:samba'}], 'scripts': []}, {'protocol': 'tcp', 'portid': '8080', 'state': 'open', 'reason': 'syn-ack', 'reason_ttl': '63', 'service': {'name': 'http-proxy', 'servicefp': 'SF-Port8080-TCP:V=7.91%I=7%D=5/12%Time=609C7365%P=x86_64-pc-linux-gnu%r(GetRequest,429,"HTTP/1\\.1\\x20200\\x20\\r\\nX-Content-Type-Options:\\x20nosniff\\r\\nX-XSS-Protection:\\x201;\\x20mode=block\\r\\nCache-Control:\\x20no-cache,\\x20no-store,\\x20max-age=0,\\x20must-revalidate\\r\\nPragma:\\x20no-cache\\r\\nExpires:\\x200\\r\\nX-Frame-Options:\\x20DENY\\r\\nContent-Type:\\x20text/html;charset=UTF-8\\r\\nContent-Language:\\x20en-US\\r\\nDate:\\x20Thu,\\x2013\\x20May\\x202021\\x2000:28:33\\x20GMT\\r\\nConnection:\\x20close\\r\\n\\r\\n<!doctype\\x20html>\\n<html\\x20lang=\\"en\\">\\n\\n<head>\\n\\x20\\x20<meta\\x20charset=\\"utf-8\\">\\n\\x20\\x20<meta\\x20http-equiv=\\"x-ua-compatible\\"\\x20content=\\"ie=edge\\">\\n\\x20\\x20<meta\\x20name=\\"viewport\\"\\x20content=\\"width=device-width,\\x20initial-scale=1\\">\\n\\n\\x20\\x20<title></title>\\n\\n\\x20\\x20<link\\x20rel=\\"stylesheet\\"\\x20href=\\"/css/main\\.css\\">\\n\\x20\\x20\\n</head>\\n\\n<body>\\n\\t\\n\\t<div\\x20class=\\"small-container\\">\\n\\t\\t<div\\x20class=\\"flex-row\\">\\n\\t\\t\\t<h1>Recycler\\x20Management\\x20System</h1>\\n\\t\\t</div>\\n\\t\\t<div\\x20class=\\"flex-row\\">\\n\\t\\t\\t<img\\x20src=\\"/images/factory\\.jpg\\"\\x20class=\\"round-button\\">\\n\\t\\t</div>\\x20\\n\\n\\t</div>\\n\\t<br>\\n\\t<div\\x20class=\\"small-container\\">\\n\\n\\t\\t\\t<div\\x20class=\\"flex-small\\">Control\\x20system\\x20for\\x20the\\x20factory\\x20")%r(HTTPOptions,12B,"HTTP/1\\.1\\x20200\\x20\\r\\nAllow:\\x20GET,HEAD,OPTIONS\\r\\nX-Content-Type-Options:\\x20nosniff\\r\\nX-XSS-Protection:\\x201;\\x20mode=block\\r\\nCache-Control:\\x20no-cache,\\x20no-store,\\x20max-age=0,\\x20must-revalidate\\r\\nPragma:\\x20no-cache\\r\\nExpires:\\x200\\r\\nX-Frame-Options:\\x20DENY\\r\\nContent-Length:\\x200\\r\\nDate:\\x20Thu,\\x2013\\x20May\\x202021\\x2000:28:33\\x20GMT\\r\\nConnection:\\x20close\\r\\n\\r\\n")%r(RTSPRequest,24E,"HTTP/1\\.1\\x20400\\x20\\r\\nContent-Type:\\x20text/html;charset=utf-8\\r\\nContent-Language:\\x20en\\r\\nContent-Length:\\x20435\\r\\nDate:\\x20Thu,\\x2013\\x20May\\x202021\\x2000:28:33\\x20GMT\\r\\nConnection:\\x20close\\r\\n\\r\\n<!doctype\\x20html><html\\x20lang=\\"en\\"><head><title>HTTP\\x20Status\\x20400\\x20\\xe2\\x80\\x93\\x20Bad\\x20Request</title><style\\x20type=\\"text/css\\">body\\x20{font-family:Tahoma,Arial,sans-serif;}\\x20h1,\\x20h2,\\x20h3,\\x20b\\x20{color:white;background-color:#525D76;}\\x20h1\\x20{font-size:22px;}\\x20h2\\x20{font-size:16px;}\\x20h3\\x20{font-size:14px;}\\x20p\\x20{font-size:12px;}\\x20a\\x20{color:black;}\\x20\\.line\\x20{height:1px;background-color:#525D76;border:none;}</style></head><body><h1>HTTP\\x20Status\\x20400\\x20\\xe2\\x80\\x93\\x20Bad\\x20Request</h1></body></html>");', 'method': 'probed', 'conf': '10'}, 'scripts': []}], 'hostname': [], 'macaddress': None, 'state': {'state': 'up', 'reason': 'echo-reply', 'reason_ttl': '63'}}, 'stats': {'scanner': 'nmap', 'args': '/usr/bin/nmap -oX - -sV -p- -oN /home/Kyand/OSPG/Cassios/reconScript/nmap/nmap_scan.txt 192.168.241.116', 'start': '1620865849', 'startstr': 'Wed May 12 20:30:49 2021', 'version': '7.91', 'xmloutputversion': '1.05'}, 'runtime': {'time': '1620865901', 'timestr': 'Wed May 12 20:31:41 2021', 'summary': 'Nmap done at Wed May 12 20:31:41 2021; 1 IP address (1 host up) scanned in 51.31 seconds', 'elapsed': '51.31', 'exit': 'success'}}
        else:
            print("[!] nmap scan is running...\n")
            self.result = self.nmap.nmap_version_detection(self.host, args="-p- -oN {}/nmap/nmap_scan.txt".format(
                rootDir))  # -sV -p- -oN (rootDir/nmap_scant.txt) scan
            print("[!] nmap scan has completed!\n")
            #print(self.result)
        self.openPorts = []
        for ports in self.result[self.host]["ports"]:
            self.openPorts.append(ports)

    def tbruteSMB(self):
        global bruteSMBcmd
        try:
            os.mkdir("{}/brute".format(rootDir))  # Creates the "brute" directory
        except:
            pass
        bruteSMBcmd = "hydra -t 1 -L ./wordlist/top-usernames-shortlist.txt -P ./wordlist/UserPassCombo-Jay.txt -V {} smb -o {}/brute/SMB.txt -I".format(
            host, rootDir)

        #os.system("xterm -T 'bruteforcing SMB!' -geometry 100x100 -hold -e {}".format(cords, command))

    def tsmbCheck(self):
        global smbCheckCmd
        smbCheckCmd = "python3 smbCheck.py --host {} --output {}".format(self.host, self.rootDir)

    '''
    Runs funct
    '''

    def check(self, dWordList):
        global SSL
        global allBrute
        for port in self.result[self.host]['ports']:
            number = port['portid']
            if number == "443":
                SSL = True
            else:
                SSL = False

        self.dirbust(dWordList)  # Does dirbust AND extracts comments
        for port in self.result[self.host]['ports']:
            number = port['portid']
            if number == "21":
                self.checkFTP()
            elif number == "22":
                if allBrute == 1:
                    self.tBruteSSH()
                else:
                    answ = input("[!] Do you wish to bruteforce SSH? (y/n)\n")
                    if answ == "y":
                        self.tBruteSSH()
                    else:
                        pass
                pass
            
            elif number == "445":
                if allBrute == 1:
                    self.tbruteSMB()
                else:
                    answ = input("[!] Do you wish to bruteforce SMB? (y/n)\n")
                    if answ == "y":
                        self.tbruteSMB()
                    else:
                        pass
                self.tsmbCheck()
                pass
            else:
                pass

    '''
    portScan:
    Simply returns the list of openPorts

    Example use :

    host = "10.10.10.204"
    result = nmapScan(host).listOpenPorts()
    for r in result:
        print(r)    
    '''

    def listOpenPorts(self):
        return self.openPorts

    def tBruteSSH(self):
        global bruteSSHcmd
        try:
            os.mkdir("{}/brute".format(self.rootDir))  # Creates the "brute" directory
        except:
            pass
        bruteSSHcmd = "hydra -t 1 -L ./wordlist/top-usernames-shortlist.txt -P ./wordlist/UserPassCombo-Jay.txt -V {} smb -o {}/brute/SMB.txt -I".format(
            self.host, self.rootDir)
        #os.system("xterm -T 'bruteforcing SMB!' -geometry 100x100 -hold -e {}".format(cords, command))

    def tBruteFTP(self):
        global bruteFTPcmd
        try:
            os.mkdir("{}/brute".format(self.rootDir))  # Creates the "brute" directory
        except:
            pass
        bruteFTPcmd = "hydra -s 21 -t 20 -L ./wordlist/top-usernames-shortlist.txt -P ./wordlist/UserPassCombo-Jay.txt -vV ftp://{} -o {}/brute/FTP.txt -I ".format(
            self.host, self.rootDir)
        #os.system("xterm -T 'bruteforcing FTP!' -geometry 90x30+1920+1080 -e {}".format(command))
    '''
    Do regular FTP checks (check anon login, check perms)

    '''

    def checkFTP(self):
        global allBrute
        rootDir = os.path.join(self.rootDir, "ftp")  # /ftp directory
        try:
            os.mkdir(os.path.join(self.rootDir, "ftp"))  # Create /ftp directory
        except:
            pass
        f = open("{}/results.txt".format(rootDir), "w+")  # Create results.txt file
        ftp = FTP(self.host)  # initate ftp object
        try:  # Check anonymous login
            ftp.login()
            f.write("Ftp anonymous : [WORKS]\n")
            f.close()
            if allBrute == 1:
                self.tBruteFTP()
            else:
                answ = input("[!] FTP anonymous works, do you still want to bruteforce it? (y/n)\n")
                if answ == "y":
                    self.tBruteFTP()
                else:
                    pass
            try:  # test file upload (creates test.jpg, trys to upload it, removes it, writes in results.txt)
                fileTest = open('test.jpg', 'w+')
                ftp.storbinary('STOR kitten.jpg', fileTest)
                fileTest.close()
                os.remove('test.jpg')
                f = open("{}/results.txt".format(rootDir), "a")
                f.write("File upload : [WORKS]\n")
                f.close()

            except:
                f = open("{}/results.txt".format(rootDir), "a")
                f.write("File upload : [FAILED]\n")
                f.close()
    


        except:
            f.write("Ftp anonymous : [FAILED]\n")
            f.close()
            pass

    '''
    Returns dictionary of PORT:SERVICE_NAME

    Example use :

    host = "10.10.10.204"
    result = nmapScan(host).services()
    print(result)
    '''

    def listServices(self):
        self.servicesDict = {}
        for port in self.openPorts:
            try:  # If dictionary does not have "product" key, skip. (Theres probably a better way to do this)
                self.servicesDict[port['portid']] = port['service']['name']
            except:
                pass
        return self.servicesDict  # dictionary PORT:SERVICE_NAME

    '''
    Used by dirbust function, creates log files. (Full path + name which is PORT_dirbust.txt)

    '''

    def createLogFiles(self, dir):
        self.logFiles = []  # list of full path
        try:
            os.mkdir(os.path.join(dir, "dirbust"))
        except:
            pass
        for url in self.urls:  # Creates full path
            if SSL == True:
                port = "SSL"
            else:
                port = url.split(":")[2]
            name = "{}.txt".format(port)
            self.logFiles.append("{}/dirbust/{}".format(dir, name))
        return self.logFiles  # Return list

    '''
    This is the function that when called, will run a dirbuster on each webservice.

    It needs a wordlist file, thats it!

    Needs https support to be added.
    '''

    def dirbust(self, wordfile):
        self.webServicePorts = []  # list of ports that are running http services
        self.urls = []  # list of url + port ready to dirbust.
        serviceList = self.listServices()  # Gets a list of the services.
        for port in serviceList:
            if serviceList[port] in self.webServices:  # If service_name is a web service
                self.webServicePorts.append(port)  # append the port to list
            else:
                pass
        for port in self.webServicePorts:  # Create url for dirbust.
            if SSL == True:
                if port == "80":
                    url = "https://{}".format(self.host)
                else:
                    url = "https://{}:{}".format(self.host, port)
            else:
                url = "http://{}:{}".format(self.host, port)
            self.urls.append(url)
        logFiles = self.createLogFiles(self.rootDir)  # Creates logFile Paths
        dirbuster(self.urls, wordfile, logFiles, self.rootDir)  # Starts the threads


if __name__ == '__main__':
    global allBrute
    '''
    Argparse stuff (Comment out when debugging)

    '''

    parser = argparse.ArgumentParser(description="ReconScript")
    parser.add_argument('-I', '--host', type=str, metavar='', required=True, help='IP Address of the host')
    parser.add_argument('-o', '--output', type=str, metavar='', required=True,
                        help='Output directory for scan (Full Path) (Example : /home/user/)')
    parser.add_argument('-w', '--wordlist', type=str, metavar='', required=True, help='Wordlist to use for dirbust')
    parser.add_argument('-a', '--all', action="store_true", required=False,
                        help='--all if you want to bruteforce all (Does not prompt)')
    args = parser.parse_args()
    if args.all:
        allBrute = 1
        print("[!] Will bruteforce everything that is bruteforcable! Good luck :)\n")
    else:
        allBrute = 0

    host = args.host
    rootDir = os.path.join(args.output, "reconScript")  # path to create directory
    try:  # Check if it exists (THeres a better way to do it!)
        os.mkdir(rootDir)
    except:
        print("[!] {} Already exists, will output everything there.\n".format(rootDir))
        pass
    wordlist = args.wordlist
    result = nmapScan(host, rootDir, Debug=False).check(wordlist)  # Regular portScan



    import tkinter as tk
    root = tk.Tk()
    app = NewprojectApp(root)
    app.run()


# ! /usr/bin/python
#coding=utf-8
#Author: Amanda Shan <chfshan@grandstream.cn>;jhai@grandstream.cn
import sys
import copy
from _symtable import LOCAL
sys.path.append(r'.')
# from CycleRunCase import *
# import CycleRunCase
import unittest
import os
import socket
import struct
import re
import time,datetime
import random
import signal
import array
import threading
import hashlib,md5
import json
import subprocess
from optparse import OptionParser
# import ssl
# from OpenSSL import SSL
# from M2Crypto import RSA
# import HTMLTestRunner

##################################################
# common variable
##################################################
global caseResult,caseLog
caseResult = ""
caseLog = ""
global case_Report_Manager
global LOCAL_PC_IP,LOCAL_PC_PORT
global MEETINNG_ROOM_ID,MEETING_PASSWORD
global VERBOSE,service_on
VERBOSE = 0   ## is open debug log
service_on = 1

##################################################
# Web server use, SIP test will call Web server
##################################################
global WEB_SERVER_IP,WEB_SERVER_PORT,LOGIN_WEB_ACCOUNT,LOGIN_WEB_ACCOUNT_PASSWORD
WEB_SERVER_IP=WEB_SERVER_PORT=LOGIN_WEB_ACCOUNT=LOGIN_WEB_ACCOUNT_PASSWORD=''
global APPID_FOR_WEBAPI_TEST,SECRETKEY_FOR_WEBAPI_TEST
APPID_FOR_WEBAPI_TEST = 10004
SECRETKEY_FOR_WEBAPI_TEST = "FE2DF5E80FDE4226957AA100CBBA627C"
global LOOPTIMES_webAPI_errorCode
LOOPTIMES_webAPI_errorCode = 1
global WEBAPI_KEY_URL

##################################################
# just for SIP server use
##################################################
global SIP_SERVER_IP,SIP_SERVER_PORT
global is_Exception_test
is_Exception_test = 0
global XSERVER_PUBLICKEY,XSERVER_RESPOND
XSERVER_PUBLICKEY = {}.fromkeys(('cseq_num_all'),"NONE") # every sip command vi this key to parse
XSERVER_PUBLICKEY["cseq_num_all"] = 0
XSERVER_RESPOND = {}.fromkeys(("call_id",'cseq_num','invite_to_tag_str',"body","x_gs_notify_users","x_gs_conf_control"),"NONE")
# INVITE:INVITE_to_tag , SIPID:SIPpassword
XSERVER_INVITE = {}
SESSIONINFO = []
LOOPTIMES_Xserver_errorCode = 1
global SIP_ID_NUMBER,SIP_ID_PASSWORD,LOCAL_PC_RTP_PORT
global INVITE_SDP
INVITE_SDP = {}.fromkeys(("ip","port1",'port2',"port3","port4","port5"),"NONE")


## SESSIONINFO.append({'fromuser':self.fromuser,'call_id':invite_call_id_str,'fromtag':from_tag_str,'totag':'None'})

#################################################

###########################
####Author:chfshan
####Test Case commonlib，design for every test case need run with "def run()" step
####
###########################
class projectx_base(unittest.TestCase):
    def __init__(self,AUTHOR = "chfshan",moduleID = "projectx",caseID = "0000001"):
        self.AUTHOR=AUTHOR
        self.startTime = time.strftime('%H%M%S')
        self.moduleID = moduleID
        self.caseID = caseID
    def OnSetUp(self):
        pass
    def OnTearDown(self):
        pass
    def OnError(self):
        pass
    def OnFail(self):
        pass
    def Run(self):
        self.OnSetUp()
        self.OnRun()
        self.OnTearDown()
    def OnRun(self):
        pass

###########################
####Author:chfshan
####init sip packet, every send func supplied by sipServer_commonlib, need pass this class 
####part if value define :
####protocol: the sip message is passed by this protocol
####sdp: INVITE all sdp content
####sipid_number: from user
####meeting_id_to_user: to user
###########################
class create_sipObject(object):
    """Basic representation of a snom phone."""
    def __init__(self, isReq=False, ip='', port='', ip2='', port2=5060, pkt=None):
        global LOGIN_WEB_ACCOUNT,LOGIN_WEB_ACCOUNT_PASSWORD
        """add for Grandstream-projectX by Amanda"""
        self.x_gs_notify_users = "NONE"
        self.x_gs_conf_control = "NONE"
        self.x_gs_server_id = "NONE"
        self.meeting_pw = 'NONE'
        self.user_agent = ''
        self.display_name = ''
        self.web_server_ip = ''
        self.web_server_port = ''
        self.webserver_account = ''
        self.webserver_account_pw = ''
        """Default constructor."""
        self.msg_isReq = isReq
        self.dest_ip_number = ip
        self.dest_ip_domain_name = ''
        self.dest_port_number = port
        self.local_ip_number = ip2
        self.local_port_number = port2
        self.rtp_media_port = 10000
        self.msg_method = 'NONE'
        self.msg_pkt = pkt 
        self.call_id = 'NONE'
        self.cseq = 'NONE'
        self.cseq_num = 1
        self.via_header = 'NONE'
        self.from_header = 'NONE'
        self.to_header = 'NONE'
        self.meeting_id_to_user = 'NONE'
        self.to_host = 'NONE'
        self.to_port = 5060
        self.sipid_number = 'NONE'
        self.sipid_password = 'NONE'
        self.sdp_remoteHost = '0.0.0.0'
        self.sdp_remotePort = 10000
        self.statusCode = 100
        self.hastotag = False
        self.fromtag = '00000000'
        self.totag = '00000000'
        self.body = 'NONE'
        self.bHasBody = False
        self.contentType = 'NONE'
        self.statusPhase = 'NONE'
        self.branchStr = 'NONE'
        self.snd_via_header = 'NONE'
        self.third_via_header = 'NONE'
        self.refer_to_header = 'NONE'
        self.referred_by_header = 'NONE'
        self.eventType = 'NONE'
        self.subscriptionState = 'NONE'
        self.replaces = 'NONE'
        self.bContactWithUser = False
        self.expires_value = 60
        self.expires_header = 'NONE'
        self.sessionExpires = 'NONE'
        self.minSE = 'NONE'
        self.requires = 'NONE'
        self.supported = 'NONE'
        self.rSeq = 'NONE'
        self.rAck = 'NONE'
        self.call_info_header = 'NONE'
        self.alert_info_header = 'NONE'
        self.sessExpires_time_value = 0
    #0-none, 1-uac, 2-uas
        self.sessExpires_refresher_value = 0
        self.minSE_time_value = 0
    # 0 - blf, 1 - eventlist blf
        self.blf_type = 0 
    # 0 - disabled, 1 - enabled
        self.bCompact = 0 
    # 0 - disabled, 1 - enabled
        self.ppi_header = 'NONE'
        self.ppi_user = 'NONE'
        self.bPrivacyRequired = False
        self.ReferType = 0
        self.contact_header = 'NONE'
        self.diversion_header = 'NONE'
        self.sdp_ptime_param_string = 'NONE'
        self.first_audio_codec_type = -1
        self.first_audio_codec_rtpmap_param = 'NONE'
        self.first_video_codec_type = -1
        self.first_video_codec_rtpmap_param = 'NONE'
        self.first_video_codec_fmtp_param = 'NONE'
        self.authorization_header = 'NONE'
        self.www_authenticate_header = 'NONE'
        self.proxy_authorization_header = 'NONE'
        self.proxy_authenticate_header = 'NONE'
        self.realm = 'NONE'
        self.nonce = 'NONE'
#         self.username = 'NONE'
        self.ruri = 'NONE'
        self.allow_header = 'NONE'
        self.callee_mode = False
        self.protocol = 'tcp'
        self.isSrtp = 0
        self.sdp = 'NONE'

###########################
####Author:chfshan
####print log , if VERBOSE=1, will print
####
###########################       
def debug_print(buffer1, VERBOSE = 1):
    if VERBOSE == 1:
        print buffer1
###########################
####Author:chfshan
####stop script
####
########################### 
def exitScript():
    sys.exit()
    
###########################
####Author:chfshan
####case end , set the Case result
####
########################### 
def setCaseResult(buffer,ModuleID = "", caseID = ""):
    global caseResult
    print "case result = %s" % (str(buffer))
    caseResult = str(buffer)

def addCaseLog(buffer,ModuleID = "", caseID = ""):
    global caseLog
#     a = datetime.datetime.now() 
#     b = a.strptime("%Y%m%d%H%M%S")
    b = time.strftime('%Y%m%d%H%M%S')
    print str(b) + ": %s" %(str(buffer))
    caseLog = str(b) + ":" + str(buffer) + "\r\n"

###########################
####Author:chfshan
####get local ip address
####
########################### 
def get_ip_address():
    #get local ip address
    localIP = socket.gethostbyname(socket.gethostname())
    addCaseLog("getted your localIP = %s (get_ip_address)" % localIP )
    #get other ip addresses
    ipList = socket.gethostbyname_ex(socket.gethostname())
    for i in ipList:
        if i != localIP:
            debug_print( "extra local IP:%s" %i,VERBOSE)
    return localIP

###########################
####Author:chfshan
####create one socket and connect to (destserver_address,destserver_port) server, connect protocol setted by parameter: protocol
####parameter:
####return:
####return the success created socket
########################### 
def connectServer(destserver_address = "", destserver_port="" ,localip_address = "" ,local_portaddr = "" , protocol = ""):
    global LOCAL_PC_IP,LOCAL_PC_PORT,SIP_SERVER_IP,SIP_SERVER_PORT
    if local_portaddr == "":
        local_portaddr = int(LOCAL_PC_PORT)
    if not localip_address:
        localip_address = LOCAL_PC_IP
    if not destserver_address:
        destserver_address = SIP_SERVER_IP
    if not destserver_port:
        destserver_port = int(SIP_SERVER_PORT)
    if str(protocol).lower() == 'udp':
        addCaseLog("your protocol is udp (connectServer)")
        sendsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sendsock.bind(('%s' % localip_address, int(local_portaddr)))
        sendsock.settimeout(3)
    elif str(protocol).lower() == 'ssl' or str(protocol).lower() == 'tls':
        addCaseLog("your protocol is ssl & tls (connectServer)")
        sendsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = SSL.Context(SSL.TLSv1_METHOD)
        sendsock = SSL.Connection(context, sendsock)
        dest_address = socket.getaddrinfo(destserver_address, int(destserver_port))[0][4][0]
        
        # Connect the socket to the port where the server is listening
#         server_address = (destserver_address, int(destserver_port))
        try:
            sendsock.connect((dest_address, destserver_port))
            sendsock.do_handshake()
        except socket.error or socket.timeout:
            sendsock.close()
            addCaseLog("connect to %s failed (connectServer)"% str(dest_address))
        sendsock.settimeout(1)
        addCaseLog("connect to %s:%s success (connectServer)"% (str(dest_address),str(destserver_port)))

    else:
        addCaseLog("your protocol is tcp (connectServer)")
        sendsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        server_address = (destserver_address, int(destserver_port))
        try:
            sendsock.connect(server_address)
        except socket.error or socket.timeout:
            sendsock.close()
            addCaseLog("connect to %s failed (connectServer)"% str(server_address))
#         sendsock.settimeout(1)
        addCaseLog("connect to %s:%s success (connectServer)"%server_address)
    return sendsock

###########################
####Author:chfshan
####common method of connection with sip
####
###########################

class sipServer_commonlib(threading.Thread):
    def __init__(self, client_param):
        threading.Thread.__init__(self)
        global LOCAL_PC_IP,LOCAL_PC_RTP_PORT,MEETING_PASSWORD,SIP_ID_NUMBER,SIP_ID_PASSWORD,LOGIN_WEB_ACCOUNT,LOGIN_WEB_ACCOUNT_PASSWORD,WEB_SERVER_IP,WEB_SERVER_PORT
        global MEETINNG_ROOM_ID
        self.localsock = ''
        if client_param.local_port_number == "" or str(client_param.local_port_number).lower() == 'none':
            self.localport = client_param.local_port_number = LOCAL_PC_PORT
        else:
            self.localport = client_param.local_port_number
        
        if client_param.local_ip_number =="" or str(client_param.local_ip_number).lower() == 'none':
            self.localip = client_param.local_ip_number = LOCAL_PC_IP
        else:
            self.localip = client_param.local_ip_number

        if client_param.sipid_number == "" or str(client_param.sipid_number).lower() == 'none':
            self.fromuser = client_param.sipid_number=  SIP_ID_NUMBER
        else:
            self.fromuser = client_param.sipid_number
        if client_param.sipid_password == "" or str(client_param.sipid_password).lower() == 'none':
            self.sipid_password = client_param.sipid_password=  SIP_ID_PASSWORD
        else:
            self.sipid_password = client_param.sipid_password
        self.dest_ip_domain_name = client_param.dest_ip_domain_name
        if client_param.meeting_id_to_user ==""  or str(client_param.meeting_id_to_user).lower() == 'none':
            self.touserOrmeetingID = client_param.meeting_id_to_user = MEETINNG_ROOM_ID
        else:
            self.touserOrmeetingID = client_param.meeting_id_to_user
        if str(client_param.meeting_pw).lower() == 'none':
            self.meeting_pw =client_param.meeting_pw= MEETING_PASSWORD
        else:
            self.meeting_pw = client_param.meeting_pw
        if client_param.dest_ip_number == "" or str(client_param.dest_ip_number).lower() == 'none':
            self.dest_address =client_param.dest_ip_number = SIP_SERVER_IP
        else:
            self.dest_address = client_param.dest_ip_number
        if client_param.dest_port_number == "" or str(client_param.dest_port_number).lower() == 'none':
            self.dest_port = client_param.dest_port_number =SIP_SERVER_PORT
        else:
            self.dest_port = client_param.dest_port_number
        if client_param.user_agent == "" or str(client_param.user_agent).lower() == 'none':
            self.user_agent = client_param.user_agent ='windows'
        else:
            self.user_agent = client_param.user_agent
        if client_param.display_name == "" or str(client_param.display_name).lower() == 'none':
            self.display_name = client_param.display_name = 'python'
        else:
            self.display_name = client_param.display_name
        if client_param.rtp_media_port == "":
            self.rtp_port = client_param.rtp_media_port =LOCAL_PC_RTP_PORT
        else:
            self.rtp_port = client_param.rtp_media_port            
        self.header_name_compact_format_dictionary =  dict((['Call-ID', 'i'], ['Contact', 'm'], ['Content-Encoding', 'e'], ['Content-Length', 'l'], ['Content-Type', 'c'], ['From', 'f'], ['Subject', 's'], ['To', 't'], ['Via', 'v'], ['Supported', 'k'], ['Session-Expires', 'x']))            
        self.content_of_x_gs_conf_contorl = ""
        self.chat_to_users = "all"
        self.chat_content = "%s send test messages from python tool"%(self.fromuser)
        self.protocol = client_param.protocol
        if client_param.web_server_ip == "":
            self.webserver = client_param.web_server_ip =WEB_SERVER_IP
        else:
            self.webserver = client_param.web_server_ip
        if client_param.web_server_port == "":
            self.webserver_port = client_param.web_server_port =WEB_SERVER_PORT
        else:
            self.webserver_port = client_param.web_server_port
        if client_param.webserver_account == "":
            self.webserver_account = client_param.webserver_account =LOGIN_WEB_ACCOUNT
        else:
            self.webserver_account = client_param.webserver_account
        if client_param.webserver_account_pw == "":
            self.webserver_account_pw = client_param.webserver_account_pw =LOGIN_WEB_ACCOUNT_PASSWORD
        else:
            self.webserver_account_pw = client_param.webserver_account_pw
        self.receivedPacket = ""
        self.callID = ""
#         self.OnSetUp()
        addCaseLog("your sip account password = %s (sipServer_commonlib)" % self.sipid_password)
        self.sdp = client_param.sdp
        self.isSrtp = client_param.isSrtp
        self.object = client_param

###########################
####Author:chfshan
####send bye to peer
####parameter:
####msg_info: should create by class create_sipObject and init every value that you want sent to peer
####sock: this 'bye' will send vi this socket ,you can create by function:connectServer
####
###########################           
    def send_BYE(self,sock,msg_info):
        bye_request = "BYE sip:%s@%s:%d SIP/2.0\r\n"%(msg_info.meeting_id_to_user, msg_info.dest_ip_number, int(msg_info.dest_port_number))
        if msg_info.protocol == 'udp':
            bye_request += "Via: SIP/2.0/UDP %s:%d;branch=z9hG4bK12345678%x"%(str(msg_info.local_ip_number),int(msg_info.local_port_number), random.randint(0, 10000)) + "\r\n"
            bye_request += "Contact: <sip:" + str(msg_info.local_ip_number) + ":" + "%d"%int(msg_info.local_port_number) + ";transport=udp>\r\n"
        else:
            bye_request += "Via: SIP/2.0/TCP %s:%d;branch=z9hG4bK12345678%x"%(str(msg_info.local_ip_number),int(msg_info.local_port_number), random.randint(0, 10000)) + "\r\n"
            bye_request += "Contact: <sip:" + str(msg_info.local_ip_number) + ":" + "%d"%int(msg_info.local_port_number) + ";transport=tcp>\r\n"
        bye_request += "To: <sip:%s@%s:%d>;tag=%s\r\n"%(msg_info.meeting_id_to_user, msg_info.dest_ip_number, msg_info.dest_port_number, msg_info.totag)
        bye_request += "From: <sip:%s@%s:%d>;tag=%s\r\n"%(msg_info.sipid_number, str(msg_info.local_ip_number), int(msg_info.local_port_number), msg_info.fromtag)
        bye_request += "Call-ID: %s\r\n"%msg_info.call_id
        bye_request += "CSeq: %d BYE\r\n" % msg_info.cseq_num
        bye_request += "Content-Length: 0\r\n\r\n"
        if msg_info.protocol == 'udp':
            sock.sendto(bye_request, (msg_info.dest_ip_number, msg_info.dest_port_number))
        else:
            try:
                sock.sendall(bye_request)
            except Exception as e:
                addCaseLog("send bye failed,socket connect failed: %s(send_Bye)" % (str(e)))
                self.OnError()
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1

    def send_INFO(self,sock,msg_info,content_of_x_gs_conf_contorl=""):
        msg_info = self.checkAndInitData(sock, msg_info)
        if msg_info == False:
            self.OnError()
        msg_info.fromtag="%x"%random.randint(0, 10000)
        msg_info.call_id="1701338429%x@%s-%d"%(random.randint(0, 10000),self.localip,self.localport)
        msg_info.cseq_num = XSERVER_PUBLICKEY["cseq_num_all"]

        if content_of_x_gs_conf_contorl == "":
            addCaseLog("content_of_x_gs_conf_contorl is empty (send_INFO)")
        msg_info.msg_method = "INFO"
        sip_request = "%s sip:%s@%s:%d SIP/2.0\r\n"%(msg_info.msg_method, msg_info.meeting_id_to_user, msg_info.dest_ip_number, msg_info.dest_port_number)
    
        if msg_info.protocol == 'udp':
            sip_request += "Via: SIP/2.0/UDP %s:%d;branch=z9hG4bK12345678%x"%(msg_info.local_ip_number,msg_info.local_port_number, random.randint(0, 10000)) + "\r\n"
            sip_request += "Contact: <sip:" + str(msg_info.local_ip_number) + ":" + "%d"%msg_info.local_port_number + ";transport=udp>\r\n"
        else:
            sip_request += "Via: SIP/2.0/TCP %s:%d;branch=z9hG4bK12345678%x;rport;alias"%(msg_info.local_ip_number,msg_info.local_port_number, random.randint(0, 10000)) + "\r\n"
            sip_request += "Contact: <sip:" + str(msg_info.sipid_number) + "@" + str(msg_info.local_ip_number) + ":" + "%d"%msg_info.local_port_number + ";transport=tcp>\r\n"

        if msg_info.hastotag == True:
            sip_request += "To: <sip:%s@%s:%d>;tag=%s\r\n"%(msg_info.meeting_id_to_user, msg_info.dest_ip_number, msg_info.dest_port_number, msg_info.totag)
        else:
            sip_request += "To: <sip:%s@%s:%d>\r\n"%(msg_info.meeting_id_to_user, msg_info.dest_ip_number, msg_info.dest_port_number)
    
        sip_request += "From: <sip:%s@%s:%d>;tag=%s\r\n"%(msg_info.sipid_number, msg_info.local_ip_number, msg_info.local_port_number, msg_info.fromtag)
        sip_request += "Call-ID: %s\r\n"%msg_info.call_id
        sip_request += "CSeq: %d %s\r\n" %(msg_info.cseq_num, msg_info.msg_method)

        if self.compare_string(msg_info.authorization_header, 'NONE') != 0:
            sip_request += "Authorization: %s\r\n"%msg_info.authorization_header;
        elif self.compare_string(msg_info.proxy_authorization_header, 'NONE') != 0:
            sip_request += "Proxy-Authorization: %s\r\n"%msg_info.proxy_authorization_header;

#####    added by Amandashan start
        sip_request += "User-Agent: %s \r\n"%(msg_info.user_agent)
        sip_request += "Max-Forwards: 70 \r\n"
#####    added by Amandashan end
        sip_request += "X-GS-Conf-Control: %s\r\n" % (content_of_x_gs_conf_contorl)
        sip_request += "Content-Length: 0\r\n\r\n"
    
        if msg_info.protocol == 'udp':
            sock.sendto(sip_request, (msg_info.dest_ip_number, msg_info.dest_port_number))
        else:
            try:
                sock.sendall(sip_request)
            except Exception as e:
                addCaseLog("send INFO %s  failed,socket connect failed: %s(send_INFO)") % (content_of_x_gs_conf_contorl,str(e))
                self.OnError()
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1

    def compare_string(self,buffer1, buffer2):
        #print "[%s][%s]"%(buffer1, buffer2)
        result = int(buffer1.find(buffer2))
        if result != -1:
            result = int(buffer2.find(buffer1))
            if result != -1:
                return 0
        return 1

    def send_MESSAGE(self,sock,msg_info,chat_to_users="all",chat_content="test message send from python tool"):
        method_type = "MESSAGE"
        msg_info = self.checkAndInitData(sock, msg_info)
        if msg_info == False:
            self.OnError()
        msg_info.fromtag="%x"%random.randint(0, 10000)
        msg_info.call_id="1701338429%x@%s-%d"%(random.randint(0, 10000),self.localip,self.localport)
        msg_info.cseq_num = XSERVER_PUBLICKEY["cseq_num_all"]
        
        sip_request = "%s sip:%s@%s:%d SIP/2.0\r\n"%(method_type, msg_info.meeting_id_to_user, msg_info.dest_ip_number, msg_info.dest_port_number)
        if msg_info.protocol == 'udp':
            sip_request += "Via: SIP/2.0/UDP %s:%d;branch=z9hG4bK12345678%x"%(msg_info.local_ip_number,msg_info.local_port_number, random.randint(0, 10000)) + "\r\n"
            sip_request += "Contact: <sip:" + msg_info.local_ip_number + ":" + "%d"%msg_info.local_port_number + ";transport=udp>\r\n"
        else:
            sip_request += "Via: SIP/2.0/TCP %s:%d;branch=z9hG4bK12345678%x;rport;alias"%(msg_info.local_ip_number,msg_info.local_port_number, random.randint(0, 10000)) + "\r\n"
            sip_request += "Contact: <sip:" + str(msg_info.sipid_number) + "@" + str(msg_info.local_ip_number) + ":" + "%d"%msg_info.local_port_number + ";transport=tcp>\r\n"
        
        if msg_info.hastotag == True:
            sip_request += "To: <sip:%s@%s:%d>;tag=%s\r\n"%(msg_info.meeting_id_to_user, msg_info.dest_ip_number, msg_info.dest_port_number, msg_info.totag)
        else:
            sip_request += "To: <sip:%s@%s:%d>\r\n"%(msg_info.meeting_id_to_user, msg_info.dest_ip_number, msg_info.dest_port_number)
    
        sip_request += "From: <sip:%s@%s:%d>;tag=%s\r\n"%(msg_info.sipid_number, msg_info.local_ip_number, msg_info.local_port_number, msg_info.fromtag)
        sip_request += "Call-ID: %s\r\n"%msg_info.call_id
        sip_request += "CSeq: %d %s\r\n" %(msg_info.cseq_num, method_type)
        
        if self.compare_string(msg_info.authorization_header, 'NONE') != 0:
            sip_request += "Authorization: %s\r\n"%msg_info.authorization_header;
        elif self.compare_string(msg_info.proxy_authorization_header, 'NONE') != 0:
            sip_request += "Proxy-Authorization: %s\r\n"%msg_info.proxy_authorization_header;        
        
#####    added by Amandashan start
        sip_request += "User-Agent: %s \r\n"%(msg_info.user_agent)
        sip_request += "Max-Forwards: 70 \r\n"
#####    added by Amandashan end
        sip_request += "X-GS-Message-Users: %s\r\n"%(chat_to_users)
        sip_request += "User-Agent: %s  N/A\r\n"%(msg_info.user_agent)
        sip_request += "Content-Type: text/plain;charset=utf-8\r\n"
        sip_request += "Content-Length: %d\r\n\r\n"%(len(chat_content))
        sip_request += self.chat_content
    
        if msg_info.protocol == 'udp':
            sock.sendto(sip_request, (msg_info.dest_ip_number, msg_info.dest_port_number))
        else:
            try:
                sock.sendall(sip_request)
            except Exception as e:
                addCaseLog("send request %s  failed,socket connect failed: " % (msg_info.msg_method))
                addCaseLog(e)
                self.OnError()
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1 

    def send_INVITE_response_confroom(self,sock, msg_info):
        sdp_content = "v=0\r\no=confroom 53655765 2353687637 IN IP4 %s\r\ns=-\r\nc=IN IP4 %s\r\nt=0 0\r\nm=audio %d RTP/AVP %d 101\r\n"%(msg_info.local_ip_number, msg_info.local_ip_number, int(msg_info.rtp_media_port), msg_info.first_audio_codec_type)
    
        if self.compare_string(msg_info.first_audio_codec_rtpmap_param, 'NONE') != 0:
            sdp_content += "%s\r\n"%msg_info.first_audio_codec_rtpmap_param
    
        if self.compare_string(msg_info.sdp_ptime_param_string, 'NONE') != 0:
            sdp_content += "%s\r\n"%msg_info.sdp_ptime_param_string
        sdp_content += "a=rtpmap:101 telephone-event/8000\r\n"
        
        if msg_info.first_video_codec_type != -1:
            sdp_content += "m=video %d RTP/AVP %d\r\n"%(msg_info.rtp_media_port+2, msg_info.first_video_codec_type)
            if self.compare_string(msg_info.first_video_codec_rtpmap_param, 'NONE') != 0:
                sdp_content += "%s\r\n"%msg_info.first_video_codec_rtpmap_param
            if self.compare_string(msg_info.first_video_codec_fmtp_param, 'NONE') != 0:
                sdp_content += "%s\r\n"%msg_info.first_video_codec_fmtp_param
    
        ok_response = "SIP/2.0 200 OK\r\n"
        ok_response += msg_info.via_header + "\r\n"
        if self.compare_string(msg_info.snd_via_header, 'NONE') != 0:
            ok_response += msg_info.snd_via_header + "\r\n"
        if self.compare_string(msg_info.third_via_header, 'NONE') != 0:
            ok_response += msg_info.third_via_header + "\r\n"
        ok_response += "Contact: <sip:%s@%s:%d;transport=udp>\r\n" % (msg_info.meeting_id_to_user, msg_info.local_ip_number, msg_info.local_port_number)
        ok_response += "Max-Forwards: 70\r\nUser-Agent: python(IPC)\r\n"
        
        if msg_info.hastotag == True:
            ok_response += "To:%s"%msg_info.to_header + "\r\n"
        else:
            ok_response += "To:<sip:%s@%s:%d>;tag=201203271%s\r\n"%(msg_info.meeting_id_to_user, msg_info.dest_ip_number, msg_info.dest_port_number, random.randint(0, 10000))
        ok_response += "From:%s\r\n"%msg_info.from_header
        ok_response += "Call-ID: %s\r\n" % msg_info.call_id
        ok_response += "CSeq: %s\r\n" %msg_info.cseq
    
        if self.compare_string(msg_info.sessionExpires, 'NONE') != 0:
            ok_response += "Session-Expires: %s\r\n" %msg_info.sessionExpires
    
        if self.compare_string(msg_info.minSE, 'NONE') != 0:
            ok_response += "Min-SE: %s\r\n" %msg_info.minSE
    
        if self.compare_string(msg_info.supported, 'NONE') != 0:
            ok_response += "Supported: %s\r\n" %msg_info.supported
    
        if self.compare_string(msg_info.requires, 'NONE') != 0:
            ok_response += "Require: %s\r\n" %msg_info.requires
    
        if msg_info.bHasBody == True:
            ok_response += "Content-Type: %s\r\n"%msg_info.contentType    
            ok_response += "Content-Length: %d\r\n\r\n"%(len(sdp_content))
            ok_response += sdp_content
        else:
            ok_response += "Content-Length: 0\r\n\r\n"
        
        debug_print( "%s\r\n"%ok_response, VERBOSE)
        debug_print( "send this message to (%s:%d)"%(msg_info.dest_ip_number, msg_info.dest_port_number), VERBOSE)    
        if msg_info.protocol == 'udp':
            sock.sendto(ok_response, (msg_info.dest_ip_number, msg_info.dest_port_number))
        else:
            try:
                sock.sendall(ok_response)
            except Exception as e:
                addCaseLog("send 200OK failed,socket connect failed: %s(send_INFO)") % (str(e))
                self.OnError()
            
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1
        return True

    def send_base_request(self,sock, method_type, msg_info, param="",chat_to_users=""):
        
        if msg_info.dest_ip_domain_name == '' or msg_info.dest_ip_domain_name == 'NONE':
            msg_info.dest_ip_domain_name = msg_info.dest_ip_number
        if chat_to_users !="":
            self.chat_to_users = chat_to_users

        sock = self.localsock
        # send SIP request to sip server
        sip_request = "%s sip:%s@%s:%d SIP/2.0\r\n"%(method_type, msg_info.meeting_id_to_user, msg_info.dest_ip_domain_name, msg_info.dest_port_number)
    
        if msg_info.protocol == 'udp':
            sip_request += "Via: SIP/2.0/UDP %s:%d;branch=z9hG4bK12345678%x"%(str(msg_info.local_ip_number).upper(),msg_info.local_port_number, random.randint(0, 10000)) + "\r\n"
            sip_request += "Contact: <sip:" + msg_info.local_ip_number + ":" + "%d"%msg_info.local_port_number + ";transport=udp>\r\n"
        else:
            sip_request += "Via: SIP/2.0/%s %s:%d;branch=z9hG4bK12345678%x;rport;alias"%(str(msg_info.protocol).upper(), msg_info.local_ip_number,msg_info.local_port_number, random.randint(0, 10000)) + "\r\n"
            sip_request += "Contact: <sip:" + str(msg_info.sipid_number) + "@" + str(msg_info.local_ip_number) + ":" + str("%d"%msg_info.local_port_number) + ";transport=" + str(msg_info.protocol).upper() + ">\r\n"    
        sip_request += "From: <sip:%s@%s:%d>;tag=%s\r\n"%(msg_info.sipid_number, msg_info.dest_ip_domain_name, msg_info.dest_port_number, msg_info.fromtag)


        if msg_info.statusCode == 401:
            sip_request += "To: <sip:%s@%s:%d>\r\n"%(msg_info.meeting_id_to_user, msg_info.dest_ip_domain_name, msg_info.dest_port_number)
            sip_request += "Authorization: %s\r\n"%msg_info.authorization_header;
        elif msg_info.statusCode == 407:
            sip_request += "To: <sip:%s@%s:%d>\r\n"%(msg_info.meeting_id_to_user, msg_info.dest_ip_domain_name, msg_info.dest_port_number)
            sip_request += "Proxy-Authorization: %s\r\n"%msg_info.proxy_authorization_header;
        elif msg_info.hastotag == True:
            sip_request += "To: <sip:%s@%s:%d>;tag=%s\r\n"%(msg_info.meeting_id_to_user, msg_info.dest_ip_domain_name, msg_info.dest_port_number, msg_info.totag)
        else:
            sip_request += "To: <sip:%s@%s:%d>\r\n"%(msg_info.meeting_id_to_user, msg_info.dest_ip_domain_name, msg_info.dest_port_number)
        sip_request += "Call-ID: %s\r\n"%msg_info.call_id
        sip_request += "Allow: INVITE, ACK, OPTIONS, CANCEL, BYE, SUBSCRIBE, NOTIFY, INFO, REFER, UPDATE, MESSAGE\r\n"
        sip_request += "User-Agent: %s\r\n" % msg_info.user_agent
        sip_request += "Supported: path\r\n"
        sip_request += "Max-Forwards: 70\r\n"
        sip_request += "CSeq: %d %s\r\n" %(msg_info.cseq_num, method_type)

        if self.compare_string(method_type, 'MESSAGE') == 0:
            sip_request += "X-GS-Message-Users: %s\r\n"%(chat_to_users)
            sip_request += "User-Agent: %s  N/A\r\n"%(msg_info.user_agent)
            sip_request += "Content-Type: text/plain;charset=utf-8\r\n"
            sip_request += "Content-Length: %d\r\n\r\n"%(len(str(param)))
            sip_request += str(param)
        elif self.compare_string(method_type, 'INFO') == 0:
    #####    added by Amandashan start
            sip_request += "User-Agent: %s \r\n"%(msg_info.user_agent)
            sip_request += "Max-Forwards: 70 \r\n"
    #####    added by Amandashan end
            sip_request += "X-GS-Conf-Control: %s\r\n"%msg_info.x_gs_conf_control
            sip_request += "Content-Length: 0\r\n\r\n"
        elif self.compare_string(method_type, 'NOTIFY') == 0:
            xml_text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<conference-info refresh=\"218\" entity=\"10000\" state=\"partial\" version=\"1\">\r\n<users><user entity=\"1000\" state=\"partial\" mute=\"0\"/>\r\n</users>\r\n</conference-info>"
            xml_text = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<conference-info %s />\r\n</users>\r\n</conference-info>" % (param)
            sip_request += "X-GS-Notify-Users: all\r\n"
            sip_request += "Content-Type: application/conference-info+xml\r\n"
            sip_request += "Event: X-GS-CONFERENCE\r\n"
            sip_request += "Content-Length: %d\r\n\r\n"%(len(xml_text))
            sip_request += xml_text
        elif self.compare_string(method_type, 'REGISTER') == 0:
            sip_request += "Expires: 3600\r\n"
            sip_request += "Content-Length: 0\r\n\r\n"
        else:
            sip_request += "Content-Length: 0\r\n\r\n"
        debug_print(sip_request, VERBOSE)
        if msg_info.protocol == 'udp':
            sock.sendto(sip_request, (msg_info.dest_ip_number, msg_info.dest_port_number))
        else:
            try:
                sock.sendall(sip_request)
            except Exception as e:
                addCaseLog("send request %s  failed,socket connect failed: %s(send_INFO)" % (method_type,str(e)))
                self.OnError()
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1

    def send_Unknown_request_response_200(self,sock, buffer, msg_info):

    
        ok_response = "SIP/2.0 200 OK\r\n"
        ok_response += msg_info.via_header + "\r\n"
        if self.compare_string(msg_info.snd_via_header, 'NONE') != 0:
            ok_response += msg_info.snd_via_header + "\r\n"
    
        ok_response += "Contact: <sip:" + msg_info.local_ip_number + ":" + "%d"%msg_info.local_port_number + ";transport=udp>\r\n"
        ok_response += "Max-Forwards: 70\r\nUser-Agent: python(IPC)\r\n"
        if msg_info.hastotag == True:
            ok_response += "To:%s"%msg_info.to_header + "\r\n"
        else:
            ok_response += "To:%s"%msg_info.to_header + ";tag=201203271"+"\r\n"
    
            msg_info.totag = "201203271"
        ok_response += "From:%s"%msg_info.from_header + "\r\n"
        ok_response += "Call-ID: %s\r\n" % msg_info.call_id
        ok_response += "CSeq: %s\r\n" %msg_info.cseq
        expiresindex1 = msg_info.expires_header.find('NONE')
        if expiresindex1 == -1:
            ok_response += "%s\r\n"%msg_info.expires_header
        ok_response += "Content-Length: 0\r\n\r\n"
    
        debug_print( "from[%s:%d] to[%s:%d]\r\n"%(msg_info.local_ip_number, msg_info.local_port_number, msg_info.dest_ip_number, msg_info.dest_port_number), VERBOSE )
        debug_print( "%s\r\n"%ok_response, VERBOSE )
        if msg_info.protocol == 'udp':
            sock.sendto(ok_response, (msg_info.dest_ip_number, msg_info.dest_port_number))
        else:
            try:
                sock.sendall(ok_response)
            except Exception as e:
                addCaseLog("send 200OK failed,socket connect failed: %s(send_INFO)") % (str(e))
                self.OnError()
            
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1
        return True
    
    def send_Unknown_request_response_404(self,sock, buffer, msg_info):

        ok_response = "SIP/2.0 404 Not Found\r\n"
        ok_response += msg_info.via_header + "\r\n"
        if self.compare_string(msg_info.snd_via_header, 'NONE') != 0:
            ok_response += msg_info.snd_via_header + "\r\n"
    
        ok_response += "Max-Forwards: 70\r\nUser-Agent: python(IPC)\r\n"
        if msg_info.hastotag == True:
            ok_response += "To:%s"%msg_info.to_header + "\r\n"
        else:
            ok_response += "To:%s"%msg_info.to_header + ";tag=201203271"+"\r\n"
    
            msg_info.totag = "201203271"
        ok_response += "From:%s"%msg_info.from_header + "\r\n"
        ok_response += "Call-ID: %s\r\n" % msg_info.call_id
        ok_response += "CSeq: %s\r\n" %msg_info.cseq
        expiresindex1 = msg_info.expires_header.find('NONE')
        if expiresindex1 == -1:
            ok_response += "%s\r\n"%msg_info.expires_header
        ok_response += "Content-Length: 0\r\n\r\n"
    
        debug_print( "from[%s:%d] to[%s:%d]\r\n"%(msg_info.local_ip_number, msg_info.local_port_number, msg_info.dest_ip_number, msg_info.dest_port_number), msg_info.VERBOSE )
        debug_print( "%s\r\n"%ok_response, msg_info.VERBOSE )
        if msg_info.protocol == 'udp':
            sock.sendto(ok_response, (msg_info.dest_ip_number, msg_info.dest_port_number))
        else:
            try:
                sock.sendall(ok_response)
            except Exception as e:
                addCaseLog("send bye failed,socket connect failed: %s(send_INFO)") % (str(e))
                self.OnError()
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1
        return True
    
######
##accept =True, will send you 200OK
#####
    def handle_Unknown_request(self,sock, buffer, msg_info, accept=True):
        if accept:
            self.send_Unknown_request_response_200(sock, buffer, msg_info)
        else:
            self.send_Unknown_request_response_404(sock, buffer, msg_info)
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1
        return 0

    def send_ACK_request(self,sock, msg_info):

        msg_info = copy.deepcopy(self.checkAndInitData(sock, msg_info))
        if msg_info == False:
            self.OnError()
    
        ack_request = "ACK sip:%s@%s:%d SIP/2.0\r\n"%(msg_info.meeting_id_to_user, msg_info.dest_ip_domain_name, msg_info.dest_port_number)
        if msg_info.statusCode == 200:
            if msg_info.protocol == 'udp':
                ack_request += "Via: SIP/2.0/UDP %s:%d;branch=z9hG4bK12345678%x;rport"%(msg_info.local_ip_number,msg_info.local_port_number, random.randint(0, 10000)) + "\r\n"
            else:
                ack_request += "Via: SIP/2.0/TCP %s:%d;branch=z9hG4bK12345678%x;rport"%(msg_info.local_ip_number,msg_info.local_port_number, random.randint(0, 10000)) + "\r\n"
        else:
            if msg_info.protocol == 'udp':
                ack_request += "Via: SIP/2.0/UDP " + msg_info.local_ip_number + ":" + "%d"%msg_info.local_port_number + ";branch=%s"%msg_info.branchStr + "\r\n"
            else:
                ack_request += "Via: SIP/2.0/TCP " + str(msg_info.local_ip_number) + ":" + "%d"%msg_info.local_port_number + ";branch=%s"%msg_info.branchStr + "\r\n"
        msg_info.bContactWithUser = True
        if msg_info.bContactWithUser == True:
            if msg_info.protocol == 'udp':
                ack_request += "Contact: <sip:%s@%s:%d;transport=udp>\r\n" % (msg_info.sipid_number, msg_info.local_ip_number, msg_info.local_port_number)
            else:
                ack_request += "Contact: <sip:%s@%s:%d;transport=tcp>\r\n" % (msg_info.sipid_number, msg_info.local_ip_number, msg_info.local_port_number)
        else:
            if msg_info.protocol == 'udp':
                ack_request += "Contact: <sip:%s:%d;transport=udp>\r\n" % (msg_info.local_ip_number, msg_info.local_port_number)
            else:
                ack_request += "Contact: <sip:%s:%d;transport=tcp>\r\n" % (msg_info.local_ip_number, msg_info.local_port_number)

        ack_request += "Max-Forwards: 70\r\n"
        ack_request += "User-Agent: %s\r\n" % (msg_info.user_agent)
        ack_request += "To:%s"%msg_info.to_header + "\r\n"
        ack_request += "From:%s"%msg_info.from_header + "\r\n"
        ack_request += "Call-ID: %s\r\n" % msg_info.call_id
        ack_request += "CSeq: %d ACK\r\n" %msg_info.cseq_num
        ack_request += "Content-Length: 0\r\n\r\n"
    
        debug_print( "send this message to (%s:%d)"%(msg_info.dest_ip_number, msg_info.dest_port_number), VERBOSE)    
    
        if msg_info.protocol == 'udp':
            sock.sendto(ack_request, (msg_info.dest_ip_number, msg_info.dest_port_number))
        else:
            try:
                sock.sendall(ack_request)
            except Exception as e:
                addCaseLog("send ACK failed,socket connect failed: %s(send_INFO)") % (str(e))
                self.OnError()
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1
        return True

    def send_invite(self,sock,msg_info):
        msg_info = self.checkAndInitData(sock, msg_info)
        if msg_info == False:
            self.OnError()
        if not XSERVER_INVITE.has_key(msg_info.call_id):
            XSERVER_INVITE.setdefault(msg_info.call_id)
            msg_info.hastotag = False
        elif self.compare_string(str(XSERVER_INVITE[msg_info.call_id]), 'None') != 0:
            msg_info.totag = XSERVER_INVITE[msg_info.call_id]
            msg_info.hastotag = True
        if msg_info.sdp == 'NONE':
            if msg_info.isSrtp == 0:
                sdp_content = "v=0\r\no=user1 8000 8000 IN IP4 %s\r\ns=SIP Call\r\nc=IN IP4 %s\r\nt=0 0\r\n" % (msg_info.local_ip_number, msg_info.local_ip_number)
                sdp_content += "m=audio %d RTP/AVP 0 101\r\na=sendrecv\r\na=rtpmap:0 PCMU/8000\r\na=ptime:20\r\na=rtpmap:101 telephone-event/8000\r\na=fmtp:101 0-15\r\n"%( msg_info.rtp_media_port)
            else:
                sdp_content = "v=0\r\no=user1 8000 8000 IN IP4 %s\r\ns=SIP Call\r\nc=IN IP4 %s\r\nt=0 0\r\n"%(msg_info.local_ip_number, msg_info.local_ip_number)
                sdp_content +=  "m=audio %d RTP/SAVP 0 101\r\na=sendrecv\r\na=rtpmap:0 PCMU/8000\r\na=ptime:20\r\na=rtpmap:101 telephone-event/8000\r\na=fmtp:101 0-15\r\n"%(msg_info.rtp_media_port)
                sdp_content += "a=crypto:1 AES_CM_256_HMAC_SHA1_80 inline:75f0VtA/4DiQX8hp5DSi0qkYUV99q44ua5vkdL4W1e32yRr92ZMIaKDLDqtSKg==|2^31\r\n"
                sdp_content += "a=crypto:2 AES_CM_256_HMAC_SHA1_32 inline:W/UvV5zFQg7jIRrso3CS2dj1yxJE6DvR0zLfnCDGjCcQl2PnnDljNa0YGRogTw==|2^31\r\n"
                sdp_content += "a=crypto:3 AES_CM_128_HMAC_SHA1_80 inline:cr3pJrFmUyt7LmXrD0ZhTZTgZoyLvTXPZFQQZyyc|2^31\r\n"
                sdp_content += "a=crypto:4 AES_CM_128_HMAC_SHA1_32 inline:vqRjdqxU7Lot2R3d4ub2PDXWbwf/qerNSpvInzBj|2^31\r\n"
        else:
            sdp_content = msg_info.sdp
        if msg_info.meeting_pw == "NONE" or msg_info.meeting_pw == "":
            invite_request = "INVITE sip:%s@%s:%s SIP/2.0\r\n"%(msg_info.meeting_id_to_user, msg_info.dest_ip_domain_name, msg_info.dest_port_number)
        else:
            invite_request = "INVITE sip:%s*%s@%s:%s SIP/2.0\r\n"%(msg_info.meeting_id_to_user, msg_info.meeting_pw, msg_info.dest_ip_domain_name, msg_info.dest_port_number)
        if msg_info.protocol == 'udp':
            invite_request += "Via: SIP/2.0/UDP %s:%d;branch=z9hG4bK12345678%x;rport;alias"%(msg_info.local_ip_number,msg_info.local_port_number, random.randint(0, 10000)) + "\r\n"
            invite_request += "Contact: <sip:" + msg_info.sipid_number + "@" + msg_info.local_ip_number + ":" + "%d"%msg_info.local_port_number + ";transport=udp>\r\n"
        else:
            invite_request += "Via: SIP/2.0/TCP %s:%d;branch=z9hG4bK12345678%x;rport;alias"%(msg_info.local_ip_number,msg_info.local_port_number, random.randint(0, 10000)) + "\r\n"
            invite_request += "Contact:  \"%s (%s)\" <sip:"%(str(msg_info.display_name),str(msg_info.sipid_number)) + str(msg_info.sipid_number) + "@" + str(msg_info.local_ip_number) + ":" + "%d"%msg_info.local_port_number + ";transport=tcp>\r\n"
    
        if msg_info.hastotag == True:
            if msg_info.meeting_pw == "NONE" or msg_info.meeting_pw == "":
                invite_request += "To: <sip:%s@%s:%d>;tag=%s\r\n"%(msg_info.meeting_id_to_user, msg_info.dest_ip_domain_name, msg_info.dest_port_number, msg_info.totag)
            else:
                invite_request += "To: <sip:%s*%s@%s:%d>;tag=%s\r\n"%(msg_info.meeting_id_to_user, msg_info.meeting_pw, msg_info.dest_ip_domain_name, msg_info.dest_port_number, msg_info.totag)
    
        else:
            if msg_info.meeting_pw == "NONE" or msg_info.meeting_pw == "":
                invite_request += "To: <sip:%s@%s:%s>\r\n"%(msg_info.meeting_id_to_user, msg_info.dest_ip_domain_name, msg_info.dest_port_number)
            else:
                invite_request += "To: <sip:%s*%s@%s:%s>\r\n"%(msg_info.meeting_id_to_user, msg_info.meeting_pw, msg_info.dest_ip_domain_name, msg_info.dest_port_number)
    
        invite_request += "From: \"%s (%s)\" <sip:%s@%s:%s>;tag=%s\r\n"%(msg_info.display_name,msg_info.sipid_number, msg_info.sipid_number, msg_info.dest_ip_domain_name, msg_info.dest_port_number, msg_info.fromtag)
        
        
        if msg_info.statusCode == 401:
            invite_request += "Authorization: %s\r\n"%msg_info.authorization_header;
        elif msg_info.statusCode == 407:
            invite_request += "Proxy-Authorization: %s\r\n"%msg_info.proxy_authorization_header;
        
        invite_request += "Call-ID: %s\r\n"%msg_info.call_id
        invite_request += "CSeq: %d INVITE\r\n" % msg_info.cseq_num
        invite_request += "Max-Forwards: 70\r\n"
        invite_request += "User-Agent: %s\r\n"%(msg_info.user_agent)
        invite_request += "Privacy: none\r\n"
        invite_request += "P-Preferred-Identity: \"%s\" <sip:"%(str(msg_info.display_name)) + str(msg_info.sipid_number) + "@" + str(msg_info.dest_ip_domain_name) + ">\r\n"
        invite_request += "Supported: replaces, path, timer, eventlist\r\n"
        invite_request += "Allow: INVITE, ACK, OPTIONS, CANCEL, BYE, SUBSCRIBE, NOTIFY, INFO, REFER, UPDATE, MESSAGE\r\n"
        invite_request += "Content-Type: application/sdp\r\n"
        invite_request += "Accept: application/sdp, application/dtmf-relay\r\n"
        invite_request += "Content-Length: %d\r\n\r\n"%(len(sdp_content))
        invite_request += sdp_content
        debug_print(invite_request, VERBOSE)
        if msg_info.protocol == 'udp':
            sock.sendto(invite_request, (msg_info.dest_ip_number, msg_info.dest_port_number))
        else:
            try:
                sock.sendall(invite_request)
            except Exception as e:
                addCaseLog("send request %s  failed,socket connect failed: %s(send_INVITE)" % (msg_info.call_id,str(e)))
                self.OnError()
            
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1

    def calc_auth_response(self,realm, username, password, method, ruri, nonce ):
        ha1 = md5.new()
        ha1.update(username)
        ha1.update(":")
        ha1.update(realm)
        ha1.update(":")
        ha1.update(str(password))
        ha1_string = ha1.hexdigest()
    
        print "%s,%s,%s,%s"%(username, realm, str(password), ha1_string)
    
        ha2 = md5.new()
        ha2.update(method)
        ha2.update(":")
        ha2.update(ruri)
        ha2_string = ha2.hexdigest()
    
        response = md5.new()
        response.update(ha1_string)
        response.update(":")
        response.update(nonce)
        response.update(":")
        response.update(ha2_string)
        return response.hexdigest()

    def create_authorization(self,msg_info):
        response_string = self.calc_auth_response(msg_info.realm, msg_info.sipid_number, msg_info.sipid_password, msg_info.msg_method, msg_info.ruri, msg_info.nonce )
        print "Digest username=\"%s\", realm=\"%s\", nonce=\"%s\", uri=\"%s\", response=\"%s\", algorithm=MD5"%(msg_info.sipid_number,msg_info.realm,msg_info.nonce,msg_info.ruri,response_string) 
        return "Digest username=\"%s\", realm=\"%s\", nonce=\"%s\", uri=\"%s\", response=\"%s\", algorithm=MD5"%(msg_info.sipid_number,msg_info.realm,msg_info.nonce,msg_info.ruri,response_string)

###########################
####Author:chfshan
####analysis sip message, get and set data to class create_sipObject's every varabile
####parameter:
####text: the text data of sip message
####return:
####class create by create_sipObject
########################### 
    def parse(self,text):
        """Parses the incoming SUBSCRIBE."""
        try:
            lines = text.split('\r\n')
            # Line 1 conatains the SUBSCRIBE and our MAC
            msg = create_sipObject(pkt=text)
            result = int(lines[0][0:7].find('SIP/2.0'))
            if result == -1:
                msg.msg_isReq = True
                debug_print('this is a request message(parse)', VERBOSE)
            else:
                debug_print('this is a response message(parse)', VERBOSE)
            if msg.msg_isReq == False:
                temp_buffer = lines[0].split(' ')
                msg.statusCode = int(temp_buffer[1])
                msg.statusPhase = temp_buffer[2]
            # Some SIP info we need
            lineindex = self.get_headerline_by_name(text, "Call-ID")
            if lineindex == 0:
                return None
            
            temp_buffer_list = lines[lineindex].split(':')
            msg.call_id = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
            msg.call_id = msg.call_id.strip()
            
            lineindex = self.get_headerline_by_name(text, "CSeq")
            if lineindex == 0:
                return None
            temp_buffer_list = lines[lineindex].split(':')
            cseq_temp = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
            msg.cseq = cseq_temp
            cseq_temp_2 = msg.cseq.split(' ')
            msg.cseq_num = int(cseq_temp_2[0])
            msg.msg_method = cseq_temp_2[1]
            debug_print("lineindex0: %s" % lineindex, VERBOSE)
            lineindex = self.get_headerline_by_name(text, "Via")
            if lineindex == 0:
                return None
            
            msg.via_header = lines[lineindex]
            result = int(msg.via_header.find(";branch="))
            if result != -1:
                temp_buffer_list =  msg.via_header[result + 8:].split(';')
                msg.branchStr = temp_buffer_list[0].strip()
            
#             lineindex = self.get_snd_via_header(text)
            lineindex = self.get_headerline_by_name(text,"Via",1)            
            if lineindex > 1:
                msg.snd_via_header = lines[lineindex]
            
#             lineindex = self.get_third_via_header(text)
            debug_print("lineindex1: %s" % lineindex, VERBOSE)
            lineindex = self.get_headerline_by_name(text,"Via",2)
            if lineindex > 1:
                msg.third_via_header = lines[lineindex]
            lineindex = self.get_headerline_by_name(text, "From")
            debug_print("lineindex1-1: %s" % lineindex, VERBOSE)
            if lineindex == 0:
                return None
            temp_buffer_list = lines[lineindex].split(':')
            msg.from_header = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
            result = int(msg.from_header.find(";tag="))
            debug_print("lineindex1-2-result: %s" % result, VERBOSE)
            if result != -1:
                user_buffer =  msg.from_header[result + 5:].split(';')
                msg.fromtag = user_buffer[0]
            result = msg.from_header.find("@")
            debug_print("lineindex1-3-result: %s" % msg.from_header, VERBOSE)
            if result != -1:
                user_buffer = msg.from_header.split('@')
#                 user_index = user_buffer[0].find('sip:')
                user_index = user_buffer[len(user_buffer)-2].find('sip:')
                debug_print("lineindex1-5-user_index: %s" % user_index, VERBOSE)
                if user_index == -1:
                    return None
                user_name = user_buffer[len(user_buffer)-2][user_index + 4:]
                msg.sipid_number = user_name.strip()
                debug_print("lineindex1-5-sipid_number: %s" % msg.sipid_number, VERBOSE)
            else:
                user_index = msg.from_header.find('sip:')
                debug_print("lineindex1-6-user_index: %s" % user_index, VERBOSE)
                if user_index == -1:
                    return None
                msg.sipid_number = 'none'
            lineindex = self.get_headerline_by_name(text, "To")
            if lineindex == 0:
                return None
            temp_buffer_list = lines[lineindex].split(':')
            msg.to_header = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
            debug_print("lineindex2: %s" % lineindex, VERBOSE)
            result = int(msg.to_header.find(";tag="))
            if result != -1:
                msg.hastotag = True
                user_buffer =  msg.to_header[result + 5:].split(';')
                msg.totag = user_buffer[0]
            
            result = int(msg.to_header.find("@"))
            if result != -1:
                user_buffer = msg.to_header.split('@')
                user_index = user_buffer[0].find('sip:')
                if user_index == -1:
                    return None
                user_name = user_buffer[0][user_index + 4:]
                msg.meeting_id_to_user = user_name.strip()
            else:
                user_index = msg.to_header.find('sip:')
                if user_index == -1:
                    return None
                msg.meeting_id_to_user = 'none'
                msg.to_host = 'none'
        
            lineindex = self.get_headerline_by_name(text, "Content-Type")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.contentType = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
                flag_for_contentType_checking = msg.contentType.find('message/sipfrag')
                if flag_for_contentType_checking != -1:
                    sdp_index = text.find('\r\n\r\n')
                    if sdp_index != -1:
                        msg.body = text[sdp_index+4:]
                        msg.bHasBody = True        
                flag_for_contentType_checking = msg.contentType.find('application/sdp')
                if flag_for_contentType_checking != -1:
                    sdp_index = text.find('m=audio ')
                    if sdp_index != -1:
                        user_buffer = text[sdp_index:].split(' ')
                        msg.sdp_remotePort = int(user_buffer[1])
                        msg.first_audio_codec_type = int(user_buffer[3].split('\r\n')[0])
                        sdp_index = text.find('c=IN IP4 ')
                        if sdp_index != -1:
                            user_buffer = text[sdp_index:].split(' ')
                            msg.sdp_remoteHost = user_buffer[2]
        
                        format_string = "a=rtpmap:%d"%msg.first_audio_codec_type
                        param_index = text.find(format_string)
                        if param_index != -1:
                            msg.first_audio_codec_rtpmap_param = text[param_index:].split('\r\n')[0]
        
                        format_string = "a=ptime"
                        param_index = text.find(format_string)
                        if param_index != -1:
                            msg.sdp_ptime_param_string = text[param_index:].split('\r\n')[0]
                        sdp_index = text.find('\r\n\r\n')
        
                        if sdp_index != -1:
                            msg.body = text[sdp_index+4:]
                            msg.bHasBody = True    
                            sdp_index = text.find('m=video ')
                            if sdp_index != -1:
                                user_buffer = text[sdp_index:].split(' ')
                                try:
                                    msg.first_video_codec_type = int(user_buffer[3].split('\r\n')[0])
                                    format_string = "a=rtpmap:%d"%msg.first_video_codec_type
                                    param_index = text.find(format_string)
                                    if param_index != -1:
                                        msg.first_video_codec_rtpmap_param = text[param_index:].split('\r\n')[0]
                                    format_string = "a=fmtp:%d"%msg.first_video_codec_type
                                    param_index = text.find(format_string)
                                    if param_index != -1:
                                        msg.first_video_codec_fmtp_param = text[param_index:].split('\r\n')[0]
                                except:
                                    debug_print( "video sdp parse error\r\n", VERBOSE)
        
                #the other kind of body
                if msg.bHasBody == False:
                    sdp_index = text.find('\r\n\r\n')
                    if sdp_index != -1:
                        msg.body = text[sdp_index+4:]
                        msg.bHasBody = True        
        
            lineindex = self.get_headerline_by_name(text, "Refer-To")
            debug_print("lineindex 3: %s" % lineindex, VERBOSE)
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.refer_to_header = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
            else:
                lineindex = self.get_headerline_by_name(text, "Refer-to")
                if lineindex > 0:
                    temp_buffer_list = lines[lineindex].split(':')
                    msg.refer_to_header = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
            debug_print("lineindex 4: %s" % lineindex, VERBOSE)
            lineindex = self.get_headerline_by_name(text, "Referred-By")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.referred_by_header = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
            lineindex = self.get_headerline_by_name(text, "Event")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.eventType = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
            debug_print("lineindex 5: %s" % lineindex, VERBOSE)
            lineindex = self.get_headerline_by_name(text, "Replaces")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.replaces = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
            
            lineindex = self.get_headerline_by_name(text, "Subscription-State")
            debug_print("lineindex 6: %s" % lineindex, VERBOSE)
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.subscriptionState = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
        
            lineindex = self.get_headerline_by_name(text, "Expires")
            if lineindex > 0:
                msg.expires_header = lines[lineindex]
                temp_buffer_list = lines[lineindex].split(':')
                tmp_expires_buffer = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
                msg.expires_value = int(tmp_expires_buffer.strip())
            else:
                expires_index = text.find(';expires=0')
                if expires_index != -1:
                    msg.expires_value = 0
        
            lineindex = self.get_headerline_by_name(text, "Session-Expires")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.sessionExpires = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
                if len(msg.sessionExpires) > 2:
                    result_sessionTimer = int(msg.sessionExpires.find(";", 0, 5))
                    if result_sessionTimer != -1:
                        if result_sessionTimer > 0:
                            msg.sessExpires_time_value = int(msg.sessionExpires[0 : result_sessionTimer-1])
                            result_sessionTimer_ = int(msg.sessionExpires.find("uac", result_sessionTimer, 20))
                            if result_sessionTimer_ != -1:
                                msg.sessExpires_refresh_value = 1
                            else:
                                msg.sessExpires_refresh_value = 2
                    else:
                        msg.sessExpires_time_value = int(msg.sessionExpires)
                        msg.sessExpires_refresh_value = 0
                
            lineindex = self.get_headerline_by_name(text, "Min-SE")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.minSE = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
                msg.minSE_time_value = int(msg.minSE)
        
            lineindex = self.get_headerline_by_name(text, "Supported")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.supported = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
        
            lineindex = self.get_headerline_by_name(text, "Require")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.requires = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
            debug_print("lineindex 7: %s" % lineindex, VERBOSE)
            lineindex = self.get_headerline_by_name(text, "RSeq")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.rSeq = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
        
            lineindex = self.get_headerline_by_name(text, "RAck")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.rAck = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
        
            lineindex = self.get_headerline_by_name(text, "Call-Info")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.call_info_header = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
        
            lineindex = self.get_headerline_by_name(text, "Alert-Info")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.alert_info_header = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
        
            lineindex = self.get_headerline_by_name(text, "Authorization")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.authorization_header = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
            debug_print("lineindex 8: %s" % lineindex, VERBOSE)
            lineindex = self.get_headerline_by_name(text, "WWW-Authenticate")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.www_authenticate_header = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
                result = int(msg.www_authenticate_header.find('realm=\"'));
                if result != -1:
                    realm_string_1 = msg.www_authenticate_header[result+7:].split('"')
                    msg.realm = realm_string_1[0]
                    debug_print( "===================%s"%(msg.realm),VERBOSE)
                    result = int(msg.www_authenticate_header.find('nonce=\"'));
                    if result != -1:
                        nonce_string_1 = msg.www_authenticate_header[result+7:].split('"')
                        msg.nonce = nonce_string_1[0]
        
            lineindex = self.get_headerline_by_name(text, "Proxy-Authenticate")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.proxy_authenticate_header = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
                result = int(msg.proxy_authenticate_header.find('realm=\"'));
                if result != -1:
                    realm_string_1 = msg.proxy_authenticate_header[result+7:].split('"')
                    msg.realm = realm_string_1[0]
                    result = int(msg.proxy_authenticate_header.find('nonce=\"'));
                    if result != -1:
                        nonce_string_1 = msg.proxy_authenticate_header[result+7:].split('"')
                        msg.nonce = nonce_string_1[0]
            
            lineindex = self.get_headerline_by_name(text, "User-Agent")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.user_agent = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
                
            lineindex = self.get_headerline_by_name(text, "P-Preferred-Identity")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.ppi_header = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
            
                result = msg.from_header.find("@")
                if result != -1:
                    user_buffer = msg.ppi_header.split('@')
                    user_index = user_buffer[0].find('sip:')
                    if user_index != -1:
                        user_name = user_buffer[0][user_index + 4:]
                        msg.ppi_user = user_name.strip()
        
            lineindex = self.get_headerline_by_name(text, "Privacy")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                user_index = temp_buffer_list[1].find('id')
                if user_index != -1:
                    msg.bPrivacyRequired = True
        
            lineindex = self.get_headerline_by_name(text, "Contact")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.contact_header = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
            debug_print("lineindex 8: %s" % lineindex, VERBOSE)
            lineindex = self.get_headerline_by_name(text, "Diversion")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.diversion_header = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
        
            lineindex = self.get_headerline_by_name(text, "Allow")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.allow_header = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
            
            """Add for gsmeeting projectX by amanda"""
            lineindex = self.get_headerline_by_name(text, "X-GS-SERVER-ID")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.x_gs_server_id = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
                
            lineindex = self.get_headerline_by_name(text, "X-GS-Notify-Users")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.x_gs_notify_users = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
            debug_print("lineindex 9: %s" % lineindex, VERBOSE)
            lineindex = self.get_headerline_by_name(text, "X-GS-Conf-Control")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.x_gs_conf_control = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
            return msg
        except:
            debug_print( "this may be empty packet\r\n", VERBOSE)
            return None

    def OnError(self):
        addCaseLog("sipServer_commonlib.OnError, case failed")
        setCaseResult("failed")
        if self.localsock:
            self.localsock.close()
        sys.exit()
    def get_compact_format_by_name(self,name):
        for key in self.header_name_compact_format_dictionary.keys():
            if self.compare_string(key, name) == 0:
                return self.header_name_compact_format_dictionary[key]
        return '0'

###########################
####Author:chfshan
####check is sip message is health ,if not false, else return class create_sipObject
####parameter:
####msg_info: class create by create_sipObject
####return
####class create by create_sipObject
###########################
    def checkAndInitData(self,sock,msg_info):
        try:
            if msg_info.dest_ip_domain_name == '' or msg_info.dest_ip_domain_name == 'NONE':
                msg_info.dest_ip_domain_name = msg_info.dest_ip_number
            if msg_info.rtp_media_port == "":
                msg_info.rtp_media_port = self.rtp_port
            if msg_info.user_agent == "":
                msg_info.user_agent = self.user_agent
            if msg_info.display_name == "":
                msg_info.display_name = self.display_name
            if msg_info.meeting_id_to_user== "" or msg_info.dest_ip_number=="" or msg_info.dest_port_number == "":
                addCaseLog("to user is empty or dest ip|port is empty (checkInitData)")
                return False
            if msg_info.sipid_number == "" or msg_info.local_ip_number == "" or msg_info.local_port_number == "":
                addCaseLog("from user is empty or local ip|port is empty (checkInitData)")
                return False
            if sock =="":
                addCaseLog("Sock may create failed (checkInitData)")
                return False
            if msg_info.cseq_num == "":
                msg_info.cseq_num = XSERVER_PUBLICKEY["cseq_num_all"]
        except Exception as e:
            
            addCaseLog("check data failed:")
            addCaseLog(e)
            self.OnError()
        return msg_info

    def get_headerline_by_name(self, buffer, name, pos = 0):
        """find the header line by name"""
        if len(name) == 0:
            return 0
        lines = buffer.split('\r\n')
        lineindex = 1
        tmp_pos_value = 0
        
        while True:
            if len(lines[lineindex]) > 3:
                result = lines[lineindex].find(':')
                
                if result != -1:
                    
                    result = int(lines[lineindex].find(name, 0, 20))
                    if result != -1:
                        temp_buffer1 = lines[lineindex].split(':')
                        temp_buffer2 = temp_buffer1[0].strip()
                        if len(name) == len(temp_buffer2):
                            
                            if tmp_pos_value == pos:
                                return lineindex
                            tmp_pos_value += 1
                    
                    else:
                        temp_buffer1_a = lines[lineindex].split(':')
                        if len(temp_buffer1_a[0]) == 1:
                            temp_buffer2_a = self.get_compact_format_by_name(name)
                            if temp_buffer2_a[0] != '0':
                                if temp_buffer1_a[0][0] == temp_buffer2_a[0]:
                                    if tmp_pos_value == pos:
                                        return lineindex
                                    tmp_pos_value += 1
                lineindex += 1
            else:
                break    
        
        return 0

###########################
####Author:chfshan
####create socket and start received thread
####parameter:
####
####return
####
###########################
    def initClient(self):
        self.localsock = connectServer(self.dest_address, self.dest_port, self.localip, self.localport,self.protocol)
        msg_info = self.checkAndInitData(self.localsock, self.object)
        if msg_info == False :
            self.OnError()
        receivePack = sipReceiveSock_Thread(self.localsock,msg_info)
        receivePack.start()

    def set(self,msg_info,section,data):
        global SESSIONINFO
        for i in range(0,len(SESSIONINFO)):
            if SESSIONINFO[i]['fromuser'] == msg_info.sipid_number:
                if SESSIONINFO[i].has_key(section):
                    SESSIONINFO[i][section] = data
                else:
                    return False
    def get(self,msg_info,section):
        global SESSIONINFO
        for i in range(0,len(SESSIONINFO)):
            if SESSIONINFO[i]['fromuser'] == msg_info.sipid_number:
                if SESSIONINFO[i].has_key(section):
                    return SESSIONINFO[i][section]
                else:
                    return False
###########################
####Author:chfshan
####create call thread and recevie thread and RTP send and received thread
####parameter:
####sip_obj: create by create_sipObject
####return
####
###########################
class x_Join_Meeting(sipServer_commonlib):
    def __init__( self, sip_obj):
        sipServer_commonlib.__init__(self,sip_obj)
        self.OnSetUp()
        self.start_Xserver(self.localport,self.rtp_port)
#         self.receivedThread = ""
        self.inviteThread = ""
    def OnSetUp(self):
        global MEETINNG_ROOM_ID,MEETING_PASSWORD
        if self.fromuser == "" or str(self.fromuser).lower() == "none":
            addCaseLog("your sipID is empty, starting to connect Web server and get sipID with web user %s:%s (sipServer_commonlib)" %(self.webserver_account,self.webserver_account_pw))
            webuser = webAPI(self.webserver, self.webserver_port, self.localip, self.localport, self.webserver_account,self.webserver_account_pw)
            webuser.getVOIPnumberandPW()
            self.object.fromuser = self.fromuser = webuser.sipUserID
            self.object.sipid_password = self.sipid_password = webuser.sipUserPassword
            addCaseLog("get sipID account  %s:%s" %(self.fromuser,self.sipid_password))
        if self.touserOrmeetingID == "" or str(self.touserOrmeetingID).lower() == "none":
            addCaseLog("your meetingID is empty, starting to connect Web server and get sipID with web user %s:%s" %(self.webserver_account,self.webserver_account_pw))
            webuser = webAPI(self.webserver, self.webserver_port, self.localip, self.localport, self.webserver_account,self.webserver_account_pw)
            webuser.getQuickStartMeetingID()
            self.object.touserOrmeetingID = self.touserOrmeetingID = webuser.meetingID
            self.object.meeting_pw = self.meeting_pw =  webuser.meetingPassword
            addCaseLog("get meeting number  %s:%s" %(self.touserOrmeetingID,self.meeting_pw))
        
        if self.sipid_password == "" or str(self.sipid_password).lower() == 'none':
            self.object.sipid_password = self.sipid_password = self.fromuser
        self.localsock = connectServer(self.dest_address, self.dest_port, self.localip, self.localport,self.protocol)

    def start_Invite_Register_session_timer(self,localport="",local_rtp_port=""):
        self.localport = localport
        self.rtp_port = local_rtp_port
        msg_info = self.checkAndInitData(self.localsock, self.object)
        if msg_info == False :
            self.OnError()
        
        thread_for_Invite_register_session_timer = Invite_Register_session_timer(self.localsock,msg_info)
        thread_for_Invite_register_session_timer.start()
        self.inviteThread = thread_for_Invite_register_session_timer
        
    def start_rtp_session_timer(self,local_rtp_port):
        if local_rtp_port == "":
            local_rtp_port = self.local_rtp_port
        media = ipvideotalk_Media_Data(self.localip,int(local_rtp_port))
#         media = Media_Service(self.localip,int(local_rtp_port))
        media.start()
        
    def start_sipReceiveSock_Thread(self,localport="",local_rtp_port=""):
        self.localport = localport
        self.rtp_port = local_rtp_port

        msg_info = self.checkAndInitData(self.localsock, self.object)
        if msg_info == False :
            self.OnError()

        receivePack = sipReceiveSock_Thread(self.localsock,msg_info)
        receivePack.start()
        self.receivedThread = receivePack
#         time.sleep(2)
        return receivePack

    def start_Xserver(self,localport="",local_rtp_port=""):
 
        self.start_sipReceiveSock_Thread(localport,local_rtp_port)
        self.start_Invite_Register_session_timer(localport,local_rtp_port)
        self.start_rtp_session_timer(local_rtp_port)

class Invite_Register_session_timer(sipServer_commonlib):
    def __init__( self, sock, sip_obj):
        sipServer_commonlib.__init__(self,sip_obj)
        self.localsock = sock
        self.register_time = 60
        self.invite_session_time = 1200
    def run(self):
        global service_on
        global SESSIONINFO
        sendsock = self.localsock;
        invite_count = 0
        invite_call_id_str = 'NONE'
        register_call_id_str = "NONE"
        from_tag_str = 'NONE'
        register_count = 0
        addCaseLog("#######Invite_Register_session_timer for %s 's thread is started on [%s:%d]"%(self.fromuser,self.localip, self.localport))
        addCaseLog("uid= %s, confid = %s, confpw= %s"%(self.fromuser,self.touserOrmeetingID,self.meeting_pw))
        while service_on:
            if register_count%(self.register_time) == 0:
                register_msg = copy.deepcopy(self.object)
                register_msg.meeting_id_to_user = self.fromuser
                register_msg.fromtag= "%x"%random.randint(0, 10000)
                if self.compare_string(register_call_id_str, 'NONE') == 0:
                    register_call_id_str = "1701338429%x@%s-%d"%(random.randint(0, 10000),self.localip,self.localport)                
                register_msg.call_id = register_call_id_str
                register_msg.cseq_num = XSERVER_PUBLICKEY["cseq_num_all"]
                addCaseLog("%s try to send %s register request to %s (Invite_Register_session_timer)"%(register_msg.sipid_number,register_count/self.register_time, register_msg.meeting_id_to_user))
                self.send_base_request(sendsock, "REGISTER",register_msg)
                addCaseLog("%s send %s register request to %s (Invite_Register_session_timer)"%(register_msg.sipid_number,register_count/self.register_time,  register_msg.meeting_id_to_user))
            register_count = register_count + 1
            time.sleep(1)
            if invite_count%(self.invite_session_time) == 0:
                invite_msg = copy.deepcopy(self.object)

                if self.compare_string(invite_call_id_str, 'NONE') == 0:
                    invite_call_id_str = "1701338429%x@%s-%d-%s"%(random.randint(0, 10000),self.localip,self.localport,self.fromuser)
                if self.compare_string(from_tag_str, 'NONE') == 0:
                    from_tag_str = "%x"%random.randint(0, 10000)
                    SESSIONINFO.append({'fromuser':self.fromuser,'call_id':invite_call_id_str,'fromtag':from_tag_str,'totag':'None','sdp':invite_msg.sdp})
                invite_msg.fromtag=from_tag_str
                invite_msg.call_id=invite_call_id_str
                for i in range(0,len(SESSIONINFO)):
                    if SESSIONINFO[i]['call_id'] == invite_msg.call_id:
                        if self.compare_string(str(SESSIONINFO[i]['totag']), 'None') != 0:
                            invite_msg.totag = SESSIONINFO[i]['totag']
                            invite_msg.hastotag = True
                invite_msg.cseq_num = XSERVER_PUBLICKEY["cseq_num_all"]
                          
                self.send_invite(sendsock,invite_msg)
                addCaseLog("%s send %s INVITE request to %s (Invite_Register_session_timer)"%(invite_msg.sipid_number,invite_count/self.invite_session_time, self.touserOrmeetingID))
            invite_count = invite_count + 1
            time.sleep(1)
        addCaseLog("#######Invite_Register_session_timer for %s 's thread is stopped on [%s:%d],result is service_on = %s (Invite_Register_session_timer)"%(self.fromuser,self.localip, self.localport,service_on))
    def OnError(self):
        addCaseLog("sipServer_commonlib.OnError, case failed")
        setCaseResult("failed")
        if self.localsock:
            self.localsock.close()
        sys.exit()

class sipReceiveSock_Thread(sipServer_commonlib):
    def __init__( self, sock, sip_obj):
        sipServer_commonlib.__init__(self,sip_obj)
        self.callID = ""
        self.test_notify_index = 0
        self.message_index = 0
        self.bye_index = 0
        self.invite_200OK_index = 0
        self.invite_index = 0
        self.is_join_meeting_success = 0
        self.temp_sipmessage = sip_obj
        self.localsock = sock
    def run(self):
        global service_on,is_Exception_test
        global cseq_num_all
        sendsock = self.localsock
        is_first_notify = 1
        addCaseLog("#######  %s 's thread sipReceiveSock_Thread is started on [%s:%d]########"%(self.fromuser,self.localip, self.localport))
        addCaseLog("uid= %s, uidpw = %s, confid = %s(sipReceiveSock_Thread)"%(self.fromuser,self.touserOrmeetingID,self.meeting_pw))
        while service_on:
            try:
                if self.protocol == 'udp':
                    response, rcvaddress= sendsock.recvfrom(10240)
                else:
                    response = sendsock.recv(10240)
#                     print response
            except Exception as e:
#                 addCaseLog("dealWithRecePack::received Packet = %s"%e)
                continue
            service_msg = self.parse(response)
            if service_msg == None:
                continue
            service_msg.local_ip_number = self.localip
            service_msg.local_port_number = self.localport
            service_msg.dest_ip_domain_name = self.dest_ip_domain_name
            service_msg.user_agent = self.user_agent
            service_msg.protocol = self.protocol
            service_msg.isSrtp = self.isSrtp
            if service_msg.protocol == 'udp':
                rcv_host, rcv_port = rcvaddress
                service_msg.dest_ip_number = rcv_host
                service_msg.dest_port_number = rcv_port
            else:
                service_msg.dest_ip_number = self.dest_address
                service_msg.dest_port_number = self.dest_port
            if service_msg:
                self.callID = service_msg.call_id
                if service_msg.msg_isReq:
                    addCaseLog("%s request::%s %d %s request is received for %s, to_user = %s (sipReceiveSock_Thread)" % (service_msg.sipid_number,service_msg.msg_method, service_msg.statusCode, service_msg.statusPhase, service_msg.sipid_number, service_msg.meeting_id_to_user))
                    if self.compare_string(service_msg.msg_method, 'NOTIFY') == 0:
                        self.test_notify_index = self.test_notify_index+1
                        if service_msg.bHasBody:
                            addCaseLog("%s has body (sipReceiveSock_Thread)" % (service_msg.msg_method))
                        if is_first_notify == 1:
                            is_first_notify = 0
                            service_msg.meeting_id_to_user=self.touserOrmeetingID
                            service_msg.sipid_number=self.fromuser
                            self.is_join_meeting_success = 0
                            service_msg.cseq_num = service_msg.cseq_num + 1
                            param = "uid=%s;action=get_all_users;conf-id=%s"%(service_msg.sipid_number, self.touserOrmeetingID)
                            service_msg.x_gs_conf_control = param
                            addCaseLog("%s : I am first Notify, start to send join meeting 'INFO', param = %s (sipReceiveSock_Thread)" % (service_msg.sipid_number,param))
                            self.send_base_request(sendsock, "INFO", service_msg)
                    if self.compare_string(service_msg.msg_method, 'BYE') == 0:
                        self.bye_index = self.bye_index + 1
                        XSERVER_RESPOND["cseq_num"] = service_msg.cseq_num

                    elif self.compare_string(service_msg.msg_method, 'MESSAGE') == 0:
                        self.test_message_index = self.test_message_index + 1
                        XSERVER_RESPOND["cseq_num"] = service_msg.cseq_num
                        addCaseLog("%s Received MESSAGE request(%s %d %s), send 200 OK to the girl (sipReceiveSock_Thread)" % (service_msg.sipid_number,service_msg.msg_method, service_msg.statusCode, service_msg.statusPhase))
                        self.handle_Unknown_request(sendsock, None, service_msg)
                        
                    elif self.compare_string(service_msg.msg_method, 'INVITE') == 0:
                        self.invite_index = self.invite_index + 1
                        service_msg.rtp_media_port = self.rtp_port
                        addCaseLog("%s Received INVITE request(%s %d %s), send 200 OK to the girl (sipReceiveSock_Thread)" % (service_msg.sipid_number,service_msg.msg_method, service_msg.statusCode, service_msg.statusPhase))
                        self.send_INVITE_response_confroom(sendsock, service_msg)
                        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1
                        
                    elif self.compare_string(service_msg.msg_method, 'ACK') != 0 and self.compare_string(service_msg.msg_method, 'INVITE') != 0 and self.compare_string(service_msg.msg_method, 'BYE') != 0 :
                        addCaseLog("%s Received unexcepted packet(%s %d %s), send 200 OK to the girl (sipReceiveSock_Thread)" % (service_msg.sipid_number,service_msg.msg_method, service_msg.statusCode, service_msg.statusPhase))
                        self.handle_Unknown_request(sendsock, None, service_msg)
                else:
                    addCaseLog("%s respond::%s %d %s repond is received for %s, to_user = %s (sipReceiveSock_Thread)" % (service_msg.sipid_number,service_msg.msg_method, service_msg.statusCode, service_msg.statusPhase, service_msg.sipid_number, service_msg.meeting_id_to_user))
                    debug_print(response, VERBOSE)
                    if service_msg.statusCode == 401:
                        if self.compare_string(service_msg.www_authenticate_header, 'NONE') != 0:
                            if self.compare_string(service_msg.msg_method, 'INVITE') != 0:
                                service_msg.cseq_num += 1
#                                 service_msg.username = service_msg.sipid_number
                                service_msg.sipid_password = self.sipid_password
                                service_msg.ruri = "sip:%s@%s:%d"%(service_msg.meeting_id_to_user, service_msg.dest_ip_domain_name, int(service_msg.dest_port_number))
                                service_msg.authorization_header = self.create_authorization(service_msg)
                                addCaseLog("%s Received 401 auth respond packet(%s %d %s), send authed  request to the girl (sipReceiveSock_Thread)" % (service_msg.sipid_number,service_msg.msg_method, service_msg.statusCode, service_msg.statusPhase))
                                self.send_base_request(sendsock, service_msg.msg_method, service_msg, None)
                    elif service_msg.statusCode == 407:
                        if self.compare_string(service_msg.proxy_authenticate_header, 'NONE') != 0:
                            if self.compare_string(service_msg.msg_method, 'INVITE') != 0:
                                service_msg.cseq_num += 1
#                                 service_msg.username = service_msg.sipid_number
                                service_msg.sipid_password = self.sipid_password
                                service_msg.ruri = "sip:%s@%s:%d"%(service_msg.meeting_id_to_user, service_msg.dest_ip_domain_name, service_msg.dest_port_number)
                                service_msg.proxy_authorization_header = self.create_authorization(service_msg)
                                addCaseLog("%s Received 407 auth respond packet(%s %d %s), send authed  request to the girl (sipReceiveSock_Thread)" % (service_msg.sipid_number,service_msg.msg_method, service_msg.statusCode, service_msg.statusPhase))
                                self.send_base_request(sendsock, service_msg.msg_method, service_msg, None)
                    
                    if self.compare_string(service_msg.msg_method, 'INVITE') == 0:
                        if service_msg.statusCode >= 200:
                            service_msg.user_agent = self.user_agent
                            service_msg.display_name = self.display_name
                            if service_msg.statusCode == 200:
                                addCaseLog("%s Received INVITE 200 repond now(%s %d %s), send ACK to the girl (sipReceiveSock_Thread)" % (service_msg.sipid_number,service_msg.msg_method, service_msg.statusCode, service_msg.statusPhase))
                                self.send_ACK_request(sendsock, service_msg)
                                XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1
                                if str(self.fromuser).lower() ==  service_msg.sipid_number:
                                    for i in range(0,len(SESSIONINFO)):
                                        if SESSIONINFO[i]['call_id'] == service_msg.call_id:
                                            if self.compare_string(str(SESSIONINFO[i]['totag']), 'None') == 0:
                                                SESSIONINFO[i]['totag'] = service_msg.totag
                                self.getSDPipAndPortInfo(response)
                                self.invite_200OK_index += 1
#                                 to_user = service_msg.meeting_id_to_user
#                                 from_user = service_msg.sipid_number
#                                 from_host = service_msg.local_ip_number
#                                 from_port = service_msg.dest_port_number
                                addCaseLog("%s Now ,start waiting Join notify....." % service_msg.sipid_number)
                                self.is_join_meeting_success = 0
                                continue
                            
                            elif service_msg.statusCode == 401:
                                service_msg.cseq_num += 1
#                                 service_msg.username = service_msg.sipid_number
                                service_msg.sipid_password = self.sipid_password
                                service_msg.ruri = "sip:%s@%s:%d"%(service_msg.meeting_id_to_user, service_msg.dest_ip_domain_name, service_msg.dest_port_number)
                                service_msg.authorization_header = self.create_authorization(service_msg)
                                service_msg.user_agent = self.user_agent
                                service_msg.display_name = self.display_name
                                service_msg.sdp = self.sdp
                                if str(self.fromuser).lower() ==  service_msg.sipid_number:
                                    for i in range(0,len(SESSIONINFO)):
                                        if SESSIONINFO[i]['call_id'] == service_msg.call_id:
                                            if self.compare_string(str(SESSIONINFO[i]['totag']), 'None') == 0:
                                                service_msg.totag='NONE'
                                                service_msg.hastotag = False
                                            service_msg.sdp = SESSIONINFO[i]['sdp']
                                addCaseLog("%s Received INVITE 4XX repond now(%s %d %s), send authed INVITE to the girl (sipReceiveSock_Thread)" % (service_msg.sipid_number,service_msg.msg_method, service_msg.statusCode, service_msg.statusPhase))
                                self.send_invite(sendsock, service_msg)
                                continue

                            elif service_msg.statusCode == 407:
                                service_msg.cseq_num += 1
#                                 service_msg.username = service_msg.sipid_number
                                service_msg.sipid_password = self.sipid_password
                                service_msg.ruri = "sip:%s@%s:%d"%(service_msg.meeting_id_to_user, service_msg.dest_ip_domain_name, service_msg.dest_port_number)
                                service_msg.proxy_authorization_header = self.create_authorization(service_msg)
                                service_msg.user_agent = self.user_agent
                                service_msg.display_name = self.display_name
                                if str(self.fromuser).lower() ==  service_msg.sipid_number:
                                    for i in range(0,len(SESSIONINFO)):
                                        if SESSIONINFO[i]['call_id'] == service_msg.call_id:
                                            if self.compare_string(str(SESSIONINFO[i]['totag']), 'None') == 0:
                                                service_msg.totag='NONE'
                                                service_msg.hastotag = False
                                            service_msg.sdp = SESSIONINFO[i]['sdp']
                                
                                addCaseLog("%s Received INVITE 4XX repond now(%s %d %s), send authed INVITE to the girl (sipReceiveSock_Thread)" % (service_msg.sipid_number,service_msg.msg_method, service_msg.statusCode, service_msg.statusPhase))
                                self.send_invite(sendsock, service_msg)
                                continue

                            else:
                                if not is_Exception_test:
                                    service_on = 0
                                    break
                                self.is_join_meeting_success = 2
                                continue
                    if self.compare_string(service_msg.msg_method, 'REGISTER') == 0:
                        XSERVER_RESPOND["call_id"] = service_msg.call_id
                        XSERVER_RESPOND["cseq_num"] = service_msg.cseq_num
                        XSERVER_RESPOND["body"] = service_msg.body
                        XSERVER_RESPOND["x_gs_conf_control"] = service_msg.x_gs_conf_control
                        if service_msg.statusCode == 200:
                            addCaseLog("%s register success,cheers!! continue" %(service_msg.sipid_number))
                            continue
#                             break
                        else:
                            if service_msg.statusCode >= 300 and service_msg.statusCode !=200 and service_msg.statusCode != 401 and service_msg.statusCode != 407:
                                addCaseLog(" %s register failed" %(service_msg.sipid_number))
#                             if not is_Exception_test:
#                                 service_on = 0
#                                 break
                            continue

                    if self.compare_string(service_msg.msg_method, 'MESSAGE') == 0:
                        XSERVER_RESPOND["call_id"] = service_msg.call_id
                        XSERVER_RESPOND["cseq_num"] = service_msg.cseq_num
                        XSERVER_RESPOND["body"] = service_msg.body
                        XSERVER_RESPOND["x_gs_conf_control"] = service_msg.x_gs_conf_control
                        if service_msg.statusCode >= 200:
                            if service_msg.statusCode == 200:
                                addCaseLog("%s send Message success,cheers!! continue"%(service_msg.sipid_number))
                                continue
                            elif service_msg.statusCode >= 300:
                                if not is_Exception_test:
                                    service_on = 0
                                    break
                                continue
                    if self.compare_string(service_msg.msg_method, 'INFO') == 0:
                        XSERVER_RESPOND["call_id"] = service_msg.call_id
                        XSERVER_RESPOND["cseq_num"] = service_msg.cseq_num
                        XSERVER_RESPOND["body"] = service_msg.body
                        XSERVER_RESPOND["x_gs_conf_control"] = service_msg.x_gs_conf_control
                        if service_msg.statusCode >= 200:
                            if service_msg.statusCode == 200:
                                addCaseLog("%s send INFO success,cheers!! continue"%(service_msg.sipid_number))
                                continue
                            elif service_msg.statusCode >= 300:
                                addCaseLog(" %s respond::%s %d %s response is received for %s(%s)" % (service_msg.sipid_number,service_msg.msg_method, service_msg.statusCode, service_msg.statusPhase, self.fromuser, self.touserOrmeetingID))
#                                 if not is_Exception_test:
#                                     service_on = 0
#                                     break
                                continue             
        addCaseLog("#######sipReceiveSock_Thread for %s is closed, result is service_on = %s (sipReceiveSock_Thread)#####"% (self.fromuser,service_on))

    def getSDPipAndPortInfo(self,data,callid=''):
        global INVITE_SDP
        global SESSIONINFO
        a = str(data).find("c=IN IP4")
        for i in range(a+8,a+8+30):
            if str(data[i]).isdigit() == False and str(data[i]) != " " and str(data[i]) != ".":
                INVITE_SDP["ip"] = str(data[a+9:i]).strip()
                break
        b = str(data).find("m=audio")
        for i in range(b+8,b+9+20):
            if str(data[i]).isdigit() == False and str(data[i]) != " " and str(data[i]) != ".":
                INVITE_SDP["port1"] = str(data[b+8:i]).strip()
                break
        c = str(data).find("m=video")
        for i in range(c+8,c+9+20):
            if str(data[i]).isdigit() == False and str(data[i]) != " " and str(data[i]) != ".":
                INVITE_SDP["port2"] = str(data[c+8:i]).strip()
                break

class webAPI(projectx_base):
    def __init__(self,destaddress = '',destport='',localaddress ="",localport = '',loginEmail="",loginpassword=""):
        global WEB_SERVER_IP,WEB_SERVER_PORT,LOCAL_PC_IP,LOCAL_PC_PORT
        if loginEmail =="":
            self.loginEmail = LOGIN_WEB_ACCOUNT
        else:
            self.loginEmail = loginEmail
        if loginpassword =="":
            self.loginpassword = LOGIN_WEB_ACCOUNT_PASSWORD
        else:
            self.loginpassword = loginpassword
        if destaddress == "":
            destaddress = WEB_SERVER_IP
        else:
            self.destaddress = destaddress
        if destport == "":
            destport = WEB_SERVER_PORT
        else:
            self.destport = destport
        if localaddress == "":
            self.localaddress = LOCAL_PC_IP
        else:
            self.localaddress = localaddress
        if localport == "":
            self.localport = LOCAL_PC_PORT
        else:
            self.localport = localport
        self.accessToken = ""
        self.meetingID = ""
        self.meetingPassword = ""
        self.meetingserialNum = ""
        self.sock = ""
        self.sipUserPassword = ""
        self.sipUserID = ""
        self.sipDomain = ""
        self.webUserID = ""
        self.web_api_host = "api.ipvideotalk.com"
        self.localsock = ""
    def OnTearDown(self):
        pass
    def OnError(self):
        addCaseLog("webAPI::OnError, case failed")
        setCaseResult("failed")
        if self.localsock:
            self.localsock.close()
        exitScript()
    def getPostData(self,postURL = "",postContent = ""):
        head = self.getWebAPISignatureHead(postContent)
        contenttext = str(head)
        contentlength = len(contenttext)
        loginAPI = "POST %s HTTP/1.1\r\n" %(postURL)
        loginAPI += "Host: %s\r\n"%(self.web_api_host)
        loginAPI += "Accept: */*\r\nContent-Length: %s\r\n"%(contentlength)
        loginAPI += "Content-Type: application/x-www-form-urlencoded\r\n\r\n" 
        loginAPI += contenttext
        return loginAPI
    def getJasonBody(self,data):
        lines = str(data).split("\r\n")
        lineLen = len(lines)
        return str(lines[lineLen-1])
#     def getAccessToken(self,destaddress,destport,loginEmail="",loginpassword=""):
    def getAccessToken(self):            
        localsock = connectServer(self.destaddress,self.destport,self.localaddress,self.localport)
        if not self.loginpassword:
            addCaseLog("getAccessToken::login Web password is null")
            self.OnError()
        if not self.loginEmail:
            addCaseLog("getAccessToken::login Web Email is null")
            self.OnError()
        loginpasswordEncode = self.getLoginPasswordEncode(self.loginpassword)
        login = self.getPostData("/user/login","username=%s&password=%s"%(self.loginEmail,loginpasswordEncode))
        localsock.send(login)
        while 1:
            try:
                response, rcvaddress= localsock.recvfrom(10240)
            except Exception as e:
                print e
                continue
            if response:
                jsondata = self.getJasonBody(response)
                if not jsondata:
                    addCaseLog("getAccessToken failed, jason body is null body= %s,total repond=%s"%(jsondata,response))
                    continue
#                     self.OnError()                    
                if jsondata.find("errorMsg") != -1:
                    addCaseLog("getAccessToken failed, errormsg=%s"%(jsondata))
                    self.OnError()
                try:
                    t = json.loads(jsondata)
                    self.accessToken = t.get('data').get('accessToken')
                except Exception as e:
                    addCaseLog("getAccessToken failed, errormsg=%s"%(e))
                    self.OnError()                    
                addCaseLog( "get accessToken success , value=%s"%(self.accessToken))
                if self.accessToken:
                    break
        localsock.close()
#     def getQuickStartMeetingID(self,destaddress = '172.172.172.24',destport='80',loginEmail="",loginpassword=""):
    def getQuickStartMeetingID(self):
        global MEETINNG_ROOM_ID,MEETING_PASSWORD,service_on
        localsock = connectServer(self.destaddress,self.destport,self.localaddress,int(self.localport) + 1)
        if not self.accessToken:
            addCaseLog("starting login webPage(%s:%s), loginEmail= %s , loginPassword = %s" %(self.destaddress,self.destport,self.loginEmail,self.loginpassword))
            self.getAccessToken()
        quickstartAPI = self.getPostData("/meeting/quick_start","accessToken=%s"%(self.accessToken))
        try:
            localsock.send(quickstartAPI)
        except Exception as e:
            addCaseLog("getQuickStartMeetingID: connect socket failed = %s" % (str(e)))
        while service_on:
            try:
                response, rcvaddress= localsock.recvfrom(10240)
            except Exception as e:
                continue
            if response == "" :
                self.OnError()
            else:
                jsondata = self.getJasonBody(response)
                if not jsondata:
                    addCaseLog("getQuickStartMeetingID failed, jason body is null = %s"%(jsondata))
                    addCaseLog("getQuickStartMeetingID failed, the response = %s"%(response))
                    continue
                if jsondata.find("errorMsg") != -1:
                    addCaseLog("getQuickStartMeetingID failed, errormsg=%s"%(jsondata))
                    self.OnError()
                try:
                    t = json.loads(jsondata)
                    self.meetingID = t.get('data').get('meetingNum')
                    self.meetingPassword = t.get('data').get('password')
                    self.meetingserialNum = t.get('data').get('serialNum')
                except Exception as e:
                    addCaseLog("getQuickStartMeetingID failed, errormsg=%s"%(e))
                    self.OnError()                     
                debug_print("confid=%s"%(self.meetingID),VERBOSE)
                MEETINNG_ROOM_ID = self.meetingID
                MEETING_PASSWORD = self.meetingPassword
                addCaseLog("Create meeting success,MEETINNG_ROOM_ID=%s,meeting password = %s"%(MEETINNG_ROOM_ID,MEETING_PASSWORD))
                if self.meetingID:
                    break
        localsock.close()
#     def getVOIPnumberandPW(self,destaddress = '172.172.172.24',destport='80',loginEmail="",loginpassword=""):
    def getVOIPnumberandPW(self):
        global SIP_ID_NUMBER,SIP_ID_PASSWORD
        localsock = connectServer(self.destaddress,self.destport,self.localaddress,int(self.localport))
        if not self.accessToken:
            self.getAccessToken()
        voipAPI = self.getPostData("/user/voip","accessToken=%s"%(self.accessToken))
        localsock.send(voipAPI)
        while 1:
            try:
                response, rcvaddress= localsock.recvfrom(10240)
            except Exception as e:
                continue
            if response == "" :
                self.OnError()
            else:
                jsondata = self.getJasonBody(response)
                if not jsondata:
                    addCaseLog("getVOIPnumberandPW failed, jason body is null = %s"%(jsondata))
                    continue 
                if jsondata.find("errorMsg") != -1:
                    addCaseLog("getVOIPnumberandPW failed, errormsg=%s"%(jsondata))
                    self.OnError()
                try:
                    t = json.loads(jsondata) 
                except Exception as e:
                    addCaseLog("getVOIPnumberandPW failed, errormsg=%s"%(e))
                    self.OnError()
                self.sipUserPassword = t.get('data').get('password')
                self.sipUserID = t.get('data').get('voipNum')
                self.sipDomain = t.get('data').get('sipDomain')
                self.webUserID = t.get('data').get('userId')
                addCaseLog("get SIPID success, sipUserID=%s,sipUserPassword = %s"%(self.sipUserID,self.sipUserPassword))
                SIP_ID_NUMBER = self.sipUserID
                SIP_ID_PASSWORD = self.sipUserPassword
                if self.sipUserID:
                    break
        localsock.close()        
    def getTimeStamp(self):
        time_struct = time.mktime(time.localtime(time.time()))
#         lt = time.localtime(time.time())
        utc_st = datetime.datetime.utcfromtimestamp(time_struct)
        timeStamp =  utc_st.strftime("%Y%m%d%H%M%S")
        return timeStamp
    def readyForsignature(self,data,securetyKey=""):
        spl = str(data).split("&")
        spl.sort()
        a = ""
        for i in range(0, len(spl)):
            a = a + spl[i]
            a = a + "&"
        a = a+ securetyKey
        a = a + "&"
        return a                                 
    def getWebAPISignatureHead(self,userDefinedParam = "", appid = "", secretKey=""):
        global APPID_FOR_WEBAPI_TEST,SECRETKEY_FOR_WEBAPI_TEST
        if not appid:
            appid = APPID_FOR_WEBAPI_TEST
        if not secretKey:
            secretKey = SECRETKEY_FOR_WEBAPI_TEST
        timeStamp = self.getTimeStamp()
        initStr1 = "appID=%s&charset=UTF-8&format=JSON&source=WIN&timeStamp=%s&version=1.0&%s&" % (appid,timeStamp,userDefinedParam)
        initStr = self.readyForsignature(initStr1,secretKey)
        m = hashlib.md5()
        m.update(initStr)
        signature = m.hexdigest()
        signatureResult = "source=WIN&version=1.0&charset=UTF-8&format=JSON&appID=%s&timeStamp=%s&signature=%s&%s" % (appid,timeStamp,signature,userDefinedParam)
        return signatureResult
    def getLoginPasswordEncode(self,passwordStr):
        m = hashlib.md5()
        m.update(passwordStr)
        return m.hexdigest()

class web_Exceptional_ReceivedPack(threading.Thread):
    
    def __init__( self, sock, local_address, local_port,test_API_NAME,meetingnumber="",meetingpassword="",sipnumber="",sippassword="",webUserID=""):
        threading.Thread.__init__(self)
        self.localsock = sock
        if local_address == "":
            self.localip = LOCAL_PC_IP
        else:
            self.localip = local_address
        if local_port == "":
            self.localport = LOCAL_PC_PORT
        else:
            self.localport = local_port
        self.loopsend = 0
        ########################
        self.received_head = ""
        self.recevied_body = ""
        self.method = ""
        self.APIURL = ""
        self.receivedURL = ""
        self.methodType = ""
        self.msg_isReq = ""
        self.errorCode_system = {'1':'10001','2':'10002','3':'10003','4':'10004','5':'10005','6':'10006','7':'10007','8':'10008','9':'20001','10':'20002'}
#         self.errorCode_system = {'1':'10001'}
        self.errorCode_httperror = {'1':'404','2':'505','3':'400','4':'500'}
        self.errorCode_noRespond = {'1':'timeout'}
        self.errorCode_self = {}
        self.test_API_NAME = test_API_NAME
        self.http_body = ""
        
        self.meetingnumber=meetingnumber
        self.meetingpassword = meetingpassword
        self.sipnumber = sipnumber
        self.sippassword = sippassword
        self.webUserID = webUserID
        self.protocol = 'tcp'
    def parseReceivedData( self, data, test_API_NAME,retcodeResult=""):
        global LOGIN_WEB_ACCOUNT
        if data == "":
            return "NONE"
        lines = str(data).split("\r\n")
        lineLen = len(lines)
        if lineLen == 0:
            return "NONE"
        result = int(lines[0][0:8].find('HTTP/1.1'))
        if result == -1:
            self.msg_isReq = True
            temp_buffer = lines[0].split(' ')
            if len(temp_buffer) < 1:
                return "NONE"
            self.methodType = temp_buffer[0]
            self.receivedURL = temp_buffer[1]
            self.recevied_body = str(lines[lineLen-1])
        else:
            self.methodType = temp_buffer[0]
            self.receivedURL = temp_buffer[0]
            
        if self.msg_isReq == False:
            self.recevied_body = str(lines[lineLen-1])        
        if test_API_NAME == "/common/sourcepermission":
            self.errorCode_self = {}
            self.http_body = "{\"data\":{\"android\":\"1,2,3,6,7\",\"gxp\":\"1,2,3,7\",\"gxv\":\"1,2,3,7\",\"ios\":\"1,2,3,6,7\",\"mac\":\"1,2,3,6,7\",\"oth"
            self.http_body += "er\":\"1,2,3,6,7\",\"pstn\":\"1,2\",\"websocket\":\"1,2,3,4,5,6,7,8,9\",\"windows\":\"1,2,3,4,5,6,7,8,9\"},\"retCode\":\""+ str(retcodeResult) + "\"}"
            self.errorCode_self = {}
        elif test_API_NAME == "/common/version":
            self.errorCode_self = {'1':'30009'}
            self.http_body = "{\"data\":{\"autoUpdate\":\"0\",\"fileName\":\"GSMeetingUpdate(v0.0.0.27).exe\",\"fileSize\":\"8483088\",\"version\":\"0.0.0.28\",\"versionId\":\"55\"},\"retCode\":\""+ str(retcodeResult) + "\"}"
        elif str(self.receivedURL).find("/common/clientdownload") != -1:
            self.http_body = "{\"data\":{\"url\":\"http://sip.grandstream.com\"},\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {'1':'30009','2':'30003'}
        elif test_API_NAME == "/user/login":
            self.http_body = "{\"data\":{\"accessToken\":\""+str(random.randint(0,10000))+"\",\"email\":\""+str(LOGIN_WEB_ACCOUNT) + "\",\"firstName\":\"fawe\",\"lastName\":\"amanda\",\"nameShow\":\"0\"},\"retCode\":\""+ str(retcodeResult) + "\"}"
            self.errorCode_self = {'1':'40003','2':'40006','3':'40008'}
        elif str(self.receivedURL).find("/meeting/join_meeting_info") != -1:
            if self.meetingpassword == "":
                self.http_body =  "{\"data\":{\"attendLimit\":\"100\",\"duration\":\"60\",\"endTime\":\"20150324071923\",\"fileSizeLimit\":\"4194304\",\"invitesList\":\"a1@gs.com,\",\"master\":\"53\",\"meetingNum\":\"" + str(self.meetingnumber)+ "\",\"micLimit\":\"10\",\"needPassword\":\"0\",\"serialNum\":\"2FA95DE441CD41C5AF608BC85C11AD69\",\"startTime\":\"20150324061923\",\"status\":\"1\",\"theme\":\"a1  mytest's meeting\",\"url\":\"http://meetings.ipvideotalk.com/join?meetingNum=" + str(self.meetingnumber)+ "\"},\"retCode\":\"" + str(retcodeResult) + "\"}"
            else:
                self.http_body =  "{\"data\":{\"attendLimit\":\"100\",\"duration\":\"60\",\"endTime\":\"20150324071923\",\"fileSizeLimit\":\"4194304\",\"invitesList\":\"a1@gs.com,\",\"master\":\"53\",\"meetingNum\":\"" + str(self.meetingnumber)+ "\",\"micLimit\":\"10\",\"needPassword\":\"1\",\"serialNum\":\"2FA95DE441CD41C5AF608BC85C11AD69\",\"startTime\":\"20150324061923\",\"status\":\"1\",\"theme\":\"a1  mytest's meeting\",\"url\":\"http://meetings.ipvideotalk.com/join?meetingNum=" + str(self.meetingnumber)+ "\"},\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {'1':'20008','2':'20009','3':'20010','4':'20012','5':'20013','6':'20015','7':'20016'}
        elif str(self.receivedURL).find("/user/query") != -1:
            self.http_body = "{\"data\":{\"email\":\""+str(LOGIN_WEB_ACCOUNT) + "\",\"firstName\":\"ddddd\",\"lastName\":\"Wake up\"},\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {}
        elif str(self.receivedURL) == "/user/voip":
            self.http_body = "{\"data\":{\"password\":\"" + str(self.sippassword)+ "\",\"sipDomain\":\"opensip-5060-512954155.us-west-2.elb.amazonaws.com\",\"state\":\"1\",\"userId\":\"53\",\"voipNum\":\"" + str(self.sipnumber)+ "\"},\"retCode\":\"" + str(retcodeResult) + "\"}"
            print "voip body = %s" % str(self.http_body)
            self.errorCode_self = {'1':'40007'}
        elif str(self.receivedURL).find("/user/voip_tourist") != -1:
            self.http_body = "{\"data\":{\"password\":\"" + str(self.sippassword)+ "\",\"sipDomain\":\"opensip-5060-512954155.us-west-2.elb.amazonaws.com\",\"state\":\"1\",\"voipNum\":\"" + str(self.sipnumber)+ "\"},\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {'1':'50001','2':'50002','3':'50003','4':'40005','5':'20007'}
        elif test_API_NAME == "/meeting/quick_start":
            self.http_body = "{\"data\":{\"meetingNum\":\"" + str(self.meetingnumber)+ "\",\"password\":\""+str(self.meetingpassword) + "\",\"serialNum\":\"9D364713AA2949A0AFC0716EC23004B8\"},\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {'1':'40004','2':'20011'}
        elif str(self.receivedURL).find("/user/logout") != -1:
            self.http_body = "{\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {}
        elif str(self.receivedURL).find("/user/update_password") != -1:
            self.http_body = "{\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {'1':'40006','2':'50004'}
        elif str(self.receivedURL).find("/meeting/list") != -1:
            self.http_body = "{\"data\":[{\"endTime\":\"20150226090526\",\"isCycle\":\"0\",\"master\":\"53\",\"meetingNum\":\"" + str(self.meetingnumber)+ "\",\"participants\":\"1\",\"serialNum\":\"D0703B532F324038AEC04ED0B90C153A\",\"startTime\":\"20150226080526\",\"status\":\"-2\",\"theme\":\"meeting status=-2\",\"timeShow\":\"16:05 PM-17:05 PM(GMT+08:00) Beijing, Chongqing, Hong Kong, Urumqi\",\"timeZone\":\"Asia/Shanghai\",\"url\":\"http://meetings.ipvideotalk.com/27526722\",\"userTimeZone\":\"Asia/Shanghai\"},{\"endTime\":\"20150318090824\",\"isCycle\":\"0\",\"master\":\"53\",\"meetingNum\":\"" + str(self.meetingnumber)+ "\",\"participants\":\"1\",\"serialNum\":\"6CBEA7B1A87A4322AF80973561900CB0\",\"startTime\":\"20150318080824\",\"status\":\"-1\",\"theme\":\"meeting status=-1\",\"timeShow\":\"16:08 PM-17:08 PM(GMT+08:00) Beijing, Chongqing, Hong Kong, Urumqi\",\"timeZone\":\"Asia/Shanghai\",\"url\":\"http://meetings.ipvideotalk.com/48349224\",\"userTimeZone\":\"Asia/Shanghai\"},{\"endTime\":\"20150318090836\",\"isCycle\":\"0\",\"master\":\"53\",\"meetingNum\":\"41399325\",\"participants\":\"1\",\"serialNum\":\"C8FEF0CEA55444EF8C673C2F2E2B138E\",\"startTime\":\"20150318080836\",\"status\":\"0\",\"theme\":\"meeting status=0\",\"timeShow\":\"16:08 PM-17:08 PM(GMT+08:00) Beijing, Chongqing, Hong Kong, Urumqi\",\"timeZone\":\"Asia/Shanghai\",\"url\":\"http://meetings.ipvideotalk.com/41399325\",\"userTimeZone\":\"Asia/Shanghai\"},{\"endTime\":\"20150318090848\",\"isCycle\":\"0\",\"master\":\"53\",\"meetingNum\":\"44309726\",\"participants\":\"1\",\"serialNum\":\"CB5A2C212125448A9FEC1E2E19819D80\",\"startTime\":\"20150318080848\",\"status\":\"1\",\"theme\":\"meeting status=1\",\"timeShow\":\"16:08 PM-17:08 PM(GMT+08:00) Beijing, Chongqing, Hong Kong, Urumqi\",\"timeZone\":\"Asia/Shanghai\",\"url\":\"http://meetings.ipvideotalk.com/44309726\",\"userTimeZone\":\"Asia/Shanghai\"},{\"endTime\":\"20150318091000\",\"isCycle\":\"0\",\"master\":\"53\",\"meetingNum\":\"45339227\",\"participants\":\"1\",\"serialNum\":\"AA57BC2DB2414381801E18E75028FD01\",\"startTime\":\"20150318081000\",\"status\":\"2\",\"theme\":\"meeting status=2\",\"timeShow\":\"16:10 PM-17:10 PM(GMT+08:00) Beijing, Chongqing, Hong Kong, Urumqi\",\"timeZone\":\"Asia/Shanghai\",\"url\":\"http://meetings.ipvideotalk.com/45339227\",\"userTimeZone\":\"Asia/Shanghai\"},{\"endTime\":\"20150318091128\",\"isCycle\":\"1\",\"master\":\"53\",\"meetingNum\":\"46339629\",\"participants\":\"1\",\"serialNum\":\"13FF49E01451495E9EA1D5F6E5200F98\",\"startTime\":\"20150318081128\",\"status\":\"3\",\"theme\":\"meeting status=3\",\"timeShow\":\"16:11 PM-17:11 PM(GMT+08:00) Beijing, Chongqing, Hong Kong, Urumqi\",\"timeZone\":\"Asia/Shanghai\",\"url\":\"http://meetings.ipvideotalk.com/46339629\",\"userTimeZone\":\"Asia/Shanghai\"},{\"endTime\":\"20150320050333\",\"isCycle\":\"0\",\"master\":\"53\",\"meetingNum\":\"43423316\",\"participants\":\"1\",\"serialNum\":\"58629DC832344A8A977CDE7DF20F00A7\",\"startTime\":\"20150320040333\",\"status\":\"4\",\"theme\":\"meeting status=4\",\"timeShow\":\"12:03 PM-13:03 PM(GMT+08:00) Beijing, Chongqing, Hong Kong, Urumqi\",\"timeZone\":\"Asia/Shanghai\",\"url\":\"http://meetings.ipvideotalk.com/43423316\",\"userTimeZone\":\"Asia/Shanghai\"},{\"endTime\":\"20150320050356\",\"isCycle\":\"0\",\"master\":\"53\",\"meetingNum\":\"44433418\",\"participants\":\"1\",\"serialNum\":\"99AB8CDB66A54166821188CC91200D31\",\"startTime\":\"20150320040356\",\"status\":\"5\",\"theme\":\"meeting status=5\",\"timeShow\":\"12:03 PM-13:03 PM(GMT+08:00) Beijing, Chongqing, Hong Kong, Urumqi\",\"timeZone\":\"Asia/Shanghai\",\"url\":\"http://meetings.ipvideotalk.com/44433418\",\"userTimeZone\":\"Asia/Shanghai\"},{\"endTime\":\"20150320051312\",\"isCycle\":\"1\",\"master\":\"53\",\"meetingNum\":\"49463036\",\"participants\":\"1\",\"serialNum\":\"5625D34ECA8B471F8DE042FBDF45B8BC\",\"startTime\":\"20150320041312\",\"status\":\"2\",\"theme\":\"meeting status=2 cycle=1\",\"timeShow\":\"12:13 PM-13:13 PM(GMT+08:00) Beijing, Chongqing, Hong Kong, Urumqi\",\"timeZone\":\"Asia/Shanghai\",\"url\":\"http://meetings.ipvideotalk.com/49463036\",\"userTimeZone\":\"Asia/Shanghai\"},{\"endTime\":\"20150320051413\",\"isCycle\":\"1\",\"master\":\"53\",\"meetingNum\":\"43453840\",\"participants\":\"1\",\"serialNum\":\"853C0B6D47BD48CEAAD65C01B8E77676\",\"startTime\":\"20150320041413\",\"status\":\"2\",\"theme\":\"meeting  status=2 cycle=1\",\"timeShow\":\"12:14 PM-13:14 PM(GMT+08:00) Beijing, Chongqing, Hong Kong, Urumqi\",\"timeZone\":\"Asia/Shanghai\",\"url\":\"http://meetings.ipvideotalk.com/43453840\",\"userTimeZone\":\"Asia/Shanghai\"}],\"pageNum\":\"1\",\"totalNum\":\"29\",\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {}
        elif str(self.receivedURL).find("/meeting/upcomings") != -1:
            self.http_body = "{\"data\":[{\"endTime\":\"20150226090526\",\"isCycle\":\"0\",\"master\":\"53\",\"meetingNum\":\"" + str(self.meetingnumber)+ "\",\"participants\":\"1\",\"serialNum\":\"D0703B532F324038AEC04ED0B90C153A\",\"startTime\":\"20150226080526\",\"status\":\"2\",\"theme\":\"a1  mytest's meeting\",\"timeShow\":\"16:05 PM-17:05 PM(GMT+08:00) Beijing, Chongqing, Hong Kong, Urumqi\",\"timeZone\":\"Asia/Shanghai\",\"url\":\"http://meetings.ipvideotalk.com/27526722\",\"userTimeZone\":\"Asia/Shanghai\"}],\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {}
  
        elif str(self.receivedURL).find("/meeting/attendees_list") != -1:
            self.http_body =  "{\"data\":{[{\"email\":\"amanda@grandstream.com\",\"name\":\"Amanda Shan\"}]},\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {}
        elif str(self.receivedURL).find("/user/voip_attendee_info") != -1:
            self.http_body =  "{\"data\":{[{\"email\":\"amanda@grandstream.com\",\"firstName\":\"Amanda Shan\",\"lastName\":\"Amanda Shan\",\"voipNum\":\"" + str(self.sipnumber)+ "\"}]},\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {}
        elif str(self.receivedURL).find("/meeting/delete") != -1:
            self.http_body = "{\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {'1':'20017','2':'20012','3':'20000'}
        elif str(self.receivedURL).find("/meeting/invite") != -1:
            self.http_body = "{\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {'1':'20012','2':'20009','3':'20015','4':'20016'}
            addCaseLog( "%s errorCode_self len = %d" % (test_API_NAME,len(self.errorCode_self)))
        elif str(self.receivedURL).find("/user/checkregist") != -1:
            self.http_body = "{\"data\":{\"checkcode\":\"0\"},\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {}
        ######################meeting setting API###################
        elif str(self.receivedURL).find("/user/userupdate") != -1:
            self.http_body = "{\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {'1':'40001','2':'50002','3':'50003'}
        elif str(self.receivedURL) == "/user/setting/quickstart":
            self.http_body = "{\"data\":{\"attendListState\":\"0\",\"autoRec\":\"0\",\"chatPromptSound\":\"0\",\"chatState\":\"0\",\"fileTransferState\":\"0\",\"isSendEmail\":\"0\",\"loginPromptState\":\"1\",\"logoutPromptState\":\"1\",\"meetingTitle\":\"a1  mytest's meeting\",\"muteState\":\"0\",\"password\":\""+str(self.meetingpassword) + "\",\"pstn\":\"2\"},\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {'1':'20011'}
        elif str(self.receivedURL).find("/user/setting/quickstart_update") != -1:
            self.http_body = "{\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {'1':'40002'}
        ####################chat file API#####################
        elif str(self.receivedURL).find("/file/conf/list") != -1:
            self.http_body = "{\"data\":[{\"creatTime\":\"20150324072732\",\"fileID\":\"hggSwpggSBK7YiVjK5dH8w\",\"fileName\":\"GSMeeting.lnk\",\"meetingNum\":\"" + str(self.meetingnumber)+ "\",\"serialNum\":\"C5EE95E35643463EA4A38CFCD5F5CB83\",\"size\":\"989\",\"state\":\"1\",\"uploadId\":\"96\",\"userID\":\""+ str(self.webUserID) +"\"}],\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {}
        elif str(self.receivedURL).find("/file/delete") != -1:
            self.http_body = "{\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {'1':'30009','2':'10006','3':'30001'}
        elif str(self.receivedURL).find("/upload") != -1:
            self.http_body = "{\"data\":{\"bucket\":\"\",\"fileId\":\"hggSwpggSBK7YiVjK5dH8w\",\"filePath\":\"http://meetings.ipvideotalk.com/api/file/a/tmpurl/hggSwpggSBK7YiVjK5dH8w\"},\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {'1':'30017','2':'20012','3':'30001','4':'30008','5':'30004','6':'30006','7':'30007','8':'-1'}
        elif str(self.receivedURL).find("/file/conf/getAccessUrl") != -1:
            self.http_body = "{\"data\":{\"url\":\"http://gs-storage-server-og-hz-test2.s3.amazonaws.com/meeting/54/2015/3/25/zXO2U81GSl6l_QnLU2Zngg.log?response-content-disposition=attachment%3Bfilename%3Dmonitor.log&AWSAccessKeyId=AKIAJZHSIZRVYIRFL4MA&Expires=1427269583&Signature=2c9HIu65yQ638NY52GTwmb%2BwTqk%3D\"},\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {'1':'30009','2':'30003','3':'30010'}
        ######################### meeting remind API #####################
        elif str(self.receivedURL).find("/meeting/msgdelete") != -1:
            self.http_body = "{\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {}
        elif str(self.receivedURL).find("/meeting/remindlater") != -1:
            self.http_body = "{\"data\":{},\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {}
        elif str(self.receivedURL).find("/meeting/msglist") != -1:
            self.http_body = "{\"data\":[{\"endTime\":\"20150226090526\",\"isCycle\":\"0\",\"master\":\"53\",\"meetingNum\":\"" + str(self.meetingnumber)+ "\",\"participants\":\"1\",\"serialNum\":\"D0703B532F324038AEC04ED0B90C153A\",\"startTime\":\"20150226080526\",\"status\":\"2\",\"theme\":\"a1  mytest's meeting\",\"timeShow\":\"16:05 PM-17:05 PM(GMT+08:00) Beijing, Chongqing, Hong Kong, Urumqi\",\"timeZone\":\"Asia/Shanghai\",\"url\":\"http://meetings.ipvideotalk.com/27526722\",\"userTimeZone\":\"Asia/Shanghai\"}],\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {}

###################need modify##################
        elif str(self.receivedURL).find("/file/share/share_all") != -1:
            self.http_body = "{\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {}
        elif str(self.receivedURL).find("/gateway/create_meeting") != -1:
            self.http_body = "{\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {'1':'40002'}
        elif str(self.receivedURL).find("/gateway/forget_password") != -1:
            self.http_body = "{\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {'1':'40002'}
        elif str(self.receivedURL).find("/gateway/signup") != -1:
            self.http_body = "{\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {'1':'40002'}


        elif str(self.receivedURL).find("/file/checkcanrecord") != -1:
            self.http_body = "{\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {'1':'40002'}
        elif str(self.receivedURL).find("/common/allcountry") != -1:
            self.http_body = "{\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {'1':'40002'}
        else:
            self.http_body = "{\"retCode\":\"" + str(retcodeResult) + "\"}"
            self.errorCode_self = {}

    #options=0： https status is correct，retcode not correct
    def sendAPIRespond(self,sock,data,test_API_NAME,retcodeResult,options=0):
        
        if retcodeResult =="":
            retCodeResult = 0
        result = ""
        self.parseReceivedData( data, test_API_NAME,retcodeResult)
        addCaseLog("received client request, request_line = %s %s" % (self.methodType,self.receivedURL))

        if options == 0:
            http_200OK_Head = "HTTP/1.1 200 OK \r\n"
            http_200OK_Head += "Server: nginx/1.0.15 \r\n"
            http_200OK_Head += "Date: Mon, 08 Dec 2014 03:16:31 GMT \r\n"
            http_200OK_Head += "Content-Type: text/plain;charset=UTF-8 \r\n"
            http_200OK_Head += "Connection: keep-alive \r\n"
            http_200OK_Head += "Accept-Charset: big5, big5-hkscs, euc-jp, euc-kr, gb18030, gb2312, gbk, ibm-thai, ibm00858, ibm01140, ibm01141, "
            http_200OK_Head += "ibm01142, ibm01143, ibm01144, ibm01145, ibm01146, ibm01147, ibm01148, ibm01149, ibm037, ibm1026, ibm1047, ibm273, ibm277, ibm278, "
            http_200OK_Head += "ibm280, ibm284, ibm285, ibm290, ibm297, ibm420, ibm424, ibm437, ibm500, ibm775, ibm850, ibm852, ibm855, ibm857, ibm860, ibm861, ibm862, "
            http_200OK_Head += "ibm863, ibm864, ibm865, ibm866, ibm868, ibm869, ibm870, ibm871, ibm918, iso-2022-cn, iso-2022-jp, iso-2022-jp-2, iso-2022-kr, iso-8859-1, "
            http_200OK_Head += "iso-8859-13, iso-8859-15, iso-8859-2, iso-8859-3, iso-8859-4, iso-8859-5, iso-8859-6, iso-8859-7, iso-8859-8, iso-8859-9, jis_x0201, jis_"
            http_200OK_Head += "x0212-1990, koi8-r, koi8-u, shift_jis, tis-620, us-ascii, utf-16, utf-16be, utf-16le, utf-32, utf-32be, utf-32le, utf-8, windows-1250, "
            http_200OK_Head += "windows-1251, windows-1252, windows-1253, windows-1254, windows-1255, windows-1256, windows-1257, windows-1258, windows-31j, "
            http_200OK_Head += "x-big5-hkscs-2001, x-big5-solaris, x-compound_text, x-euc-jp-linux, x-euc-tw, x-eucjp-open, x-ibm1006, x-ibm1025, x-ibm1046, "
            http_200OK_Head += "x-ibm1097, x-ibm1098, x-ibm1112, x-ibm1122, x-ibm1123, x-ibm1124, x-ibm1364, x-ibm1381, x-ibm1383, x-ibm300, x-ibm33722, x-ibm737, "
            http_200OK_Head += "x-ibm833, x-ibm834, x-ibm856, x-ibm874, x-ibm875, x-ibm921, x-ibm922, x-ibm930, x-ibm933, x-ibm935, x-ibm937, x-ibm939, x-ibm942, "
            http_200OK_Head += "x-ibm942c, x-ibm943, x-ibm943c, x-ibm948, x-ibm949, x-ibm949c, x-ibm950, x-ibm964, x-ibm970, x-iscii91, x-iso-2022-cn-cns, "
            http_200OK_Head += "x-iso-2022-cn-gb, x-iso-8859-11, x-jis0208, x-jisautodetect, x-johab, x-macarabic, x-maccentraleurope, x-maccroatian, x-maccyrillic, "
            http_200OK_Head += "x-macdingbat, x-macgreek, x-machebrew, x-maciceland, x-macroman, x-macromania, x-macsymbol, x-macthai, x-macturkish, x-macukraine, "
            http_200OK_Head += "x-ms932_0213, x-ms950-hkscs, x-ms950-hkscs-xp, x-mswin-936, x-pck, x-sjis_0213, x-utf-16le-bom, x-utf-32be-bom, x-utf-32le-bom, "
            http_200OK_Head += "x-windows-50220, x-windows-50221, x-windows-874, x-windows-949, x-windows-950, x-windows-iso2022jp\r\n"
            http_len = "Content-Length: " + str(len(self.http_body)) + "\r\n\r\n"
            result = http_200OK_Head + str(http_len)+ str(self.http_body)
        else:
            http_200OK_Head = "HTTP/1.1 %s HTTP Version Not Supported \r\n" % (str(retcodeResult))
            http_200OK_Head += "Server: nginx/1.0.15 \r\n"
            http_200OK_Head += "Date: Mon, 08 Dec 2014 03:16:31 GMT \r\n"
            http_200OK_Head += "Connection: keep-alive \r\n\r\n"
            result = http_200OK_Head + str(0)
        addCaseLog("I will respond you ,body = %s" % str(self.http_body))
        try:
            sock.sendall(result)
        except Exception as e:
            addCaseLog("send http %s failed, result = %s" % (str(self.http_body),str(e)))
    
    def loopSendErrorCode(self,sendsock,data,test_API_NAME):
        global LOOPTIMES_webAPI_errorCode
        if LOOPTIMES_webAPI_errorCode <= len(self.errorCode_system):
            keyValue = str(LOOPTIMES_webAPI_errorCode)
            addCaseLog( "[1] Start ServerCommon exception test, total test time = %s,retCode = %s,http status code = %s" % (LOOPTIMES_webAPI_errorCode,self.errorCode_system[keyValue],"200OK"))
            self.sendAPIRespond(sendsock,data,self.test_API_NAME,self.errorCode_system[keyValue])
            LOOPTIMES_webAPI_errorCode += 1
        elif LOOPTIMES_webAPI_errorCode <= len(self.errorCode_system)+len(self.errorCode_self):
            keyValue = str(LOOPTIMES_webAPI_errorCode-len(self.errorCode_system))
            addCaseLog( "[2] Start ServerCommon exception test, total test time = %s,retCode = %s,http status code = %s" % (LOOPTIMES_webAPI_errorCode,self.errorCode_self[keyValue],"200OK"))
            self.sendAPIRespond(sendsock,data,self.test_API_NAME,self.errorCode_self[keyValue])
            LOOPTIMES_webAPI_errorCode += 1
        elif LOOPTIMES_webAPI_errorCode <= len(self.errorCode_system)+len(self.errorCode_self)+len(self.errorCode_httperror):
            keyValue = str(LOOPTIMES_webAPI_errorCode-len(self.errorCode_system)-len(self.errorCode_self))
            addCaseLog( "[3] Start ServerCommon exception test, total test time = %s,retCode = %s,http status code = %s" % (LOOPTIMES_webAPI_errorCode,"0",self.errorCode_httperror[keyValue]))
            self.sendAPIRespond(sendsock,data,self.test_API_NAME,self.errorCode_httperror[keyValue],1)
            LOOPTIMES_webAPI_errorCode += 1
        elif LOOPTIMES_webAPI_errorCode <= len(self.errorCode_system)+len(self.errorCode_self)+len(self.errorCode_httperror)+len(self.errorCode_noRespond):
            keyValue = str(LOOPTIMES_webAPI_errorCode-len(self.errorCode_system)-len(self.errorCode_self)-len(self.errorCode_httperror))
            addCaseLog( "[4] Start timeout exception test, total test time = %s,no http respond" % (LOOPTIMES_webAPI_errorCode))
#           self.sendAPIResule(sendsock,self.test_API_NAME,self.errorCode_noRespond[keyValue],1)
            LOOPTIMES_webAPI_errorCode += 1
        else:
            addCaseLog( "[5] Start Normal respond, total test time = %s,retCode = %s,http status code = %s" % (LOOPTIMES_webAPI_errorCode,"0","200OK"))
            self.sendAPIRespond(sendsock,data,test_API_NAME,0,0)
            addCaseLog( "Dear, we finshed \"%s\" errorCode test, total test time = %s , clear the environment" % (self.test_API_NAME,LOOPTIMES_webAPI_errorCode))
            LOOPTIMES_webAPI_errorCode = 1
            addCaseLog( "Now you can start \"%s\" test again, test time setted to = %s" % (self.test_API_NAME,LOOPTIMES_webAPI_errorCode))
            
    def testedAPIandSend(self,sendsock,data,receivedURL,test_API_NAME):
        if str(self.receivedURL).find(test_API_NAME) != -1:
            addCaseLog("###### WoW, received tested API request, start set error coding#####")
            self.loopSendErrorCode(sendsock,data,test_API_NAME) 
        elif str(self.receivedURL).find("/common/sourcepermission") != -1:
            self.sendAPIRespond(sendsock,data,"/common/sourcepermission",0,0)
        elif str(self.receivedURL).find("/common/version") != -1:
            self.sendAPIRespond(sendsock,data,"/common/version",0,0)
        elif str(self.receivedURL).find("/user/login") != -1:
            self.sendAPIRespond(sendsock,data,"/user/login",0,0)
        elif str(self.receivedURL).find("/user/logout") != -1:
            self.sendAPIRespond(sendsock,data,"/user/logout",0,0)
        elif str(self.receivedURL).find("/user/update_password") != -1:
            self.sendAPIRespond(sendsock,data,"/user/update_password",0,0)
        elif str(self.receivedURL).find("/user/update_password") != -1:
            self.sendAPIRespond(sendsock,data,"/user/update_password",0,0)
        elif str(self.receivedURL).find("/meeting/list") != -1:
            self.sendAPIRespond(sendsock,data,"/meeting/list",0,0)           
        elif str(self.receivedURL).find("/meeting/upcomings") != -1:
            self.sendAPIRespond(sendsock,data,"/meeting/upcomings",0,0)            
        elif str(self.receivedURL).find("/meeting/join_meeting_info") != -1:
            self.sendAPIRespond(sendsock,data,"/meeting/join_meeting_info",0,0)
        elif str(self.receivedURL).find("/user/query") != -1:
            self.sendAPIRespond(sendsock,data,"/user/query",0,0)
        elif str(self.receivedURL).find("/user/voip") != -1:
            self.sendAPIRespond(sendsock,data,"/user/voip",0,0)
        elif str(self.receivedURL).find("/user/voip_tourist") != -1:
            self.sendAPIRespond(sendsock,data,"/user/voip_tourist",0,0)           
        elif str(self.receivedURL).find("/meeting/attendees_list") != -1:
            self.sendAPIRespond(sendsock,data,"/meeting/attendees_list",0,0)            
        elif str(self.receivedURL).find("/user/voip_attendee_info") != -1:
            self.sendAPIRespond(sendsock,data,"/user/voip_attendee_info",0,0)


        elif str(self.receivedURL).find("/meeting/delete") != -1:
            self.sendAPIRespond(sendsock,data,"/meeting/delete",0,0)
        elif str(self.receivedURL).find("/meeting/invite") != -1:
            self.sendAPIRespond(sendsock,data,"/meeting/invite",0,0)           
        elif str(self.receivedURL).find("/file/conf/list") != -1:
            self.sendAPIRespond(sendsock,data,"/file/conf/list",0,0)            
        elif str(self.receivedURL).find("/file/conf/getAccessUrl") != -1:
            self.sendAPIRespond(sendsock,data,"/file/conf/getAccessUrl",0,0)
            
        elif str(self.receivedURL).find("/file/delete") != -1:
            self.sendAPIRespond(sendsock,data,"/file/delete",0,0)
        elif str(self.receivedURL).find("/file/share/share_all") != -1:
            self.sendAPIRespond(sendsock,data,"/file/share/share_all",0,0)           
        elif str(self.receivedURL).find("/meeting/quick_start") != -1:
            self.sendAPIRespond(sendsock,data,"/meeting/quick_start",0,0)            
        elif str(self.receivedURL).find("/gateway/create_meeting") != -1:
            self.sendAPIRespond(sendsock,data,"/gateway/create_meeting",0,0)  
                      
        elif str(self.receivedURL).find("/gateway/forget_password") != -1:
            self.sendAPIRespond(sendsock,data,"/gateway/forget_password",0,0)
        elif str(self.receivedURL).find("/gateway/signup") != -1:
            self.sendAPIRespond(sendsock,data,"/gateway/signup",0,0)           
        elif str(self.receivedURL).find("/meeting/msglist") != -1:
            self.sendAPIRespond(sendsock,data,"/meeting/msglist",0,0)            
        elif str(self.receivedURL).find("/meeting/msgdelete") != -1:
            self.sendAPIRespond(sendsock,data,"/meeting/msgdelete",0,0)    
            
        elif str(self.receivedURL).find("/user/checkregist") != -1:
            self.sendAPIRespond(sendsock,data,"/user/checkregist",0,0)
        elif str(self.receivedURL).find("/meeting/remindlater") != -1:
            self.sendAPIRespond(sendsock,data,"/meeting/remindlater",0,0)           
        elif str(self.receivedURL).find("/user/userupdate") != -1:
            self.sendAPIRespond(sendsock,data,"/user/userupdate",0,0)            
        elif str(self.receivedURL).find("/user/setting/quickstart") != -1:
            self.sendAPIRespond(sendsock,data,"/user/setting/quickstart",0,0)   


        elif str(self.receivedURL).find("/user/setting/quickstart_update") != -1:
            self.sendAPIRespond(sendsock,data,"/user/setting/quickstart_update",0,0)
        elif str(self.receivedURL).find("/file/checkcanrecord") != -1:
            self.sendAPIRespond(sendsock,data,"/file/checkcanrecord",0,0)           
        elif str(self.receivedURL).find("/common/allcountry") != -1:
            self.sendAPIRespond(sendsock,data,"/common/allcountry",0,0)            
        elif str(self.receivedURL).find("/common/version") != -1:
            self.sendAPIRespond(sendsock,data,"/common/version",0,0)

        elif str(self.receivedURL).find("/common/clientdownload") != -1:
            self.sendAPIRespond(sendsock,data,"/common/clientdownload",0,0)
        elif str(self.receivedURL).find("/upload") != -1:
            self.sendAPIRespond(sendsock,data,"/upload",0,0)  
        else:
            self.sendAPIRespond(sendsock,data,"",0,0)  
                                             
    def run(self):
        global service_on
        global LOOPTIMES_webAPI_errorCode
        sendsock = self.localsock
        while service_on:
            try:
                if self.protocol == 'udp':
                    response, rcvaddress= sendsock.recvfrom(10240)
                else:
                    response = sendsock.recv(10240)
            except Exception as e:
                continue
            if not response:
                continue
            self.parseReceivedData(response, self.test_API_NAME)
            if self.msg_isReq != "NONE" and self.msg_isReq != "":
                self.testedAPIandSend(sendsock,response,self.receivedURL,self.test_API_NAME)
            else:
                addCaseLog("respond::%s  response is received\r\n" % (self.methodType))
                continue
        sendsock.close()

class web_Exceptional_Common(projectx_base):
    def __init__(self,test_API_NAME="login",localaddress = '',localport = '',meetingnumber="",meetingpassword="",sipnumber="",sippassword=""):
        global WEB_SERVER_IP,WEB_SERVER_PORT,LOGIN_WEB_ACCOUNT,LOGIN_WEB_ACCOUNT_PASSWORD
        if localport == "":
            self.localport = LOCAL_PC_PORT
        else:
            self.localport = localport
        if localaddress == "":
            self.localaddress = LOCAL_PC_IP
        else:
            self.localaddress = localaddress
        self.sock = ""
        if test_API_NAME =="":
            self.test_API_NAME = "login"
        else:
            self.test_API_NAME = test_API_NAME
        self.meetingpassword = meetingpassword
        self.meetingnumber=meetingnumber
        self.sipnumber = sipnumber
        self.sippassword = sippassword
        webuser = webAPI(WEB_SERVER_IP,WEB_SERVER_PORT, self.localaddress, self.localport,LOGIN_WEB_ACCOUNT,LOGIN_WEB_ACCOUNT_PASSWORD)
        if meetingnumber == "":
            addCaseLog("MeetingNumber is emptly , starting created a meeting now....")
            webuser.getQuickStartMeetingID()
            self.meetingnumber = webuser.meetingID
            self.meetingpassword = webuser.meetingPassword
        if sipnumber == "":
            addCaseLog("your Sip account is emptly , starting to get login user's SIPID....")
            webuser.getVOIPnumberandPW()
            self.sipnumber = webuser.sipUserID
            self.sippassword = webuser.sipUserPassword
            self.webUserID = webuser.webUserID

    def startWebServer(self,localip,localport):
        global service_on
        sendsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = sendsock
        try:
            self.sock.bind(('%s' % self.localaddress, localport))
#             self.sock.settimeout(3)
        except socket.error or socket.timeout:
            self.sock.close()
            self.OnError()
        self.sock.listen(10)
        addCaseLog("################## WEB simulator server started success, now i am listening################")
        addCaseLog("Server IP = %s, port = %s, testAPI = %s,please add in GS meeting config file(webport=%s,weburl:%s and hosts file)" %(localip,localport,self.test_API_NAME,localport,localport))
        while service_on:
            connection, client_address = self.sock.accept()
            T1 = web_Exceptional_ReceivedPack(connection, client_address, localport, self.test_API_NAME,self.meetingnumber,self.meetingpassword,self.sipnumber,self.sippassword,self.webUserID)
            T1.start()
    def OnRun(self):
        self.startWebServer(self.localaddress,int(self.localport))
        
    def OnError(self):
        addCaseLog("web_Exceptional::OnError, case failed")
        setCaseResult("failed")
        sys.exit()

class xserver_Exceptional_ReceivedPack(sipServer_commonlib):
    def __init__( self, sock,service_msg,sipMethod,testnum,role):
        sipServer_commonlib.__init__(self,service_msg)
        self.localsock = sock
        self.loopsend = 0
        ########################
        self.errorCode_system = {'1':'1000','2':'1001','3':'1002','4':'1003','5':'1004','6':'1005','7':'1006','8':'1007','9':'1008',\
                                 '10':'1009','11':'1010','12':'1011','13':'1012','14':'1013','15':'1014','16':'1015','17':'1016','18'\
                                 :'1017','19':'1018','20':'1019','21':'1020','22':'1021','23':'1022','24':'1023','25':'1024','26':'1025','27':'1026','28':'1027'\
                                 ,'29':'1028','30':'1029','31':'1030','32':'1031','33':'1032','34':'1033','35':'1034','36':'3000','37':'3001','38':'3002','39':\
                                 '3003','40':'3004','41':'3005','41':'3006','42':'3007','43':'3008','44':'3009','45':'3010','46':'3011','47':'3012',\
                                 '48':'5003','49':'5004','50':'5005','51':'5006','52':'5007','53':'5008','54':'5009','55':'5010','56':'5011',\
                                 '57':'5012','58':'5013','59':'5014','60':'30008'}
        
        self.errorCode_Statuserror = {'1':'404','2':'505','3':'400','4':'500','5':'481','6':'403'}
#         self.errorCode_Statuserror = {'1':'404'}
        self.errorCode_noRespond = {'1':'timeout'}
        self.sipMethod = sipMethod
        
        if testnum == "":
            testnum = 2
        self.testnum = testnum
        self.infoReceivedTime = 0
        self.av_invite_totag = "NONE"
        self.call_id = "NONE"
        self.role = role
        self.refreshTime = 1

    def getINFOactionData(self,data):
        if data:
            a = str(data).split(";")
            for i in a:
                if str(a[i]).find("action") != -1:
                    print ("getINFOactionData,result = %s" % a[i][7:])
                    return a[i][7:]
                
    def getMeetingIDAndPW(self,sock,msg_info):
        
        meetinginfo = msg_info.meeting_id_to_user
#         str(meetinginfo).find(*)

    def send_Nofity(self,sock,msg_info,flag=0):

        if msg_info.rtp_media_port == "":
            msg_info.rtp_media_port = self.rtp_port
        if msg_info.user_agent == "":
            msg_info.user_agent = 'windows'
        if msg_info.display_name == "":
            msg_info.display_name = self.display_name
        if msg_info.meeting_id_to_user == "":
            addCaseLog("meeting number is empty (send_invite)")
            self.OnError()
        # send INVITE request to sip server
        if msg_info.cseq_num == "":
            msg_info.cseq_num = XSERVER_PUBLICKEY["cseq_num_all"]
        #flag = 1(join meeting notify), flag = 2(start recording),flag=3(stop recording)
        if flag == 1:
            park_content = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\r\n<conference-info refresh=\"1\" entity=\"%s\" state=\"partial\" s=\"0000100001\" options=\"10\" time=\"20150413061340_20150413061340\"><users><user entity=\"%s\" state=\"full\" display=\"A a5\" ua=\"windows\" type=\"1\" s=\"0011\" options=\"10\"/></users></conference-info>" %(msg_info.meeting_id_to_user,str(msg_info.sipid_number))
            self.refreshTime += 1
        elif str(str(msg_info.x_gs_conf_control).find("get_all_users")) != "-1":
            if self.role =="" or self.role == "NONE" or str(self.role).lower() == "all":
                park_content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><conference-info entity=\"%s\"  state=\"full\"  s=\"0000101011\"  options=\"10\"  maxusercount=\"100\"  usercount=\"12\"  maxmic=\"10\"  active=\"1\"  creater=\"%s\"  host=\"%s\"  presenter=\"%s\"  mic_count=\"10\"  now_time=\"20150411040704\"  start_time=\"20150411033138\"  time=\"20150411033138_20150411040704\"><users><user entity=\"8210\"  state=\"full\"  display=\"pythonuser (8210)\" ua=\"ios\"  type=\"4\"  s=\"0111\"  options=\"10\"/><user entity=\"8211\"  state=\"full\"  display=\"pyuser (8211)\" ua=\"grandstream gxv\"  type=\"7\"  s=\"1110\"  options=\"10\"/><user entity=\"8212\"  state=\"full\"  display=\"py2 (8212)\" ua=\"grandstream gxp\"  type=\"8\"  s=\"1110\"  options=\"10\"/><user entity=\"8213\"  state=\"full\"  display=\"py 3 (8213)\" ua=\"other\"  type=\"0\"  s=\"1111\"  options=\"10\"/><user entity=\"8214\"  state=\"full\"  display=\"py4 (8214)\" ua=\"windows\"  type=\"1\"  s=\"1110\"  options=\"10\"/><user entity=\"8215\"  state=\"full\"  display=\"py 5 (8215)\" ua=\"mac\"  type=\"2\"  s=\"1110\"  options=\"10\"/><user entity=\"8216\"  state=\"full\"  display=\"py 6 (8216)\" ua=\"android\"  type=\"3\"  s=\"1111\"  options=\"10\"/><user entity=\"8217\"  state=\"full\"  display=\"py 7 (8217)\" ua=\"websocket\"  type=\"5\"  s=\"1110\"  options=\"10\"/><user entity=\"8218\"  state=\"full\"  display=\"py 8 (8218)\" ua=\"pstn\"  type=\"6\"  s=\"0100\"  options=\"10\"/><user entity=\"10016\"  state=\"full\"  display=\"mytest\"  ua=\"windows\"  type=\"1\"  s=\"0011\"  options=\"11\"/><user entity=\"%s\"  state=\"full\"  display=\"last(10017)\" ua=\"windows\"  type=\"1\"  s=\"1111\"  options=\"10\"/><user entity=\"%s\"  state=\"full\"  display=\"A a5\"  ua=\"windows\"  type=\"1\"  s=\"0011\"  options=\"11\"/></users></conference-info>"%(str(msg_info.meeting_id_to_user),str(msg_info.sipid_number),str(msg_info.sipid_number),str(msg_info.sipid_number),str(int(msg_info.sipid_number)+1),str(msg_info.sipid_number))
#                 park_content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><conference-info entity=\"%s\"  state=\"full\"  s=\"0000101001\"  options=\"10\"  maxusercount=\"100\"  usercount=\"12\"  maxmic=\"10\"  active=\"1\"  creater=\"%s\"  host=\"%s\"  presenter=\"%s\"  mic_count=\"10\"  now_time=\"20150411040704\"  start_time=\"20150411033138\"  time=\"20150411033138_20150411040704\"><users><user entity=\"8210\"  state=\"full\"  display=\"pythonuser (8210)\" ua=\"ios\"  type=\"4\"  s=\"0110\"  options=\"10\"/><user entity=\"%s\"  state=\"full\"  display=\"pyuser (8211)\" ua=\"grandstream gxv\"  type=\"7\"  s=\"1110\"  options=\"10\"/><user entity=\"8212\"  state=\"full\"  display=\"py2 (8212)\" ua=\"grandstream gxp\"  type=\"8\"  s=\"1110\"  options=\"10\"/><user entity=\"8213\"  state=\"full\"  display=\"py 3 (8213)\" ua=\"other\"  type=\"0\"  s=\"1110\"  options=\"10\"/><user entity=\"8214\"  state=\"full\"  display=\"py4 (8214)\" ua=\"windows\"  type=\"1\"  s=\"1110\"  options=\"10\"/><user entity=\"8215\"  state=\"full\"  display=\"py 5 (8215)\" ua=\"mac\"  type=\"2\"  s=\"1110\"  options=\"10\"/><user entity=\"8216\"  state=\"full\"  display=\"py 6 (8216)\" ua=\"android\"  type=\"3\"  s=\"1110\"  options=\"10\"/><user entity=\"8217\"  state=\"full\"  display=\"py 7 (8217)\" ua=\"websocket\"  type=\"5\"  s=\"1110\"  options=\"10\"/><user entity=\"8218\"  state=\"full\"  display=\"py 8 (8218)\" ua=\"pstn\"  type=\"6\"  s=\"0100\"  options=\"10\"/><user entity=\"10016\"  state=\"full\"  display=\"mytest\"  ua=\"windows\"  type=\"1\"  s=\"0011\"  options=\"11\"/><user entity=\"10017\"  state=\"full\"  display=\"last(10017)\" ua=\"windows\"  type=\"1\"  s=\"1100\"  options=\"10\"/><user entity=\"10018\"  state=\"full\"  display=\"A a5\"  ua=\"windows\"  type=\"1\"  s=\"0010\"  options=\"11\"/></users></conference-info>"%(str(msg_info.meeting_id_to_user),str(msg_info.sipid_number),str(msg_info.sipid_number),str(msg_info.sipid_number),str(msg_info.sipid_number))
            elif str(self.role).lower() == "host":
                park_content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><conference-info entity=\"%s\"  state=\"full\"  s=\"0000101011\"  options=\"10\"  maxusercount=\"100\"  usercount=\"12\"  maxmic=\"10\"  active=\"1\"  creater=\"%s\"  host=\"%s\"  presenter=\"%s\"  mic_count=\"10\"  now_time=\"20150411040704\"  start_time=\"20150411033138\"  time=\"20150411033138_20150411040704\"><users><user entity=\"8210\"  state=\"full\"  display=\"pythonuser (8210)\" ua=\"ios\"  type=\"4\"  s=\"0111\"  options=\"10\"/><user entity=\"8211\"  state=\"full\"  display=\"pyuser (8211)\" ua=\"grandstream gxv\"  type=\"7\"  s=\"1110\"  options=\"10\"/><user entity=\"8212\"  state=\"full\"  display=\"py2 (8212)\" ua=\"grandstream gxp\"  type=\"8\"  s=\"1110\"  options=\"10\"/><user entity=\"8213\"  state=\"full\"  display=\"py 3 (8213)\" ua=\"other\"  type=\"0\"  s=\"1111\"  options=\"10\"/><user entity=\"8214\"  state=\"full\"  display=\"py4 (8214)\" ua=\"windows\"  type=\"1\"  s=\"1110\"  options=\"10\"/><user entity=\"8215\"  state=\"full\"  display=\"py 5 (8215)\" ua=\"mac\"  type=\"2\"  s=\"1110\"  options=\"10\"/><user entity=\"8216\"  state=\"full\"  display=\"py 6 (8216)\" ua=\"android\"  type=\"3\"  s=\"1111\"  options=\"10\"/><user entity=\"8217\"  state=\"full\"  display=\"py 7 (8217)\" ua=\"websocket\"  type=\"5\"  s=\"1110\"  options=\"10\"/><user entity=\"8218\"  state=\"full\"  display=\"py 8 (8218)\" ua=\"pstn\"  type=\"6\"  s=\"0100\"  options=\"10\"/><user entity=\"10016\"  state=\"full\"  display=\"mytest\"  ua=\"windows\"  type=\"1\"  s=\"0011\"  options=\"11\"/><user entity=\"%s\"  state=\"full\"  display=\"last(10017)\" ua=\"windows\"  type=\"1\"  s=\"1111\"  options=\"10\"/><user entity=\"%s\"  state=\"full\"  display=\"A a5\"  ua=\"windows\"  type=\"1\"  s=\"0011\"  options=\"11\"/></users></conference-info>"%(str(msg_info.meeting_id_to_user),str(int(msg_info.sipid_number)+1),str(msg_info.sipid_number),str(int(msg_info.sipid_number)+1),str(int(msg_info.sipid_number)+1),str(msg_info.sipid_number))
                
            elif str(self.role).lower() == "creater":
                park_content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><conference-info entity=\"%s\"  state=\"full\"  s=\"0000101011\"  options=\"10\"  maxusercount=\"100\"  usercount=\"12\"  maxmic=\"10\"  active=\"1\"  creater=\"%s\"  host=\"%s\"  presenter=\"%s\"  mic_count=\"10\"  now_time=\"20150411040704\"  start_time=\"20150411033138\"  time=\"20150411033138_20150411040704\"><users><user entity=\"8210\"  state=\"full\"  display=\"pythonuser (8210)\" ua=\"ios\"  type=\"4\"  s=\"0111\"  options=\"10\"/><user entity=\"8211\"  state=\"full\"  display=\"pyuser (8211)\" ua=\"grandstream gxv\"  type=\"7\"  s=\"1110\"  options=\"10\"/><user entity=\"8212\"  state=\"full\"  display=\"py2 (8212)\" ua=\"grandstream gxp\"  type=\"8\"  s=\"1110\"  options=\"10\"/><user entity=\"8213\"  state=\"full\"  display=\"py 3 (8213)\" ua=\"other\"  type=\"0\"  s=\"1111\"  options=\"10\"/><user entity=\"8214\"  state=\"full\"  display=\"py4 (8214)\" ua=\"windows\"  type=\"1\"  s=\"1110\"  options=\"10\"/><user entity=\"8215\"  state=\"full\"  display=\"py 5 (8215)\" ua=\"mac\"  type=\"2\"  s=\"1110\"  options=\"10\"/><user entity=\"8216\"  state=\"full\"  display=\"py 6 (8216)\" ua=\"android\"  type=\"3\"  s=\"1111\"  options=\"10\"/><user entity=\"8217\"  state=\"full\"  display=\"py 7 (8217)\" ua=\"websocket\"  type=\"5\"  s=\"1110\"  options=\"10\"/><user entity=\"8218\"  state=\"full\"  display=\"py 8 (8218)\" ua=\"pstn\"  type=\"6\"  s=\"0100\"  options=\"10\"/><user entity=\"10016\"  state=\"full\"  display=\"mytest\"  ua=\"windows\"  type=\"1\"  s=\"0011\"  options=\"11\"/><user entity=\"%s\"  state=\"full\"  display=\"last(10017)\" ua=\"windows\"  type=\"1\"  s=\"1111\"  options=\"10\"/><user entity=\"%s\"  state=\"full\"  display=\"A a5\"  ua=\"windows\"  type=\"1\"  s=\"0011\"  options=\"11\"/></users></conference-info>"%(str(msg_info.meeting_id_to_user),str(msg_info.sipid_number),str(int(msg_info.sipid_number)+1),str(int(msg_info.sipid_number)+1),str(int(msg_info.sipid_number)+1),str(msg_info.sipid_number))
            elif str(self.role).lower() == "presenter":
                park_content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><conference-info entity=\"%s\"  state=\"full\"  s=\"0000101011\"  options=\"10\"  maxusercount=\"100\"  usercount=\"12\"  maxmic=\"10\"  active=\"1\"  creater=\"%s\"  host=\"%s\"  presenter=\"%s\"  mic_count=\"10\"  now_time=\"20150411040704\"  start_time=\"20150411033138\"  time=\"20150411033138_20150411040704\"><users><user entity=\"8210\"  state=\"full\"  display=\"pythonuser (8210)\" ua=\"ios\"  type=\"4\"  s=\"0111\"  options=\"10\"/><user entity=\"8211\"  state=\"full\"  display=\"pyuser (8211)\" ua=\"grandstream gxv\"  type=\"7\"  s=\"1110\"  options=\"10\"/><user entity=\"8212\"  state=\"full\"  display=\"py2 (8212)\" ua=\"grandstream gxp\"  type=\"8\"  s=\"1110\"  options=\"10\"/><user entity=\"8213\"  state=\"full\"  display=\"py 3 (8213)\" ua=\"other\"  type=\"0\"  s=\"1111\"  options=\"10\"/><user entity=\"8214\"  state=\"full\"  display=\"py4 (8214)\" ua=\"windows\"  type=\"1\"  s=\"1110\"  options=\"10\"/><user entity=\"8215\"  state=\"full\"  display=\"py 5 (8215)\" ua=\"mac\"  type=\"2\"  s=\"1110\"  options=\"10\"/><user entity=\"8216\"  state=\"full\"  display=\"py 6 (8216)\" ua=\"android\"  type=\"3\"  s=\"1111\"  options=\"10\"/><user entity=\"8217\"  state=\"full\"  display=\"py 7 (8217)\" ua=\"websocket\"  type=\"5\"  s=\"1110\"  options=\"10\"/><user entity=\"8218\"  state=\"full\"  display=\"py 8 (8218)\" ua=\"pstn\"  type=\"6\"  s=\"0100\"  options=\"10\"/><user entity=\"10016\"  state=\"full\"  display=\"mytest\"  ua=\"windows\"  type=\"1\"  s=\"0011\"  options=\"11\"/><user entity=\"%s\"  state=\"full\"  display=\"last(10017)\" ua=\"windows\"  type=\"1\"  s=\"1111\"  options=\"10\"/><user entity=\"%s\"  state=\"full\"  display=\"A a5\"  ua=\"windows\"  type=\"1\"  s=\"0011\"  options=\"11\"/></users></conference-info>"%(str(msg_info.meeting_id_to_user),str(int(msg_info.sipid_number)+1),str(int(msg_info.sipid_number)+1),str(msg_info.sipid_number),str(int(msg_info.sipid_number)+1),str(msg_info.sipid_number))
            else:
                park_content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><conference-info entity=\"%s\"  state=\"full\"  s=\"0000101011\"  options=\"10\"  maxusercount=\"100\"  usercount=\"12\"  maxmic=\"10\"  active=\"1\"  creater=\"%s\"  host=\"%s\"  presenter=\"%s\"  mic_count=\"10\"  now_time=\"20150411040704\"  start_time=\"20150411033138\"  time=\"20150411033138_20150411040704\"><users><user entity=\"8210\"  state=\"full\"  display=\"pythonuser (8210)\" ua=\"ios\"  type=\"4\"  s=\"0111\"  options=\"10\"/><user entity=\"8211\"  state=\"full\"  display=\"pyuser (8211)\" ua=\"grandstream gxv\"  type=\"7\"  s=\"1110\"  options=\"10\"/><user entity=\"8212\"  state=\"full\"  display=\"py2 (8212)\" ua=\"grandstream gxp\"  type=\"8\"  s=\"1110\"  options=\"10\"/><user entity=\"8213\"  state=\"full\"  display=\"py 3 (8213)\" ua=\"other\"  type=\"0\"  s=\"1111\"  options=\"10\"/><user entity=\"8214\"  state=\"full\"  display=\"py4 (8214)\" ua=\"windows\"  type=\"1\"  s=\"1110\"  options=\"10\"/><user entity=\"8215\"  state=\"full\"  display=\"py 5 (8215)\" ua=\"mac\"  type=\"2\"  s=\"1110\"  options=\"10\"/><user entity=\"8216\"  state=\"full\"  display=\"py 6 (8216)\" ua=\"android\"  type=\"3\"  s=\"1111\"  options=\"10\"/><user entity=\"8217\"  state=\"full\"  display=\"py 7 (8217)\" ua=\"websocket\"  type=\"5\"  s=\"1110\"  options=\"10\"/><user entity=\"8218\"  state=\"full\"  display=\"py 8 (8218)\" ua=\"pstn\"  type=\"6\"  s=\"0100\"  options=\"10\"/><user entity=\"10016\"  state=\"full\"  display=\"mytest\"  ua=\"windows\"  type=\"1\"  s=\"0011\"  options=\"11\"/><user entity=\"%s\"  state=\"full\"  display=\"last(10017)\" ua=\"windows\"  type=\"1\"  s=\"1111\"  options=\"10\"/><user entity=\"%s\"  state=\"full\"  display=\"A a5\"  ua=\"windows\"  type=\"1\"  s=\"0011\"  options=\"11\"/></users></conference-info>"%(str(msg_info.meeting_id_to_user),str(int(msg_info.sipid_number)+1),str(int(msg_info.sipid_number)+1),str(int(msg_info.sipid_number)+1),str(int(msg_info.sipid_number)+1),str(msg_info.sipid_number))
                
        elif flag == 2:
            park_content = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\r\n<conference-info refresh=\"%s\" entity=\"%s\" state=\"partial\" s=\"0001100111\" share_type=\"0\"/>" %(self.refreshTime,str(msg_info.meeting_id_to_user))
            self.refreshTime += 1
        elif flag == 3:
            park_content = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\r\n<conference-info refresh=\"%s\" entity=\"%s\" state=\"partial\" s=\"1100100111\" share_type=\"0\"/>" %(self.refreshTime,str(msg_info.meeting_id_to_user))
            self.refreshTime += 1
        else:
            park_content = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\r\n<conference-info refresh=\"%s\" entity=\"%s\" state=\"partial\"><users><user entity=\"%s\" state=\"partial\" s=\"0011\"/></users></conference-info>" %(self.refreshTime,msg_info.meeting_id_to_user,str(msg_info.sipid_number))
            self.refreshTime += 1
        notify_request = "NOTIFY sip:%s@%s:%d SIP/2.0"%(msg_info.meeting_id_to_user,msg_info.dest_ip_number,msg_info.dest_port_number) + "\r\n"
        notify_request += "Via: SIP/2.0/TCP %s:%d;branch=z9hG4bK1e3effada91dc37fd5a0c95cbf6767d2%d"%(msg_info.local_ip_number, msg_info.local_port_number, msg_info.cseq_num) + "\r\n"
        notify_request += "Via: SIP/2.0/UDP %s:%d;received=%s;branch=z9hG4bK1e3effada91dc37fd5a0c95cbf6767d2%d;rport=17247"%(msg_info.local_ip_number, int(msg_info.rtp_media_port), msg_info.local_ip_number,int(msg_info.cseq_num)) + "\r\n"
        notify_request += "To: <sip:%s@%s:%s>\r\n"%(msg_info.meeting_id_to_user,msg_info.local_ip_number,msg_info.local_port_number)
        if msg_info.hastotag == True:
            notify_request += "From: %s\r\n"%msg_info.to_header
        else:
            notify_request += "From: %s;tag=201203271\r\n"%msg_info.to_header
        notify_request += "Call-ID: %s\r\n"%msg_info.call_id
        notify_request += "Contact: <sip: " + msg_info.local_ip_number + ":" + "%d"%msg_info.local_port_number + ";transport=tcp>\r\n"
#         notify_request += "Event: call-info\r\n"
        notify_request += "Max-Forwards: 69\r\n"
        notify_request += "User-Agent: conference\r\n" 
        notify_request += "Event: X-GS-CONFERENCE\r\n"
        notify_request += "X-GS-Notify-Users: all\r\n"
        notify_request += "X-GS-SERVER-ID: %s\r\n" %  msg_info.local_ip_number
#         notify_request += "Call-Info: "
#         notify_request += "<sip:%s>;appearance-state=idle;appearance-index=*\r\n"%msg_info.local_ip_number
        notify_request += "Content-Type: application/conference-info+xml\r\n"
        notify_request += "CSeq: %d NOTIFY\r\n" % (msg_info.cseq_num)
        notify_request += "Content-Length: %d\r\n\r\n" % (len(park_content))
        notify_request += park_content
        debug_print( "from[%s:%d] to[%s:%d]\r\n"%(msg_info.local_ip_number, msg_info.local_port_number, msg_info.dest_ip_number, msg_info.dest_port_number), VERBOSE)
        debug_print( "%s\r\n"%notify_request, VERBOSE)
        if msg_info.protocol == 'udp':
            sock.sendto(notify_request, (msg_info.dest_ip_number, msg_info.dest_port_number))
        else:
            try:
                sock.sendall(notify_request)
            except Exception as e:
                addCaseLog("send Notify failed,socket connect failed: %s(send_Nofity)") % (str(e))
                self.OnError()
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1
        
        return True
    def OnError(self):
        global service_on
        service_on = 0
        addCaseLog("sipServer_commonlib.OnError, case failed")
        setCaseResult("failed")
        if self.localsock:
            self.localsock.close()
        sys.exit()

    def send_av_invite(self,sock,msg_info):
        if msg_info.rtp_media_port == "":
            msg_info.rtp_media_port = self.rtp_port
        if msg_info.user_agent == "":
            msg_info.user_agent = 'windows'
        if msg_info.display_name == "":
            msg_info.display_name = self.display_name
        if msg_info.meeting_id_to_user == "":
            addCaseLog("meeting number is empty (send_invite)")
            self.OnError()
        # send INVITE request to sip server
        if sock =="":
            sock = self.localsock
        if msg_info.cseq_num == "":
            msg_info.cseq_num = XSERVER_PUBLICKEY["cseq_num_all"]
#         sdp_content = "v=0\r\no=root 865661064 865661064 IN IP4 %s\r\ns=SIP Call\r\nc=IN IP4 %s\r\nt=0 0\r\nm=audio %d RTP/AVP 0 101\r\na=sendrecv\r\na=rtpmap:0 PCMU/8000\r\na=ptime:20\r\na=rtpmap:101 telephone-event/8000\r\na=fmtp:101 0-15"%(msg_info.local_ip_number, msg_info.local_ip_number, msg_info.rtp_media_port)
#         sdp_content += "\r\na=maxptime:150\r\na=sendrecv\r\nm=video 29116 RTP/AVP 31 34 98 99 104 100\r\na=rtpmap:31 H261/90000\r\na=rtpmap:34 H263/90000\r\na=rtpmap:98 h263-1998/90000\r\na=rtpmap:99 H264/90000\r\na=rtpmap:104 MP4V-ES/90000\r\na=rtpmap:100 VP8/90000\r\na=rtcp-fb:* ccm fir\r\na=sendrecv"
        sdp_content = "v=0\r\no=root 865661064 865661065 IN IP4 %s\r\ns=GrandStream X-Server 0.0.0.24\r\nc=IN IP4 %s\r\nb=CT:384\r\nt=0 0\r\nm=audio 56970 RTP/AVP 0 8 101\r\na=rtpmap:0 PCMU/8000\r\na=rtpmap:8 PCMA/8000\r\na=rtpmap:101 telephone-event/8000\r\na=fmtp:101 0-16\r\na=maxptime:150\r\na=sendrecv\r\nm=video 39884 RTP/AVP 31 34 98 99 104 100\r\na=rtpmap:31 H261/90000\r\na=rtpmap:34 H263/90000\r\na=rtpmap:98 h263-1998/90000\r\na=rtpmap:99 H264/90000\r\na=rtpmap:104 MP4V-ES/90000\r\na=rtpmap:100 VP8/90000\r\na=rtcp-fb:* ccm fir\r\na=sendrecv\r\n" %(msg_info.local_ip_number,msg_info.local_ip_number)
        if msg_info.meeting_pw == "NONE" or msg_info.meeting_pw == "":
            invite_request = "INVITE sip:%s@%s SIP/2.0\r\n"%(msg_info.meeting_id_to_user, msg_info.local_ip_number)
        else:
            invite_request = "INVITE sip:%s*%s@%s SIP/2.0\r\n"%(msg_info.meeting_id_to_user, msg_info.meeting_pw, msg_info.local_ip_number)
        if msg_info.protocol == 'udp':
            invite_request += "Via: SIP/2.0/UDP %s:%d;branch=z9hG4bK12345678%x;rport;alias"%(msg_info.local_ip_number,msg_info.local_port_number, random.randint(0, 10000)) + "\r\n"
            invite_request += "Contact: <sip:" + msg_info.sipid_number + "@" + msg_info.local_ip_number + ":" + "%d"%msg_info.local_port_number + ";transport=udp>\r\n"
        else:
            invite_request += "Via: SIP/2.0/TCP %s:%d;branch=z9hG4bK12345678%x"%(msg_info.local_ip_number,msg_info.local_port_number, random.randint(0, 10000)) + "\r\n"
            invite_request += "Via: SIP/2.0/UDP %s:5062;received=%s;branch=z9hG4bK12345678%x;rport=5062"%(msg_info.local_ip_number,msg_info.local_ip_number, random.randint(0, 10000)) + "\r\n"
            invite_request += "Contact:  \"%s (%s)\" <sip:"%(str(msg_info.display_name),str(msg_info.sipid_number)) + str(msg_info.sipid_number) + "@" + str(msg_info.local_ip_number) + ":" + "%d"%msg_info.local_port_number + ";transport=tcp>\r\n"
        print "msg_info.totag  %s" % msg_info.totag
        if msg_info.hastotag == True:
            if msg_info.meeting_pw == "NONE" or msg_info.meeting_pw == "":
                invite_request += "To: <sip:%s@%s:%d>;tag=%s\r\n"%(msg_info.meeting_id_to_user, msg_info.local_ip_number, msg_info.local_port_number, self.av_invite_totag)
            else:
                invite_request += "To: <sip:%s*%s@%s:%d>;tag=%s\r\n"%(msg_info.meeting_id_to_user, msg_info.meeting_pw, msg_info.local_ip_number, msg_info.local_port_number, self.av_invite_totag)
    
        else:
            if msg_info.meeting_pw == "NONE" or msg_info.meeting_pw == "":
                invite_request += "To: <sip:%s@%s>;tag=%s\r\n"%(msg_info.meeting_id_to_user, msg_info.local_ip_number,self.av_invite_totag)
            else:
                invite_request += "To: <sip:%s*%s@%s>;tag=%s\r\n"%(msg_info.meeting_id_to_user, msg_info.meeting_pw, msg_info.local_ip_number,self.av_invite_totag)
    
        invite_request += "From: \"%s (%s)\" <sip:%s@%s>;tag=%s\r\n"%(msg_info.display_name,msg_info.sipid_number, msg_info.sipid_number, msg_info.local_ip_number, "201203271")
#         invite_request += "From: %s\r\n" % self.av_invite_fromtag
        if self.compare_string(msg_info.authorization_header, 'NONE') != 0:
            invite_request += "Authorization: %s\r\n"%msg_info.authorization_header;
        elif self.compare_string(msg_info.proxy_authorization_header, 'NONE') != 0:
            invite_request += "Proxy-Authorization: %s\r\n"%msg_info.proxy_authorization_header;
        
        invite_request += "Call-ID: %s\r\n"%self.call_id
        invite_request += "CSeq: %d INVITE\r\n" % msg_info.cseq_num
        invite_request += "Max-Forwards: 69\r\n"
        invite_request += "Session-Expires: 600;refresher=uas\r\n"
        invite_request += "X-Info: SIP re-invite (External RTP bridge)\r\n"
        
        invite_request += "User-Agent: %s\r\n"%(msg_info.user_agent)
        invite_request += "Privacy: none\r\n"
        invite_request += "P-Preferred-Identity: \"%s\" <sip:"%(str(msg_info.display_name)) + str(msg_info.sipid_number) + "@" + str(msg_info.dest_ip_number) + ">\r\n"
        invite_request += "Supported: replaces, path, timer, eventlist\r\n"
        invite_request += "Allow: INVITE, ACK, OPTIONS, CANCEL, BYE, SUBSCRIBE, NOTIFY, INFO, REFER, UPDATE, MESSAGE\r\n"
        invite_request += "Content-Type: application/sdp\r\n"
        invite_request += "Accept: application/sdp, application/dtmf-relay\r\n"
        invite_request += "X-GS-SERVER-ID: %s \r\n"%(msg_info.local_ip_number)
        invite_request += "Content-Length: %d\r\n\r\n"%(len(sdp_content))

        
        invite_request += sdp_content
    
        if msg_info.protocol == 'udp':
            sock.sendto(invite_request, (msg_info.dest_ip_number, msg_info.dest_port_number))
        else:
            try:
                sock.sendall(invite_request)
            except Exception as e:
                addCaseLog("send request %s  failed,socket connect failed: %s(send_INVITE)") % (msg_info.call_id,str(e))
                self.OnError()
            
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1

    def send_av_stop_invite(self,sock,msg_info):
        if msg_info.rtp_media_port == "":
            msg_info.rtp_media_port = self.rtp_port
        if msg_info.user_agent == "":
            msg_info.user_agent = 'windows'
        if msg_info.display_name == "":
            msg_info.display_name = self.display_name
        if msg_info.meeting_id_to_user == "":
            addCaseLog("meeting number is empty (send_invite)")
            self.OnError()
        # send INVITE request to sip server
        if sock =="":
            sock = self.localsock
        if msg_info.cseq_num == "":
            msg_info.cseq_num = XSERVER_PUBLICKEY["cseq_num_all"]
#         sdp_content = "v=0\r\no=root 865661064 865661064 IN IP4 %s\r\ns=SIP Call\r\nc=IN IP4 %s\r\nt=0 0\r\nm=audio %d RTP/AVP 0 101\r\na=sendrecv\r\na=rtpmap:0 PCMU/8000\r\na=ptime:20\r\na=rtpmap:101 telephone-event/8000\r\na=fmtp:101 0-15"%(msg_info.local_ip_number, msg_info.local_ip_number, msg_info.rtp_media_port)
#         sdp_content += "\r\na=maxptime:150\r\na=sendrecv\r\nm=video 29116 RTP/AVP 31 34 98 99 104 100\r\na=rtpmap:31 H261/90000\r\na=rtpmap:34 H263/90000\r\na=rtpmap:98 h263-1998/90000\r\na=rtpmap:99 H264/90000\r\na=rtpmap:104 MP4V-ES/90000\r\na=rtpmap:100 VP8/90000\r\na=rtcp-fb:* ccm fir\r\na=sendrecv"
        sdp_content = "v=0\r\no=root 865661064 865661065 IN IP4 %s\r\ns=GrandStream X-Server 0.0.0.24\r\nc=IN IP4 %s\r\nb=CT:384\r\nt=0 0\r\nm=audio 56970 RTP/AVP 0 8 101\r\na=rtpmap:0 PCMU/8000\r\na=rtpmap:8 PCMA/8000\r\na=rtpmap:101 telephone-event/8000\r\na=fmtp:101 0-16\r\na=maxptime:150\r\na=sendrecv\r\n" %(msg_info.local_ip_number,msg_info.local_ip_number)
        if msg_info.meeting_pw == "NONE" or msg_info.meeting_pw == "":
            invite_request = "INVITE sip:%s@%s SIP/2.0\r\n"%(msg_info.meeting_id_to_user, msg_info.local_ip_number)
        else:
            invite_request = "INVITE sip:%s*%s@%s SIP/2.0\r\n"%(msg_info.meeting_id_to_user, msg_info.meeting_pw, msg_info.local_ip_number)
        if msg_info.protocol == 'udp':
            invite_request += "Via: SIP/2.0/UDP %s:%d;branch=z9hG4bK12345678%x;rport;alias"%(msg_info.local_ip_number,msg_info.local_port_number, random.randint(0, 10000)) + "\r\n"
            invite_request += "Contact: <sip:" + msg_info.sipid_number + "@" + msg_info.local_ip_number + ":" + "%d"%msg_info.local_port_number + ";transport=udp>\r\n"
        else:
            invite_request += "Via: SIP/2.0/TCP %s:%d;branch=z9hG4bK12345678%x"%(msg_info.local_ip_number,msg_info.local_port_number, random.randint(0, 10000)) + "\r\n"
            invite_request += "Via: SIP/2.0/UDP %s:5062;received=%s;branch=z9hG4bK12345678%x;rport=5062"%(msg_info.local_ip_number,msg_info.local_ip_number, random.randint(0, 10000)) + "\r\n"
            invite_request += "Contact:  \"%s (%s)\" <sip:"%(str(msg_info.display_name),str(msg_info.sipid_number)) + str(msg_info.sipid_number) + "@" + str(msg_info.local_ip_number) + ":" + "%d"%msg_info.local_port_number + ";transport=tcp>\r\n"
        print "msg_info.totag  %s" % msg_info.totag
        if msg_info.hastotag == True:
            if msg_info.meeting_pw == "NONE" or msg_info.meeting_pw == "":
                invite_request += "To: <sip:%s@%s:%d>;tag=%s\r\n"%(msg_info.meeting_id_to_user, msg_info.local_ip_number, msg_info.local_port_number, self.av_invite_totag)
            else:
                invite_request += "To: <sip:%s*%s@%s:%d>;tag=%s\r\n"%(msg_info.meeting_id_to_user, msg_info.meeting_pw, msg_info.local_ip_number, msg_info.local_port_number, self.av_invite_totag)
    
        else:
            if msg_info.meeting_pw == "NONE" or msg_info.meeting_pw == "":
                invite_request += "To: <sip:%s@%s>;tag=%s\r\n"%(msg_info.meeting_id_to_user, msg_info.local_ip_number,self.av_invite_totag)
            else:
                invite_request += "To: <sip:%s*%s@%s>;tag=%s\r\n"%(msg_info.meeting_id_to_user, msg_info.meeting_pw, msg_info.local_ip_number,self.av_invite_totag)
    
        invite_request += "From: \"%s (%s)\" <sip:%s@%s>;tag=%s\r\n"%(msg_info.display_name,msg_info.sipid_number, msg_info.sipid_number, msg_info.local_ip_number, "201203271")
#         invite_request += "From: %s\r\n" % self.av_invite_fromtag
        if self.compare_string(msg_info.authorization_header, 'NONE') != 0:
            invite_request += "Authorization: %s\r\n"%msg_info.authorization_header;
        elif self.compare_string(msg_info.proxy_authorization_header, 'NONE') != 0:
            invite_request += "Proxy-Authorization: %s\r\n"%msg_info.proxy_authorization_header;
        
        invite_request += "Call-ID: %s\r\n"%self.call_id
        invite_request += "CSeq: %d INVITE\r\n" % msg_info.cseq_num
        invite_request += "Max-Forwards: 69\r\n"
        invite_request += "Session-Expires: 600;refresher=uas\r\n"
        invite_request += "X-Info: SIP re-invite (External RTP bridge)\r\n"
        
        invite_request += "User-Agent: %s\r\n"%(msg_info.user_agent)
        invite_request += "Privacy: none\r\n"
        invite_request += "P-Preferred-Identity: \"%s\" <sip:"%(str(msg_info.display_name)) + str(msg_info.sipid_number) + "@" + str(msg_info.dest_ip_number) + ">\r\n"
        invite_request += "Supported: replaces, path, timer, eventlist\r\n"
        invite_request += "Allow: INVITE, ACK, OPTIONS, CANCEL, BYE, SUBSCRIBE, NOTIFY, INFO, REFER, UPDATE, MESSAGE\r\n"
        invite_request += "Content-Type: application/sdp\r\n"
        invite_request += "Accept: application/sdp, application/dtmf-relay\r\n"
        invite_request += "X-GS-SERVER-ID: %s \r\n"%(msg_info.local_ip_number)
        invite_request += "Content-Length: %d\r\n\r\n"%(len(sdp_content))

        
        invite_request += sdp_content
    
        if msg_info.protocol == 'udp':
            sock.sendto(invite_request, (msg_info.dest_ip_number, msg_info.dest_port_number))
        else:
            try:
                sock.sendall(invite_request)
            except Exception as e:
                addCaseLog("send request %s  failed,socket connect failed: %s(send_INVITE)") % (msg_info.call_id,str(e))
                self.OnError()
            
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1

    def parseReceivedData( self, data, sipMethod):
        
        global LOOPTIMES_Xserver_errorCode
        global LOCAL_PC_PORT,LOCAL_PC_IP
        if data == "":
            return "NONE"
        service_msg = self.parse(data)
        if service_msg == None:
            return
        service_msg.local_ip_number = self.localip
        service_msg.local_port_number = self.localport
        service_msg.dest_ip_number = self.dest_address
        service_msg.dest_port_number = self.dest_port
        if service_msg.msg_isReq:
            addCaseLog("%s request::%s %d %s request is received for %s, to_user = %s (parseReceivedData)" % (service_msg.sipid_number,service_msg.msg_method, service_msg.statusCode, service_msg.statusPhase, service_msg.sipid_number, service_msg.meeting_id_to_user))
            #send_Nofity flag = 1(join meeting notify), flag = 2(start recording),flag=3(stop recording)
            if str(service_msg.msg_method).lower() == sipMethod:
                addCaseLog("###### WoW, received tested API request, start set error coding#####")
                if LOOPTIMES_Xserver_errorCode <= len(self.errorCode_system):
                    self.infoReceivedTime = self.infoReceivedTime + 1
                    if self.testnum > self.infoReceivedTime:
                        addCaseLog("Test Time=%s > receivedTime=%s, will give you correct result first" % (self.testnum,self.infoReceivedTime))
                        if str(service_msg.msg_method).lower() == "info":
                            addCaseLog("Received INFO request, send 200 OK to the girl (parseReceivedData)")
                            self.handle_Unknown_request(self.localsock,None, service_msg)
                            if str(str(service_msg.x_gs_conf_control).find("ctrl_present")) != "-1":
                                addCaseLog("Received INFO request, send 200OK to the girl (parseReceivedData)" )
                                self.handle_Unknown_request(self.localsock,None, service_msg)
                                if str(str(service_msg.x_gs_conf_control).find("present-status=1")) != "-1":
                                    addCaseLog("Received INFO(start ds) request, send reinvite for av to the girl (parseReceivedData)" )
                                    self.send_av_invite(self.localsock,service_msg)
                                    addCaseLog("Received INFO(start ds) request, send  NOTIFY(start ds) to the girl (parseReceivedData)" )
                                    self.send_Nofity(self.localsock,service_msg,2)
                                else:
                                    addCaseLog("Received INFO(stop ds) request, send reinvite for av to the girl (parseReceivedData)" )
                                    self.send_av_stop_invite(self.localsock,service_msg)
                                    addCaseLog("Received INFO(stop ds) request, send NOTIFY(stop ds) to the girl (parseReceivedData)" )
                                    self.send_Nofity(self.localsock,service_msg,3)
                            elif str(str(service_msg.x_gs_conf_control).find("get_all_users")) != "-1":
                                addCaseLog("Received INFO(get all user) request, send NOTIFY(full) to the girl (parseReceivedData)" )
                                self.send_Nofity(self.localsock,service_msg,0)
                            else:
                                addCaseLog("Send NOTIFY  to the girl (parseReceivedData)")
                                self.send_Nofity(self.localsock,service_msg)
                        elif str(service_msg.msg_method).lower() == "invite":
                            if service_msg.totag == True:
                                self.infoReceivedTime = 0
                            addCaseLog("%s Received INVITE request(%s %d %s), send 200 OK to the girl (parseReceivedData)" % (service_msg.sipid_number,service_msg.msg_method, service_msg.statusCode, service_msg.statusPhase))
                            self.send_INVITE_response_confroom(self.localsock, service_msg)
                            addCaseLog("You are join invite,now Send join meeting NOTIFY  to the girl (parseReceivedData)")
                            self.send_Nofity(self.localsock,service_msg,1)
                            self.av_invite_totag = service_msg.fromtag
                            self.call_id = service_msg.call_id
                            print "self.av_invite_fromtag   %s" % self.av_invite_totag                            
                        else:
                            self.handle_Unknown_request(self.localsock,None, service_msg)
                    else:
                        keyValue = str(LOOPTIMES_Xserver_errorCode)
                        addCaseLog( "[1] Start ServerCommon exception test, total test time = %s,retCode = %s,sip status code = %s" % (LOOPTIMES_Xserver_errorCode,self.errorCode_system[keyValue],"404 not found"))
                        addCaseLog("%s Received request(%s %d %s), send 200 OK to the girl (parseReceivedData)" % (service_msg.sipid_number,service_msg.msg_method, service_msg.statusCode, service_msg.statusPhase))
                        self.sendErrorRespond(self.localsock, service_msg, sipMethod,self.errorCode_system[keyValue], 0)
                        LOOPTIMES_Xserver_errorCode += 1
                     
                elif LOOPTIMES_Xserver_errorCode <= len(self.errorCode_system)+len(self.errorCode_Statuserror):
                    keyValue = str(LOOPTIMES_Xserver_errorCode - len(self.errorCode_system))
                    addCaseLog( "[2] Start http exception test, total test time = %s,retCode = %s,sip status code = %s" % (LOOPTIMES_Xserver_errorCode,self.errorCode_Statuserror[keyValue],"404 not found"))
                    addCaseLog("%s Received request(%s %d %s), send 200 OK to the girl (parseReceivedData)" % (service_msg.sipid_number,service_msg.msg_method, service_msg.statusCode, service_msg.statusPhase))
                    self.sendErrorRespond(self.localsock, service_msg, sipMethod,"1000", self.errorCode_Statuserror[keyValue])
                    LOOPTIMES_Xserver_errorCode += 1
                elif LOOPTIMES_Xserver_errorCode <= len(self.errorCode_system)+len(self.errorCode_Statuserror)+1:
                    addCaseLog( "[3] Start time out test, total test time = %s" % (LOOPTIMES_Xserver_errorCode))
                    LOOPTIMES_Xserver_errorCode += 1
                    addCaseLog("time out")
                else:
                    addCaseLog( "[4] finished errorcode test ,now i will respond you correce result, total test time = %s" % (LOOPTIMES_Xserver_errorCode))
                    addCaseLog("%s Received INFO request(%s %d %s), send 200 OK to the girl (parseReceivedData)" % (service_msg.sipid_number,service_msg.msg_method, service_msg.statusCode, service_msg.statusPhase))
                    if str(service_msg.msg_method).lower() == "invite":
                        if service_msg.totag == True:
                            self.infoReceivedTime = 0
                        self.send_INVITE_response_confroom(self.localsock, service_msg)
                        addCaseLog("You are join invite,now Send join meeting NOTIFY  to the girl (parseReceivedData)")
                        self.send_Nofity(self.localsock,service_msg,1)
                        self.infoReceivedTime = self.infoReceivedTime + 1
                    elif str(service_msg.msg_method).lower() == "info":
                        addCaseLog("Received INFO request, send 200 OK to the girl (parseReceivedData)")
                        self.handle_Unknown_request(self.localsock,None, service_msg)
                        if str(str(service_msg.x_gs_conf_control).find("ctrl_present")) != "-1":
                            addCaseLog("Received INFO request, send 200OK to the girl (parseReceivedData)" )
                            self.handle_Unknown_request(self.localsock,None, service_msg)
                            if str(str(service_msg.x_gs_conf_control).find("present-status=1")) != "-1":
                                addCaseLog("Received INFO(start ds) request, send reinvite for av to the girl (parseReceivedData)" )
                                self.send_av_invite(self.localsock,service_msg)
                                addCaseLog("Received INFO(start ds) request, send  NOTIFY(start ds) to the girl (parseReceivedData)" )
                                self.send_Nofity(self.localsock,service_msg,2)
                            else:
                                addCaseLog("Received INFO(stop ds) request, send reinvite for av to the girl (parseReceivedData)" )
                                self.send_av_stop_invite(self.localsock,service_msg)
                                addCaseLog("Received INFO(stop ds) request, send NOTIFY(stop ds) to the girl (parseReceivedData)" )
                                self.send_Nofity(self.localsock,service_msg,3)
                        elif str(str(service_msg.x_gs_conf_control).find("get_all_users")) != "-1":
                            addCaseLog("Received INFO(get all user) request, send NOTIFY(full) to the girl (parseReceivedData)" )
                            self.send_Nofity(self.localsock,service_msg,0)
                        else:
                            addCaseLog("Send NOTIFY  to the girl (parseReceivedData)")
                            self.send_Nofity(self.localsock,service_msg)
                    else:
                        self.handle_Unknown_request(self.localsock,None, service_msg)
                    LOOPTIMES_Xserver_errorCode = 1
                    addCaseLog( "Dear, we finshed \"%s\" errorCode test, total test time = %s , clear the environment" % (service_msg.msg_method,LOOPTIMES_Xserver_errorCode))
                    addCaseLog( "Now you can start \"%s\" test again, test time setted to = %s" % (service_msg.msg_method,LOOPTIMES_Xserver_errorCode))
            else:
                if str(service_msg.msg_method).lower() == "invite":
                    if service_msg.totag == True:
                        self.infoReceivedTime = 0
                    addCaseLog("%s Received INVITE request(%s %d %s), send 200 OK to the girl (parseReceivedData)" % (service_msg.sipid_number,service_msg.msg_method, service_msg.statusCode, service_msg.statusPhase))
                    self.send_INVITE_response_confroom(self.localsock, service_msg)
                    addCaseLog("You are join invite,now Send join meeting NOTIFY  to the girl (parseReceivedData)")
                    self.send_Nofity(self.localsock,service_msg,1)
                    self.av_invite_totag = service_msg.fromtag
                    self.call_id = service_msg.call_id
                    print "self.av_invite_fromtag   %s" % self.av_invite_totag
                elif str(service_msg.msg_method).lower() == "info":
                    addCaseLog("Received INFO request, send 200 OK to the girl (parseReceivedData)")
                    self.handle_Unknown_request(self.localsock,None, service_msg)
                    if str(str(service_msg.x_gs_conf_control).find("ctrl_present")) != "-1":
                        addCaseLog("Received INFO request, send 200OK to the girl (parseReceivedData)" )
                        self.handle_Unknown_request(self.localsock,None, service_msg)
                        if str(str(service_msg.x_gs_conf_control).find("present-status=1")) != "-1":
                            addCaseLog("Received INFO(start ds) request, send reinvite for av to the girl (parseReceivedData)" )
                            self.send_av_invite(self.localsock,service_msg)
                            addCaseLog("Received INFO(start ds) request, send  NOTIFY(start ds) to the girl (parseReceivedData)" )
                            self.send_Nofity(self.localsock,service_msg,2)
                        else:
                            addCaseLog("Received INFO(stop ds) request, send reinvite for av to the girl (parseReceivedData)" )
                            self.send_av_stop_invite(self.localsock,service_msg)
                            addCaseLog("Received INFO(stop ds) request, send NOTIFY(stop ds) to the girl (parseReceivedData)" )
                            self.send_Nofity(self.localsock,service_msg,3)
                    elif str(str(service_msg.x_gs_conf_control).find("get_all_users")) != "-1":
                        addCaseLog("Received INFO(get all user) request, send NOTIFY(full) to the girl (parseReceivedData)" )
                        self.send_Nofity(self.localsock,service_msg,0)
                    else:
                        addCaseLog("Send NOTIFY  to the girl (parseReceivedData)")
                        self.send_Nofity(self.localsock,service_msg)
                elif str(service_msg.msg_method).lower() == "message":
                    addCaseLog("%s Received MESSAGE request(%s %d %s), send 200 OK to the girl (parseReceivedData)" % (service_msg.sipid_number,service_msg.msg_method, service_msg.statusCode, service_msg.statusPhase))
                    self.handle_Unknown_request(self.localsock,None, service_msg)
                    addCaseLog("Send MESSAGE to all (parseReceivedData)")
                    self.send_base_request(self.localsock, "MESSAGE", service_msg, "babababab", "all")
                elif str(service_msg.msg_method).lower() == "register":
                    addCaseLog("%s Received REGISTER request(%s %d %s), send 200 OK to the girl (parseReceivedData)" % (service_msg.sipid_number,service_msg.msg_method, service_msg.statusCode, service_msg.statusPhase))
                    self.handle_Unknown_request(self.localsock,None, service_msg)
                elif str(service_msg.msg_method).lower() == "bye":
                    addCaseLog("Received BYE now , i don't care)")
                else:
                    if str(service_msg.msg_method).lower() == "invite":
                        if service_msg.statusCode == 200:
                            addCaseLog("%s Received invite repond(%s %d %s), send ACK to the girl (parseReceivedData)" % (service_msg.sipid_number,service_msg.msg_method, service_msg.statusCode, service_msg.statusPhase))
                            self.send_ACK_request(self.localsock, service_msg)
        else:
            if str(service_msg.msg_method).lower() == "invite" and service_msg.statusCode == 200:
                addCaseLog("server Received INVITE 200 OK packet(%s %d %s), send ACK to the girl (parseReceivedData)")
                self.send_ACK_request(self.localsock, service_msg,service_msg.dest_ip_number,service_msg.dest_port_number)

    def sendErrorRespond(self,sock,msg_info,sipMethod,xecode="",options=0):
        if xecode =="":
            xecode = 0
        addCaseLog("received client request, request_line = %s" % (self.sipMethod))
        if options == 0:
            ok_response = "SIP/2.0 404 for XEcode error Test\r\n"
            ok_response += msg_info.via_header + "\r\n"
            if self.compare_string(msg_info.snd_via_header, 'NONE') != 0:
                ok_response += msg_info.snd_via_header + "\r\n"
            ok_response += "Contact: <sip:" + msg_info.local_ip_number + ":" + "%d"%msg_info.local_port_number + ";transport=tcp>\r\n"
            ok_response += "Max-Forwards: 70\r\nUser-Agent: python(IPC)\r\n"
            if msg_info.hastotag == True:
                ok_response += "To:%s"%msg_info.to_header + "\r\n"
            else:
                ok_response += "To:%s"%msg_info.to_header + ";tag=201203271"+"\r\n"
                msg_info.totag = "201203271"
            ok_response += "From:%s"%msg_info.from_header + "\r\n"
            ok_response += "Call-ID: %s\r\n" % msg_info.call_id
            ok_response += "CSeq: %s\r\n" %msg_info.cseq
            ok_response += "X-ECode :%s\r\n" % xecode
            expiresindex1 = msg_info.expires_header.find('NONE')
            if expiresindex1 == -1:
                ok_response += "%s\r\n"%msg_info.expires_header
            ok_response += "Content-Length: 0\r\n\r\n"
            debug_print( "from[%s:%d] to[%s:%d]\r\n"%(msg_info.local_ip_number, msg_info.local_port_number, msg_info.dest_ip_number, msg_info.dest_port_number), VERBOSE )
            debug_print( "%s\r\n"%ok_response, VERBOSE )
            XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1
        else:
            ok_response = "SIP/2.0 %s statuscode error test\r\n" % options
            ok_response += msg_info.via_header + "\r\n"
            if self.compare_string(msg_info.snd_via_header, 'NONE') != 0:
                ok_response += msg_info.snd_via_header + "\r\n"
        
            ok_response += "Contact: <sip:" + msg_info.local_ip_number + ":" + "%d"%msg_info.local_port_number + ";transport=udp>\r\n"
            ok_response += "Max-Forwards: 70\r\nUser-Agent: python(IPC)\r\n"
            if msg_info.hastotag == True:
                ok_response += "To:%s"%msg_info.to_header + "\r\n"
            else:
                ok_response += "To:%s"%msg_info.to_header + ";tag=201203271"+"\r\n"
        
                msg_info.totag = "201203271"
            ok_response += "From:%s"%msg_info.from_header + "\r\n"
            ok_response += "Call-ID: %s\r\n" % msg_info.call_id
            ok_response += "CSeq: %s\r\n" %msg_info.cseq
            ok_response += "X-ECode :%s" % xecode
            expiresindex1 = msg_info.expires_header.find('NONE')
            if expiresindex1 == -1:
                ok_response += "%s\r\n"%msg_info.expires_header
            ok_response += "Content-Length: 0\r\n\r\n"
            debug_print( "from[%s:%d] to[%s:%d]\r\n"%(msg_info.local_ip_number, msg_info.local_port_number, msg_info.dest_ip_number, msg_info.dest_port_number), VERBOSE )
            debug_print( "%s\r\n"%ok_response, VERBOSE )
            XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1
        if msg_info.protocol == 'udp':
            sock.sendto(ok_response, (msg_info.dest_ip_number, msg_info.dest_port_number))
        else:
            try:
                sock.sendall(ok_response)
            except Exception as e:
                addCaseLog("send 200OK failed,socket connect failed: %s(sendErrorRespond)") % (str(e))
                self.OnError()
                                                 
    def run(self):
        global service_on
        global LOOPTIMES_webAPI_errorCode
        sendsock = self.localsock
#         connection, client_address = sendsock.accept()
#         (dest_address,dest_port) = client_address
#         self.dest_address = dest_address
#         self.dest_port = dest_port
        while service_on:
            try:
                if self.protocol == 'udp':
                    response, rcvaddress= sendsock.recvfrom(10240)
                else:
                    response = sendsock.recv(10240)
            except Exception as e:
                continue
            if not response:
                continue
            self.parseReceivedData(response, self.sipMethod)
        sendsock.close()

#######################
# sipmethod: "info" | "invite" | "register" | "message"
# testnum  : 1-n  , the test time of sipmethod, if =1, the first "sipmethod" request will start errorcode test
# role     : "all" | "host" | "presenter" | "creater" | "attendee" , all: i am host+ presenter+creater
#######################
class xserver_Exceptional_Common(sipServer_commonlib):
    def __init__(self,sipMethod="",testnum="",role="",localaddress = '',localport = ''):
        self.service_msg = create_sipObject()
        self.service_msg.local_ip_number = localaddress
        self.service_msg.local_port_number = localport
        sipServer_commonlib.__init__(self,self.service_msg)
        if sipMethod == "":
            self.sipMethod = "info"
        else:
            self.sipMethod = sipMethod
        if not str(testnum).isdigit():
            addCaseLog("testnum must be digit(xserver_Exceptional_Common)")
            self.OnError()
        if testnum == "" or int(testnum)<=0:
            self.testnum = 1
        self.testnum = testnum
        self.role = role
    def startXServer(self):
        global service_on
        sendsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sendsock.bind(('%s' % self.localip, self.localport))
#             self.sock.settimeout(3)
        except Exception as e:
            addCaseLog("Xserver bind socket failed: %s " % (e))
            sendsock.close()
            self.OnError()
        sendsock.listen(10)
        addCaseLog("################## WEB simulator server started success, now i am listening################")
        addCaseLog("Server IP = %s, port = %s, testSipMethod = %s,please add in GS meeting config file(webport=%s,weburl:%s and hosts file)" %(self.localip,self.localport,self.sipMethod,self.localport,self.localport))
        while service_on:
            connection, client_address = sendsock.accept()
            (dest_address,dest_port) = client_address
            self.service_msg.dest_ip_number = dest_address
            self.service_msg.dest_port_number = dest_port   
            T1 = xserver_Exceptional_ReceivedPack(connection,self.service_msg,self.sipMethod,self.testnum,self.role)
            T1.start()

    def OnError(self):
        addCaseLog("Xserver Exception error::OnError, case failed")
        setCaseResult("failed")
        sys.exit()

class ipvideotalk_Media_Data(sipServer_commonlib):
    def __init__(self,local_address, local_port,destip="",destport = "",mediadata = ''):
        self.service_msg = create_sipObject()
        self.service_msg.local_ip_number = local_address
        self.service_msg.rtp_media_port = local_port
        sipServer_commonlib.__init__(self,self.service_msg)
        self.version = 128
        self.type = 0
        self.sequence = 1
        self.timestamp = 3103065344
        self.ssrc = 2227653485
        self.payload = "255L"
        self.aList = []
        self.destip = destip
        self.destport = destport
        self.mediadata = ""
    def loopSendNormalRTPPack(self):
        global service_on
        # Create a socket to receive rtp packets and send it back
        sendsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        local_port_num = self.localport
        
        version = struct.pack('B', self.version)
        payload_type = struct.pack('B', self.type)
        sequence = struct.pack('H', self.sequence)
        timestamp = struct.pack('I', self.timestamp)
        ssrc = struct.pack('I', self.ssrc)
        payload = ""
        for i in range(0, self.payload_length):
            payload += struct.pack('B', self.payload[i])

        packet = "".join([version, payload_type, sequence, timestamp, ssrc, payload])

    def getUdpData(self,filename=""):
        if filename == "":
            self.aList.append({'ssrc': 1482779502, 'version': 233, 'sequence': 59358, 'timestamp': 1734699388, 'payload_length': 68, 'type': 223, 'payload': [81L, 82L, 92L, 126L, 221L, 212L, 206L, 206L, 209L, 213L, 219L, 227L, 239L, 250L, 124L, 110L, 100L, 91L, 85L, 87L, 92L, 118L, 229L, 221L, 222L, 230L, 243L, 125L, 117L, 117L, 107L, 96L, 91L, 87L, 87L, 89L, 90L, 99L, 111L, 231L, 215L, 206L, 203L, 207L, 217L, 231L, 247L, 242L, 238L, 240L, 115L, 94L, 89L, 88L, 94L, 109L, 250L, 233L, 224L, 222L, 221L, 228L, 248L, 106L, 94L, 92L, 92L, 94L]})
            self.aList.append({'ssrc': 1583309926, 'version': 206, 'sequence': 57046, 'timestamp': 1803285732, 'payload_length': 68, 'type': 209, 'payload': [92L, 94L, 106L, 240L, 221L, 216L, 220L, 230L, 114L, 104L, 97L, 104L, 101L, 95L, 88L, 86L, 85L, 90L, 95L, 107L, 244L, 223L, 212L, 205L, 205L, 208L, 218L, 229L, 239L, 240L, 236L, 245L, 112L, 98L, 92L, 94L, 100L, 117L, 247L, 236L, 237L, 239L, 242L, 243L, 121L, 109L, 99L, 93L, 91L, 91L, 93L, 93L, 94L, 94L, 99L, 114L, 236L, 221L, 213L, 208L, 209L, 212L, 217L, 223L, 236L, 243L, 253L, 123L]})
            self.aList.append({'ssrc': 4025347565L, 'version': 246, 'sequence': 61935, 'timestamp': 3991925231L, 'payload_length': 68, 'type': 244, 'payload': [238L, 242L, 252L, 125L, 116L, 117L, 120L, 121L, 124L, 119L, 122L, 123L, 255L, 120L, 117L, 115L, 123L, 125L, 126L, 119L, 124L, 119L, 121L, 122L, 252L, 255L, 253L, 126L, 126L, 251L, 252L, 255L, 123L, 125L, 254L, 254L, 250L, 253L, 252L, 255L, 246L, 248L, 248L, 126L, 126L, 125L, 253L, 255L, 254L, 253L, 250L, 250L, 254L, 251L, 122L, 121L, 118L, 122L, 124L, 123L, 125L, 126L, 127L, 252L, 249L, 248L, 254L, 252L]})
            self.aList.append({'ssrc': 4269670012L, 'version': 123, 'sequence': 31867, 'timestamp': 2130639994, 'payload_length': 68, 'type': 124, 'payload': [251L, 249L, 255L, 253L, 253L, 124L, 253L, 123L, 254L, 125L, 254L, 254L, 252L, 255L, 124L, 124L, 253L, 126L, 126L, 126L, 123L, 123L, 121L, 123L, 253L, 255L, 247L, 253L, 250L, 254L, 249L, 254L, 250L, 251L, 254L, 126L, 254L, 126L, 253L, 252L, 127L, 254L, 252L, 123L, 255L, 122L, 122L, 121L, 124L, 122L, 121L, 126L, 123L, 123L, 127L, 122L, 124L, 252L, 252L, 254L, 249L, 253L, 253L, 251L, 250L, 252L, 247L, 255L]})
            self.aList.append({'ssrc': 1532450905, 'version': 223, 'sequence': 32241, 'timestamp': 1549754733, 'payload_length': 68, 'type': 229, 'payload': [93L, 102L, 103L, 94L, 94L, 106L, 215L, 193L, 194L, 203L, 228L, 100L, 103L, 121L, 116L, 255L, 230L, 221L, 212L, 214L, 234L, 91L, 84L, 85L, 94L, 95L, 90L, 84L, 90L, 95L, 94L, 96L, 101L, 97L, 106L, 93L, 110L, 205L, 193L, 198L, 209L, 106L, 98L, 118L, 253L, 120L, 231L, 232L, 220L, 219L, 224L, 239L, 249L, 103L, 92L, 88L, 84L, 86L, 86L, 83L, 93L, 126L, 114L, 101L, 85L, 84L, 233L, 194L]})
            self.aList.append({'ssrc': 3570367708L, 'version': 112, 'sequence': 59835, 'timestamp': 3647692375L, 'payload_length': 68, 'type': 197, 'payload': [103L, 91L, 92L, 112L, 212L, 206L, 109L, 89L, 93L, 92L, 250L, 92L, 81L, 80L, 88L, 96L, 109L, 90L, 113L, 114L, 208L, 188L, 210L, 81L, 107L, 109L, 224L, 218L, 245L, 219L, 206L, 110L, 91L, 93L, 108L, 223L, 209L, 228L, 105L, 87L, 108L, 107L, 95L, 87L, 82L, 83L, 97L, 104L, 98L, 101L, 104L, 111L, 191L, 190L, 108L, 86L, 91L, 254L, 213L, 223L, 241L, 207L, 219L, 105L, 89L, 86L, 236L, 205L]})
            self.aList.append({'ssrc': 3864751986L, 'version': 98, 'sequence': 53110, 'timestamp': 3839877060L, 'payload_length': 68, 'type': 107, 'payload': [214L, 224L, 228L, 224L, 237L, 223L, 126L, 93L, 252L, 98L, 100L, 92L, 90L, 102L, 83L, 87L, 99L, 95L, 91L, 94L, 102L, 230L, 199L, 204L, 227L, 215L, 250L, 253L, 95L, 107L, 224L, 221L, 225L, 223L, 227L, 230L, 222L, 250L, 93L, 115L, 100L, 92L, 91L, 94L, 92L, 85L, 91L, 97L, 95L, 94L, 95L, 111L, 220L, 200L, 211L, 222L, 215L, 232L, 126L, 96L, 240L, 224L, 232L, 237L, 229L, 225L, 229L, 230L]})
            self.aList.append({'ssrc': 4000640887L, 'version': 119, 'sequence': 61295, 'timestamp': 4051234415L, 'payload_length': 68, 'type': 250, 'payload': [117L, 238L, 118L, 238L, 120L, 246L, 251L, 110L, 238L, 106L, 248L, 115L, 119L, 126L, 116L, 124L, 124L, 115L, 245L, 119L, 252L, 251L, 251L, 123L, 238L, 122L, 242L, 124L, 242L, 255L, 246L, 125L, 245L, 114L, 249L, 118L, 121L, 251L, 115L, 125L, 126L, 116L, 251L, 115L, 250L, 124L, 249L, 252L, 251L, 243L, 119L, 241L, 121L, 250L, 246L, 125L, 250L, 253L, 122L, 248L, 113L, 247L, 111L, 127L, 111L, 252L, 112L, 123L]})
            self.aList.append({'ssrc': 1582979417, 'version': 121, 'sequence': 29300, 'timestamp': 1532913264, 'payload_length': 68, 'type': 114, 'payload': [104L, 235L, 215L, 212L, 214L, 213L, 211L, 214L, 227L, 234L, 233L, 238L, 112L, 97L, 97L, 95L, 92L, 91L, 97L, 114L, 126L, 244L, 235L, 224L, 223L, 233L, 235L, 234L, 238L, 254L, 109L, 107L, 101L, 95L, 92L, 91L, 92L, 93L, 94L, 99L, 111L, 238L, 227L, 223L, 222L, 218L, 216L, 219L, 222L, 222L, 225L, 234L, 124L, 111L, 106L, 101L, 97L, 98L, 105L, 110L, 112L, 123L, 246L, 238L, 237L, 235L, 233L, 235L]})
            self.aList.append({'ssrc': 4076301934L, 'version': 249, 'sequence': 30329, 'timestamp': 1869638500, 'payload_length': 68, 'type': 108, 'payload': [236L, 227L, 237L, 242L, 248L, 109L, 108L, 102L, 106L, 109L, 107L, 116L, 112L, 106L, 101L, 95L, 95L, 95L, 101L, 108L, 236L, 218L, 210L, 216L, 218L, 214L, 230L, 246L, 117L, 118L, 119L, 102L, 111L, 125L, 110L, 123L, 115L, 242L, 238L, 237L, 228L, 248L, 249L, 253L, 103L, 108L, 101L, 107L, 109L, 104L, 119L, 110L, 101L, 101L, 93L, 97L, 98L, 97L, 122L, 234L, 216L, 209L, 219L, 210L, 215L, 232L, 237L, 114L]})
            self.aList.append({'ssrc': 1583503963, 'version': 211, 'sequence': 60383, 'timestamp': 1482646896, 'payload_length': 68, 'type': 214, 'payload': [121L, 237L, 119L, 220L, 237L, 234L, 239L, 255L, 109L, 97L, 94L, 88L, 85L, 88L, 86L, 93L, 99L, 243L, 226L, 217L, 210L, 205L, 209L, 205L, 209L, 214L, 222L, 229L, 120L, 102L, 94L, 91L, 87L, 90L, 98L, 97L, 109L, 236L, 246L, 234L, 227L, 238L, 248L, 249L, 107L, 97L, 95L, 90L, 89L, 89L, 88L, 91L, 95L, 106L, 238L, 222L, 215L, 213L, 205L, 212L, 211L, 214L, 228L, 238L, 253L, 103L, 93L, 91L]})
            self.aList.append({'ssrc': 3706092889L, 'version': 103, 'sequence': 54896, 'timestamp': 1758906821, 'payload_length': 68, 'type': 102, 'payload': [228L, 251L, 254L, 253L, 108L, 101L, 93L, 121L, 231L, 223L, 247L, 107L, 95L, 108L, 123L, 252L, 111L, 98L, 93L, 93L, 91L, 94L, 91L, 94L, 99L, 107L, 221L, 200L, 197L, 206L, 238L, 89L, 101L, 247L, 222L, 222L, 234L, 127L, 122L, 105L, 105L, 97L, 109L, 243L, 228L, 231L, 123L, 103L, 103L, 111L, 254L, 127L, 107L, 97L, 93L, 92L, 93L, 95L, 94L, 96L, 99L, 242L, 206L, 198L, 203L, 220L, 100L, 96L]})
            self.aList.append({'ssrc': 1541170410, 'version': 220, 'sequence': 23002, 'timestamp': 1793285338, 'payload_length': 68, 'type': 90, 'payload': [221L, 96L, 233L, 109L, 242L, 112L, 233L, 97L, 222L, 98L, 223L, 95L, 223L, 97L, 237L, 108L, 235L, 99L, 225L, 104L, 234L, 109L, 248L, 247L, 108L, 236L, 117L, 249L, 126L, 122L, 240L, 113L, 249L, 126L, 246L, 109L, 230L, 104L, 230L, 101L, 227L, 102L, 232L, 107L, 236L, 122L, 120L, 240L, 118L, 123L, 127L, 254L, 122L, 125L, 126L, 255L, 111L, 237L, 106L, 238L, 117L, 253L, 254L, 253L, 114L, 242L, 113L, 247L]})
            self.aList.append({'ssrc': 2037968345, 'version': 101, 'sequence': 60533, 'timestamp': 3503214813L, 'payload_length': 68, 'type': 102, 'payload': [121L, 253L, 250L, 255L, 248L, 250L, 125L, 112L, 105L, 106L, 249L, 226L, 220L, 225L, 111L, 90L, 86L, 90L, 104L, 110L, 107L, 98L, 95L, 97L, 104L, 105L, 105L, 100L, 109L, 242L, 220L, 207L, 204L, 207L, 218L, 243L, 122L, 121L, 254L, 255L, 125L, 117L, 126L, 255L, 254L, 119L, 109L, 106L, 118L, 239L, 224L, 223L, 237L, 105L, 93L, 91L, 95L, 103L, 103L, 100L, 97L, 97L, 101L, 105L, 105L, 101L, 102L, 118L]})
            self.aList.append({'ssrc': 4277895038L, 'version': 253, 'sequence': 32127, 'timestamp': 2105441917, 'payload_length': 68, 'type': 254, 'payload': [125L, 254L, 254L, 254L, 126L, 126L, 255L, 252L, 253L, 254L, 126L, 255L, 125L, 126L, 125L, 255L, 126L, 124L, 124L, 125L, 255L, 125L, 126L, 126L, 254L, 254L, 253L, 253L, 254L, 126L, 126L, 253L, 252L, 252L, 254L, 255L, 125L, 125L, 124L, 126L, 125L, 127L, 127L, 125L, 126L, 127L, 254L, 253L, 253L, 252L, 253L, 254L, 254L, 123L, 127L, 127L, 253L, 253L, 254L, 252L, 254L, 126L, 255L, 255L, 253L, 253L, 126L, 255L]})
            self.aList.append({'ssrc': 4269078012L, 'version': 123, 'sequence': 64251, 'timestamp': 2105409405, 'payload_length': 68, 'type': 255, 'payload': [248L, 116L, 244L, 112L, 126L, 124L, 250L, 249L, 127L, 112L, 241L, 249L, 122L, 123L, 247L, 123L, 246L, 113L, 254L, 249L, 125L, 116L, 239L, 122L, 252L, 251L, 123L, 253L, 254L, 120L, 118L, 239L, 115L, 247L, 125L, 120L, 243L, 123L, 123L, 253L, 255L, 247L, 116L, 247L, 119L, 242L, 114L, 124L, 243L, 253L, 121L, 122L, 244L, 125L, 125L, 125L, 244L, 113L, 240L, 111L, 241L, 123L, 120L, 246L, 124L, 126L, 121L, 239L]})
            self.aList.append({'ssrc': 2122252030, 'version': 253, 'sequence': 65277, 'timestamp': 4261346943L, 'payload_length': 68, 'type': 252, 'payload': [126L, 125L, 254L, 124L, 125L, 255L, 126L, 126L, 126L, 255L, 127L, 253L, 127L, 255L, 127L, 255L, 126L, 123L, 124L, 124L, 125L, 126L, 126L, 254L, 254L, 255L, 253L, 253L, 252L, 251L, 252L, 252L, 127L, 255L, 126L, 254L, 254L, 125L, 126L, 126L, 126L, 254L, 124L, 126L, 126L, 254L, 255L, 255L, 127L, 253L, 254L, 253L, 254L, 254L, 255L, 254L, 255L, 127L, 126L, 126L, 124L, 126L, 126L, 254L, 126L, 255L, 125L, 127L]})
            self.aList.append({'ssrc': 4277566441L, 'version': 107, 'sequence': 60782, 'timestamp': 1894578939, 'payload_length': 68, 'type': 233, 'payload': [238L, 109L, 229L, 97L, 222L, 94L, 232L, 113L, 127L, 250L, 116L, 244L, 121L, 252L, 125L, 251L, 251L, 251L, 123L, 246L, 124L, 253L, 124L, 126L, 246L, 119L, 123L, 248L, 119L, 119L, 251L, 111L, 246L, 115L, 111L, 237L, 102L, 235L, 103L, 235L, 105L, 241L, 105L, 229L, 101L, 226L, 97L, 223L, 102L, 232L, 111L, 235L, 117L, 238L, 108L, 231L, 105L, 236L, 108L, 239L, 111L, 248L, 118L, 242L, 111L, 236L, 110L, 246L]})
            self.aList.append({'ssrc': 1541664365, 'version': 107, 'sequence': 21758, 'timestamp': 4017907791L, 'payload_length': 68, 'type': 94, 'payload': [77L, 91L, 207L, 202L, 209L, 238L, 123L, 245L, 103L, 102L, 216L, 205L, 213L, 242L, 87L, 100L, 125L, 124L, 239L, 239L, 104L, 75L, 70L, 92L, 207L, 213L, 213L, 116L, 79L, 78L, 73L, 101L, 207L, 201L, 203L, 235L, 93L, 97L, 121L, 219L, 223L, 215L, 219L, 82L, 90L, 93L, 212L, 206L, 223L, 125L, 91L, 77L, 74L, 84L, 224L, 203L, 217L, 245L, 88L, 72L, 94L, 245L, 123L, 221L, 215L, 213L, 229L, 126L]})
            self.aList.append({'ssrc': 2079846366, 'version': 114, 'sequence': 54482, 'timestamp': 3755729370L, 'payload_length': 68, 'type': 221, 'payload': [110L, 102L, 89L, 90L, 91L, 108L, 126L, 233L, 224L, 222L, 223L, 239L, 244L, 123L, 250L, 116L, 105L, 97L, 91L, 90L, 86L, 89L, 89L, 104L, 233L, 214L, 215L, 219L, 223L, 219L, 219L, 225L, 232L, 245L, 238L, 123L, 109L, 94L, 92L, 95L, 101L, 115L, 253L, 230L, 223L, 227L, 235L, 125L, 239L, 252L, 126L, 103L, 96L, 94L, 90L, 90L, 85L, 89L, 94L, 245L, 216L, 213L, 216L, 220L, 218L, 214L, 222L, 227L]})
            self.aList.append({'ssrc': 3670924493L, 'version': 94, 'sequence': 62323, 'timestamp': 3622294380L, 'payload_length': 68, 'type': 92, 'payload': [212L, 231L, 220L, 112L, 121L, 116L, 86L, 255L, 86L, 102L, 100L, 94L, 107L, 94L, 106L, 89L, 109L, 84L, 100L, 91L, 90L, 250L, 109L, 126L, 211L, 237L, 207L, 207L, 214L, 205L, 211L, 216L, 221L, 224L, 107L, 246L, 95L, 90L, 108L, 84L, 101L, 94L, 99L, 93L, 110L, 89L, 102L, 94L, 88L, 98L, 90L, 95L, 237L, 105L, 225L, 211L, 236L, 202L, 215L, 207L, 207L, 212L, 221L, 223L, 236L, 105L, 126L, 89L]})
            self.aList.append({'ssrc': 2147417853, 'version': 253, 'sequence': 64766, 'timestamp': 4278058239L, 'payload_length': 68, 'type': 252, 'payload': [125L, 255L, 125L, 125L, 122L, 123L, 124L, 123L, 123L, 122L, 123L, 124L, 126L, 254L, 254L, 252L, 252L, 251L, 252L, 253L, 251L, 253L, 252L, 252L, 251L, 252L, 252L, 253L, 253L, 254L, 255L, 255L, 126L, 126L, 122L, 121L, 122L, 123L, 124L, 123L, 124L, 126L, 124L, 126L, 254L, 252L, 252L, 254L, 251L, 253L, 253L, 253L, 254L, 254L, 127L, 254L, 251L, 253L, 253L, 253L, 253L, 254L, 254L, 126L, 125L, 124L, 122L, 123L]})
            self.aList.append({'ssrc': 1802268531, 'version': 109, 'sequence': 30064, 'timestamp': 2054913401, 'payload_length': 68, 'type': 108, 'payload': [107L, 109L, 119L, 255L, 243L, 236L, 231L, 228L, 226L, 227L, 227L, 230L, 234L, 241L, 252L, 119L, 113L, 107L, 107L, 107L, 108L, 110L, 113L, 120L, 123L, 126L, 254L, 124L, 119L, 112L, 108L, 105L, 105L, 105L, 109L, 116L, 254L, 242L, 235L, 231L, 226L, 225L, 224L, 225L, 229L, 233L, 239L, 250L, 121L, 113L, 109L, 107L, 107L, 107L, 108L, 109L, 113L, 118L, 122L, 123L, 122L, 122L, 116L, 111L, 108L, 107L, 108L, 112L]})
            self.aList.append({'ssrc': 4126141157L, 'version': 99, 'sequence': 26210, 'timestamp': 3840605549L, 'payload_length': 68, 'type': 97, 'payload': [241L, 237L, 234L, 233L, 240L, 253L, 115L, 112L, 117L, 253L, 245L, 246L, 125L, 121L, 114L, 119L, 120L, 121L, 116L, 107L, 104L, 102L, 105L, 113L, 252L, 234L, 228L, 229L, 233L, 239L, 248L, 250L, 249L, 245L, 246L, 126L, 117L, 108L, 107L, 109L, 122L, 251L, 246L, 251L, 255L, 121L, 123L, 127L, 255L, 123L, 111L, 106L, 104L, 105L, 112L, 250L, 235L, 227L, 226L, 229L, 234L, 238L, 239L, 238L, 239L, 238L, 248L, 123L]})
            self.aList.append({'ssrc': 4025087583L, 'version': 125, 'sequence': 23398, 'timestamp': 1515608922, 'payload_length': 68, 'type': 107, 'payload': [208L, 214L, 216L, 207L, 216L, 218L, 228L, 236L, 253L, 98L, 98L, 93L, 87L, 94L, 101L, 104L, 106L, 231L, 234L, 238L, 223L, 231L, 238L, 250L, 120L, 104L, 93L, 93L, 90L, 86L, 91L, 93L, 117L, 239L, 249L, 216L, 216L, 219L, 211L, 216L, 217L, 222L, 230L, 234L, 113L, 107L, 101L, 91L, 93L, 96L, 100L, 105L, 117L, 237L, 238L, 237L, 225L, 234L, 238L, 244L, 115L, 105L, 95L, 93L, 91L, 88L, 92L, 94L]})
            self.aList.append({'ssrc': 2004251765, 'version': 123, 'sequence': 31610, 'timestamp': 1953855096, 'payload_length': 68, 'type': 122, 'payload': [121L, 122L, 126L, 252L, 247L, 244L, 241L, 239L, 239L, 239L, 241L, 244L, 246L, 250L, 252L, 254L, 124L, 122L, 120L, 119L, 118L, 117L, 117L, 118L, 118L, 118L, 120L, 120L, 122L, 122L, 124L, 125L, 255L, 126L, 254L, 252L, 253L, 252L, 251L, 251L, 251L, 251L, 250L, 251L, 249L, 252L, 251L, 252L, 252L, 252L, 253L, 254L, 254L, 126L, 125L, 125L, 124L, 126L, 125L, 125L, 125L, 124L, 124L, 125L, 124L, 125L, 124L, 124L]})
            self.aList.append({'ssrc': 2139094654, 'version': 127, 'sequence': 32383, 'timestamp': 2139061630, 'payload_length': 68, 'type': 126, 'payload': [126L, 126L, 126L, 126L, 126L, 126L, 127L, 127L, 126L, 125L, 127L, 254L, 254L, 253L, 254L, 126L, 126L, 127L, 255L, 127L, 127L, 126L, 126L, 254L, 127L, 126L, 126L, 127L, 255L, 126L, 255L, 126L, 127L, 255L, 127L, 127L, 254L, 126L, 126L, 254L, 254L, 253L, 253L, 253L, 253L, 253L, 127L, 127L, 254L, 255L, 126L, 254L, 126L, 126L, 126L, 255L, 255L, 255L, 254L, 126L, 125L, 126L, 127L, 126L, 125L, 126L, 127L, 127L]})
            self.aList.append({'ssrc': 1617781880, 'version': 218, 'sequence': 30587, 'timestamp': 3764616288L, 'payload_length': 68, 'type': 97, 'payload': [98L, 96L, 95L, 122L, 105L, 110L, 122L, 253L, 218L, 208L, 230L, 223L, 216L, 229L, 234L, 109L, 235L, 247L, 101L, 107L, 111L, 115L, 252L, 119L, 245L, 253L, 246L, 240L, 123L, 116L, 112L, 106L, 112L, 112L, 121L, 120L, 113L, 106L, 104L, 99L, 100L, 102L, 101L, 100L, 109L, 220L, 207L, 234L, 223L, 215L, 230L, 235L, 107L, 228L, 237L, 106L, 109L, 112L, 109L, 101L, 95L, 247L, 253L, 233L, 216L, 250L, 109L, 236L]})
            self.aList.append({'ssrc': 1668247133, 'version': 246, 'sequence': 23278, 'timestamp': 4015420779L, 'payload_length': 68, 'type': 100, 'payload': [109L, 100L, 100L, 108L, 92L, 115L, 110L, 113L, 125L, 223L, 239L, 221L, 217L, 220L, 219L, 213L, 225L, 223L, 224L, 245L, 123L, 250L, 107L, 92L, 243L, 88L, 107L, 107L, 95L, 110L, 97L, 107L, 96L, 95L, 106L, 92L, 100L, 116L, 120L, 111L, 221L, 229L, 229L, 210L, 221L, 218L, 216L, 222L, 228L, 235L, 235L, 113L, 108L, 251L, 88L, 122L, 103L, 93L, 246L, 95L, 123L, 102L, 106L, 107L, 94L, 103L, 102L, 91L]})
            self.aList.append({'ssrc': 4042387956L, 'version': 124, 'sequence': 32253, 'timestamp': 4127063550L, 'payload_length': 68, 'type': 119, 'payload': [238L, 239L, 243L, 246L, 247L, 251L, 124L, 122L, 115L, 116L, 112L, 113L, 112L, 116L, 118L, 119L, 121L, 122L, 124L, 121L, 122L, 121L, 125L, 125L, 255L, 251L, 247L, 243L, 241L, 240L, 240L, 241L, 241L, 246L, 249L, 252L, 127L, 124L, 122L, 123L, 119L, 119L, 121L, 120L, 123L, 123L, 122L, 124L, 124L, 122L, 122L, 122L, 121L, 121L, 123L, 124L, 125L, 253L, 251L, 249L, 250L, 249L, 247L, 248L, 248L, 250L, 250L, 250L]})
            self.aList.append({'ssrc': 2138930815, 'version': 253, 'sequence': 32637, 'timestamp': 2122219134, 'payload_length': 68, 'type': 127, 'payload': [252L, 253L, 253L, 253L, 254L, 126L, 126L, 254L, 254L, 255L, 255L, 254L, 253L, 255L, 126L, 126L, 255L, 254L, 127L, 126L, 254L, 253L, 255L, 126L, 126L, 254L, 255L, 255L, 125L, 125L, 126L, 125L, 123L, 124L, 255L, 126L, 126L, 125L, 126L, 127L, 125L, 126L, 126L, 126L, 255L, 125L, 255L, 255L, 253L, 253L, 126L, 255L, 254L, 253L, 254L, 127L, 253L, 253L, 255L, 255L, 254L, 254L, 254L, 255L, 255L, 254L, 254L, 253L]})
            self.aList.append({'ssrc': 1902902135, 'version': 247, 'sequence': 29674, 'timestamp': 2104619774, 'payload_length': 68, 'type': 247, 'payload': [110L, 100L, 101L, 110L, 94L, 103L, 105L, 100L, 102L, 106L, 103L, 105L, 105L, 99L, 112L, 95L, 125L, 95L, 120L, 119L, 100L, 234L, 118L, 252L, 124L, 126L, 252L, 108L, 224L, 122L, 237L, 230L, 231L, 236L, 230L, 227L, 117L, 232L, 250L, 244L, 246L, 249L, 241L, 115L, 126L, 123L, 117L, 113L, 253L, 113L, 121L, 254L, 242L, 249L, 235L, 230L, 124L, 228L, 125L, 122L, 113L, 109L, 94L, 100L, 101L, 95L, 99L, 104L]})
            self.aList.append({'ssrc': 1650288376, 'version': 96, 'sequence': 64227, 'timestamp': 4017971817L, 'payload_length': 68, 'type': 246, 'payload': [109L, 118L, 95L, 85L, 83L, 93L, 225L, 209L, 213L, 228L, 254L, 223L, 218L, 212L, 223L, 236L, 236L, 238L, 237L, 104L, 91L, 89L, 103L, 233L, 229L, 239L, 98L, 102L, 113L, 237L, 127L, 103L, 96L, 95L, 110L, 104L, 91L, 82L, 85L, 123L, 213L, 209L, 219L, 246L, 232L, 219L, 214L, 218L, 236L, 238L, 240L, 236L, 125L, 94L, 90L, 93L, 125L, 226L, 236L, 110L, 97L, 107L, 241L, 249L, 122L, 94L, 100L, 103L]})
            self.aList.append({'ssrc': 1811708006, 'version': 110, 'sequence': 28658, 'timestamp': 3975603196L, 'payload_length': 68, 'type': 105, 'payload': [228L, 244L, 254L, 113L, 105L, 239L, 104L, 103L, 233L, 224L, 228L, 104L, 244L, 114L, 103L, 108L, 105L, 241L, 241L, 241L, 233L, 109L, 113L, 254L, 107L, 223L, 124L, 100L, 245L, 231L, 238L, 100L, 248L, 231L, 244L, 126L, 250L, 239L, 118L, 99L, 226L, 231L, 121L, 111L, 238L, 250L, 94L, 113L, 233L, 249L, 250L, 122L, 117L, 230L, 103L, 88L, 253L, 238L, 114L, 114L, 228L, 120L, 89L, 119L, 120L, 97L, 121L, 239L]})
            self.aList.append({'ssrc': 4261248635L, 'version': 245, 'sequence': 64765, 'timestamp': 4185914879L, 'payload_length': 68, 'type': 121, 'payload': [123L, 255L, 249L, 123L, 252L, 245L, 119L, 247L, 125L, 254L, 127L, 121L, 244L, 115L, 246L, 125L, 124L, 249L, 119L, 248L, 120L, 247L, 116L, 251L, 254L, 113L, 239L, 119L, 127L, 249L, 119L, 249L, 117L, 245L, 115L, 245L, 120L, 251L, 255L, 123L, 251L, 118L, 242L, 114L, 246L, 120L, 253L, 125L, 121L, 251L, 123L, 251L, 123L, 247L, 116L, 242L, 117L, 250L, 124L, 253L, 254L, 123L, 246L, 121L, 254L, 249L, 119L, 244L]})
            self.aList.append({'ssrc': 3739085670L, 'version': 214, 'sequence': 60372, 'timestamp': 1684889973, 'payload_length': 68, 'type': 201, 'payload': [233L, 118L, 122L, 251L, 248L, 108L, 101L, 117L, 122L, 249L, 114L, 118L, 244L, 249L, 108L, 103L, 100L, 103L, 94L, 92L, 94L, 103L, 122L, 227L, 209L, 203L, 214L, 234L, 119L, 103L, 104L, 94L, 106L, 233L, 223L, 229L, 238L, 252L, 246L, 110L, 106L, 245L, 248L, 125L, 116L, 105L, 123L, 114L, 110L, 114L, 118L, 115L, 109L, 97L, 95L, 93L, 94L, 111L, 123L, 239L, 213L, 204L, 216L, 228L, 252L, 107L, 115L, 95L]})
            self.aList.append({'ssrc': 4143020793L, 'version': 110, 'sequence': 29036, 'timestamp': 1970697325, 'payload_length': 68, 'type': 110, 'payload': [238L, 239L, 234L, 236L, 233L, 234L, 237L, 234L, 239L, 242L, 248L, 249L, 117L, 255L, 109L, 111L, 110L, 105L, 106L, 105L, 105L, 103L, 108L, 106L, 109L, 113L, 116L, 122L, 252L, 239L, 242L, 232L, 232L, 231L, 226L, 232L, 227L, 235L, 229L, 245L, 236L, 255L, 126L, 125L, 109L, 118L, 111L, 107L, 116L, 108L, 110L, 110L, 110L, 107L, 109L, 108L, 105L, 109L, 106L, 110L, 114L, 117L, 244L, 253L, 231L, 236L, 227L, 227L]})
            self.aList.append({'ssrc': 1936417887, 'version': 227, 'sequence': 31983, 'timestamp': 1583637357, 'payload_length': 68, 'type': 234, 'payload': [248L, 126L, 236L, 231L, 253L, 231L, 238L, 253L, 126L, 124L, 102L, 107L, 96L, 98L, 100L, 95L, 100L, 108L, 105L, 112L, 237L, 236L, 226L, 222L, 216L, 219L, 220L, 221L, 222L, 234L, 239L, 245L, 111L, 105L, 99L, 98L, 95L, 99L, 105L, 120L, 109L, 246L, 235L, 125L, 237L, 235L, 245L, 251L, 250L, 111L, 110L, 102L, 100L, 102L, 98L, 99L, 104L, 105L, 107L, 117L, 248L, 234L, 229L, 221L, 218L, 219L, 221L, 219L]})
            self.aList.append({'ssrc': 2113830655, 'version': 254, 'sequence': 65407, 'timestamp': 2139094911, 'payload_length': 68, 'type': 254, 'payload': [126L, 127L, 127L, 253L, 255L, 254L, 254L, 254L, 126L, 254L, 255L, 254L, 255L, 254L, 254L, 127L, 254L, 255L, 254L, 127L, 254L, 254L, 255L, 254L, 254L, 255L, 127L, 125L, 125L, 126L, 126L, 125L, 126L, 125L, 126L, 127L, 127L, 126L, 255L, 255L, 126L, 254L, 126L, 255L, 126L, 126L, 127L, 127L, 126L, 127L, 127L, 127L, 127L, 126L, 254L, 126L, 254L, 255L, 254L, 254L, 254L, 254L, 126L, 127L, 254L, 254L, 254L, 254L]})
            self.aList.append({'ssrc': 1785426026, 'version': 235, 'sequence': 62718, 'timestamp': 1753049971, 'payload_length': 68, 'type': 245, 'payload': [106L, 108L, 97L, 101L, 106L, 98L, 104L, 111L, 106L, 114L, 120L, 237L, 235L, 235L, 216L, 227L, 219L, 218L, 223L, 222L, 227L, 226L, 238L, 246L, 238L, 116L, 110L, 120L, 107L, 106L, 109L, 108L, 106L, 104L, 108L, 104L, 102L, 108L, 103L, 102L, 105L, 105L, 105L, 109L, 250L, 252L, 243L, 224L, 231L, 223L, 223L, 222L, 226L, 230L, 230L, 237L, 252L, 251L, 115L, 110L, 109L, 107L, 109L, 109L, 106L, 114L, 109L, 110L]})
            self.aList.append({'ssrc': 4227725808L, 'version': 112, 'sequence': 53727, 'timestamp': 3738361819L, 'payload_length': 68, 'type': 250, 'payload': [116L, 100L, 122L, 254L, 101L, 107L, 109L, 114L, 119L, 117L, 248L, 237L, 121L, 119L, 118L, 108L, 104L, 101L, 106L, 111L, 107L, 108L, 110L, 110L, 106L, 110L, 121L, 228L, 209L, 216L, 227L, 211L, 222L, 234L, 123L, 118L, 248L, 121L, 97L, 118L, 125L, 108L, 105L, 101L, 119L, 124L, 115L, 124L, 238L, 126L, 119L, 103L, 110L, 110L, 102L, 102L, 110L, 111L, 109L, 103L, 109L, 111L, 111L, 237L, 213L, 210L, 228L, 219L]})
            self.aList.append({'ssrc': 4076792810L, 'version': 111, 'sequence': 30314, 'timestamp': 4151996017L, 'payload_length': 68, 'type': 110, 'payload': [246L, 122L, 110L, 103L, 110L, 109L, 106L, 106L, 108L, 116L, 124L, 122L, 253L, 244L, 237L, 233L, 234L, 239L, 236L, 238L, 240L, 242L, 251L, 246L, 250L, 253L, 124L, 121L, 122L, 123L, 118L, 119L, 120L, 122L, 123L, 123L, 122L, 125L, 126L, 125L, 124L, 125L, 126L, 124L, 125L, 123L, 123L, 122L, 124L, 122L, 122L, 123L, 122L, 124L, 125L, 125L, 255L, 254L, 253L, 252L, 250L, 249L, 248L, 247L, 249L, 248L, 249L, 250L]})
            self.aList.append({'ssrc': 4236049790L, 'version': 126, 'sequence': 64892, 'timestamp': 4269735548L, 'payload_length': 68, 'type': 254, 'payload': [125L, 253L, 126L, 254L, 127L, 126L, 254L, 253L, 126L, 252L, 125L, 253L, 126L, 254L, 125L, 254L, 125L, 253L, 123L, 252L, 124L, 252L, 255L, 253L, 253L, 253L, 255L, 251L, 125L, 251L, 125L, 253L, 254L, 126L, 252L, 125L, 254L, 127L, 127L, 124L, 251L, 122L, 250L, 121L, 253L, 126L, 125L, 255L, 125L, 127L, 127L, 127L, 126L, 254L, 124L, 254L, 124L, 126L, 126L, 126L, 255L, 125L, 125L, 253L, 123L, 251L, 123L, 250L]})
            self.aList.append({'ssrc': 2037938812, 'version': 244, 'sequence': 63991, 'timestamp': 2113863163, 'payload_length': 68, 'type': 246, 'payload': [119L, 120L, 119L, 119L, 119L, 121L, 122L, 123L, 125L, 126L, 126L, 126L, 127L, 254L, 252L, 252L, 251L, 252L, 252L, 251L, 251L, 250L, 251L, 251L, 250L, 252L, 251L, 253L, 253L, 253L, 255L, 254L, 127L, 126L, 126L, 125L, 126L, 126L, 126L, 125L, 126L, 126L, 126L, 125L, 125L, 125L, 124L, 124L, 125L, 125L, 126L, 255L, 255L, 254L, 254L, 254L, 253L, 254L, 253L, 252L, 254L, 254L, 126L, 255L, 127L, 127L, 254L, 126L]})
            self.aList.append({'ssrc': 4193909499L, 'version': 123, 'sequence': 32123, 'timestamp': 4244537214L, 'payload_length': 68, 'type': 123, 'payload': [247L, 248L, 248L, 247L, 248L, 249L, 251L, 252L, 253L, 126L, 126L, 125L, 123L, 123L, 122L, 121L, 121L, 121L, 122L, 121L, 121L, 122L, 123L, 124L, 125L, 127L, 255L, 255L, 253L, 252L, 251L, 251L, 250L, 249L, 249L, 250L, 249L, 249L, 250L, 250L, 251L, 252L, 252L, 253L, 127L, 125L, 124L, 122L, 123L, 122L, 121L, 121L, 121L, 122L, 122L, 123L, 123L, 123L, 124L, 125L, 125L, 126L, 125L, 255L, 254L, 254L, 253L, 253L]})
            self.aList.append({'ssrc': 4269604221L, 'version': 251, 'sequence': 32252, 'timestamp': 4294868222L, 'payload_length': 68, 'type': 124, 'payload': [124L, 253L, 127L, 254L, 253L, 126L, 253L, 254L, 126L, 254L, 127L, 124L, 253L, 125L, 127L, 254L, 124L, 252L, 125L, 252L, 254L, 251L, 125L, 251L, 125L, 254L, 255L, 124L, 252L, 125L, 254L, 124L, 255L, 126L, 254L, 127L, 125L, 252L, 124L, 255L, 126L, 127L, 254L, 126L, 254L, 126L, 254L, 126L, 126L, 254L, 127L, 254L, 126L, 126L, 254L, 125L, 254L, 126L, 253L, 126L, 255L, 254L, 125L, 253L, 126L, 255L, 254L, 126L]})
            self.aList.append({'ssrc': 2097150075, 'version': 107, 'sequence': 63342, 'timestamp': 4294670075L, 'payload_length': 68, 'type': 236, 'payload': [253L, 119L, 241L, 109L, 237L, 112L, 248L, 124L, 248L, 118L, 247L, 125L, 255L, 250L, 252L, 117L, 246L, 116L, 250L, 122L, 253L, 124L, 252L, 125L, 252L, 254L, 126L, 241L, 111L, 235L, 106L, 235L, 109L, 243L, 123L, 124L, 122L, 246L, 110L, 238L, 111L, 239L, 116L, 242L, 115L, 246L, 122L, 250L, 122L, 245L, 121L, 252L, 248L, 116L, 243L, 112L, 241L, 111L, 239L, 108L, 238L, 111L, 242L, 119L, 252L, 251L, 121L, 252L]})
            self.aList.append({'ssrc': 3705961567L, 'version': 231, 'sequence': 25463, 'timestamp': 1414681178, 'payload_length': 68, 'type': 241, 'payload': [213L, 212L, 206L, 207L, 208L, 216L, 229L, 121L, 99L, 91L, 89L, 88L, 90L, 92L, 101L, 111L, 236L, 229L, 222L, 223L, 230L, 249L, 105L, 94L, 89L, 86L, 84L, 85L, 93L, 121L, 225L, 215L, 208L, 210L, 207L, 210L, 209L, 216L, 224L, 119L, 96L, 86L, 87L, 89L, 93L, 95L, 101L, 107L, 247L, 232L, 223L, 226L, 239L, 105L, 92L, 86L, 83L, 86L, 91L, 108L, 241L, 224L, 216L, 214L, 209L, 208L, 208L, 212L]})
            self.aList.append({'ssrc': 2003857263, 'version': 105, 'sequence': 28527, 'timestamp': 1903064433, 'payload_length': 68, 'type': 112, 'payload': [252L, 250L, 241L, 227L, 227L, 224L, 221L, 220L, 222L, 222L, 228L, 233L, 244L, 126L, 114L, 104L, 101L, 102L, 99L, 99L, 103L, 106L, 109L, 110L, 115L, 116L, 114L, 113L, 114L, 109L, 111L, 110L, 112L, 110L, 126L, 243L, 245L, 233L, 224L, 226L, 223L, 220L, 221L, 222L, 226L, 231L, 235L, 251L, 120L, 109L, 103L, 100L, 98L, 96L, 99L, 100L, 104L, 108L, 109L, 114L, 117L, 116L, 113L, 114L, 109L, 111L, 109L, 110L]})
            self.aList.append({'ssrc': 1978756446, 'version': 108, 'sequence': 30971, 'timestamp': 1533111676, 'payload_length': 68, 'type': 113, 'payload': [102L, 103L, 109L, 231L, 205L, 213L, 98L, 107L, 246L, 235L, 224L, 234L, 234L, 221L, 252L, 100L, 111L, 236L, 232L, 106L, 102L, 115L, 113L, 251L, 115L, 254L, 124L, 98L, 86L, 97L, 125L, 247L, 111L, 104L, 107L, 113L, 231L, 207L, 214L, 104L, 104L, 244L, 238L, 228L, 232L, 234L, 225L, 253L, 101L, 255L, 239L, 116L, 118L, 111L, 105L, 125L, 126L, 111L, 255L, 112L, 94L, 93L, 102L, 124L, 242L, 112L, 103L, 112L]})
            self.aList.append({'ssrc': 3620855025L, 'version': 221, 'sequence': 22113, 'timestamp': 1531923791, 'payload_length': 68, 'type': 251, 'payload': [217L, 230L, 127L, 98L, 83L, 76L, 71L, 70L, 74L, 79L, 106L, 214L, 200L, 192L, 191L, 197L, 203L, 219L, 238L, 101L, 89L, 81L, 77L, 77L, 85L, 110L, 222L, 210L, 209L, 214L, 222L, 252L, 107L, 85L, 77L, 71L, 70L, 72L, 78L, 90L, 229L, 204L, 195L, 190L, 192L, 199L, 210L, 236L, 105L, 89L, 82L, 78L, 76L, 80L, 94L, 229L, 212L, 205L, 209L, 217L, 238L, 104L, 88L, 78L, 73L, 71L, 70L, 75L]})
            self.aList.append({'ssrc': 4294967166L, 'version': 255, 'sequence': 32383, 'timestamp': 2122219134, 'payload_length': 68, 'type': 255, 'payload': [255L, 254L, 254L, 253L, 255L, 254L, 127L, 127L, 126L, 255L, 253L, 253L, 254L, 255L, 127L, 127L, 127L, 126L, 254L, 127L, 127L, 255L, 126L, 127L, 126L, 126L, 255L, 127L, 126L, 126L, 126L, 127L, 126L, 125L, 126L, 125L, 255L, 254L, 255L, 253L, 254L, 254L, 253L, 253L, 253L, 254L, 254L, 254L, 254L, 254L, 255L, 126L, 125L, 126L, 126L, 127L, 126L, 125L, 126L, 126L, 126L, 255L, 127L, 125L, 126L, 126L, 254L, 253L]})
            self.aList.append({'ssrc': 2122284415, 'version': 254, 'sequence': 32638, 'timestamp': 2130673407, 'payload_length': 68, 'type': 254, 'payload': [127L, 126L, 126L, 126L, 125L, 127L, 126L, 254L, 127L, 127L, 126L, 126L, 126L, 255L, 127L, 127L, 254L, 254L, 255L, 255L, 254L, 254L, 254L, 254L, 127L, 254L, 254L, 254L, 253L, 254L, 253L, 255L, 255L, 125L, 127L, 255L, 255L, 127L, 254L, 127L, 255L, 254L, 255L, 254L, 127L, 255L, 255L, 254L, 254L, 126L, 126L, 126L, 126L, 125L, 127L, 126L, 126L, 254L, 126L, 255L, 127L, 254L, 126L, 126L, 126L, 127L, 127L, 254L]})
            self.aList.append({'ssrc': 1516526686, 'version': 226, 'sequence': 31458, 'timestamp': 1751671414, 'payload_length': 68, 'type': 247, 'payload': [90L, 90L, 94L, 100L, 216L, 205L, 233L, 208L, 207L, 237L, 237L, 236L, 229L, 237L, 253L, 235L, 122L, 93L, 102L, 104L, 96L, 109L, 219L, 226L, 122L, 221L, 242L, 108L, 106L, 109L, 105L, 94L, 91L, 100L, 87L, 83L, 93L, 94L, 100L, 210L, 205L, 239L, 205L, 211L, 234L, 235L, 235L, 234L, 248L, 111L, 236L, 108L, 94L, 101L, 107L, 95L, 127L, 219L, 227L, 250L, 221L, 249L, 101L, 108L, 107L, 101L, 93L, 90L]})
            self.aList.append({'ssrc': 1919644284, 'version': 237, 'sequence': 62952, 'timestamp': 1870525430, 'payload_length': 68, 'type': 233, 'payload': [111L, 108L, 111L, 110L, 106L, 110L, 108L, 105L, 109L, 106L, 108L, 120L, 110L, 120L, 229L, 242L, 242L, 217L, 231L, 234L, 219L, 228L, 240L, 225L, 243L, 126L, 249L, 119L, 107L, 122L, 104L, 109L, 112L, 108L, 111L, 119L, 107L, 112L, 106L, 106L, 105L, 103L, 102L, 114L, 106L, 242L, 240L, 236L, 229L, 251L, 213L, 243L, 237L, 217L, 239L, 241L, 227L, 126L, 232L, 104L, 250L, 248L, 93L, 248L, 118L, 95L, 248L, 105L]})
            self.aList.append({'ssrc': 4042816375L, 'version': 123, 'sequence': 26725, 'timestamp': 2130114934, 'payload_length': 68, 'type': 109, 'payload': [241L, 254L, 115L, 116L, 122L, 252L, 252L, 126L, 122L, 122L, 253L, 245L, 246L, 253L, 121L, 120L, 255L, 249L, 251L, 125L, 121L, 120L, 124L, 126L, 253L, 125L, 121L, 116L, 122L, 252L, 245L, 247L, 251L, 255L, 250L, 247L, 244L, 250L, 255L, 123L, 124L, 124L, 127L, 123L, 122L, 119L, 124L, 253L, 250L, 255L, 123L, 120L, 122L, 124L, 125L, 124L, 123L, 122L, 125L, 254L, 249L, 246L, 247L, 246L, 245L, 242L, 242L, 243L]})
            self.aList.append({'ssrc': 1852796268, 'version': 253, 'sequence': 26483, 'timestamp': 1735026792, 'payload_length': 68, 'type': 110, 'payload': [109L, 108L, 105L, 103L, 106L, 106L, 108L, 120L, 121L, 245L, 230L, 236L, 221L, 222L, 223L, 220L, 222L, 226L, 232L, 237L, 254L, 123L, 108L, 111L, 102L, 104L, 108L, 102L, 109L, 110L, 112L, 114L, 115L, 110L, 114L, 103L, 106L, 107L, 104L, 111L, 117L, 123L, 242L, 232L, 235L, 221L, 224L, 221L, 221L, 224L, 228L, 231L, 246L, 251L, 121L, 105L, 111L, 107L, 101L, 106L, 115L, 101L, 119L, 114L, 111L, 118L, 111L, 110L]})
            self.aList.append({'ssrc': 1776447724, 'version': 245, 'sequence': 61801, 'timestamp': 2130048882, 'payload_length': 68, 'type': 126, 'payload': [250L, 231L, 103L, 248L, 248L, 106L, 244L, 126L, 108L, 238L, 125L, 103L, 239L, 101L, 249L, 120L, 113L, 250L, 242L, 247L, 251L, 253L, 248L, 244L, 121L, 237L, 253L, 240L, 125L, 242L, 251L, 238L, 121L, 250L, 248L, 127L, 250L, 251L, 242L, 111L, 236L, 113L, 102L, 239L, 101L, 111L, 234L, 108L, 245L, 121L, 104L, 232L, 120L, 98L, 241L, 120L, 252L, 126L, 109L, 254L, 240L, 120L, 254L, 253L, 120L, 225L, 113L, 254L]})
            self.aList.append({'ssrc': 1617390704, 'version': 93, 'sequence': 31854, 'timestamp': 2013264375, 'payload_length': 68, 'type': 100, 'payload': [94L, 93L, 100L, 113L, 238L, 224L, 219L, 217L, 218L, 220L, 221L, 223L, 227L, 235L, 249L, 111L, 100L, 95L, 94L, 99L, 108L, 119L, 252L, 255L, 123L, 114L, 108L, 105L, 100L, 96L, 95L, 96L, 106L, 122L, 234L, 223L, 219L, 218L, 219L, 221L, 223L, 226L, 229L, 235L, 247L, 113L, 102L, 96L, 96L, 100L, 110L, 124L, 247L, 246L, 253L, 122L, 111L, 108L, 102L, 97L, 95L, 93L, 98L, 107L, 250L, 231L, 223L, 219L]})
            self.aList.append({'ssrc': 1945992829, 'version': 247, 'sequence': 32253, 'timestamp': 4235721983L, 'payload_length': 68, 'type': 125, 'payload': [124L, 252L, 116L, 125L, 126L, 253L, 251L, 126L, 127L, 252L, 125L, 126L, 123L, 249L, 252L, 252L, 126L, 253L, 251L, 254L, 253L, 125L, 255L, 246L, 120L, 125L, 254L, 127L, 252L, 126L, 252L, 255L, 253L, 124L, 126L, 126L, 254L, 124L, 253L, 125L, 251L, 122L, 252L, 127L, 253L, 126L, 123L, 253L, 127L, 252L, 126L, 251L, 253L, 250L, 123L, 254L, 123L, 252L, 252L, 126L, 255L, 120L, 122L, 126L, 126L, 125L, 253L, 126L]})
            self.aList.append({'ssrc': 2097053309, 'version': 123, 'sequence': 61296, 'timestamp': 4134991217L, 'payload_length': 68, 'type': 244, 'payload': [254L, 126L, 124L, 253L, 255L, 121L, 253L, 120L, 246L, 118L, 247L, 122L, 249L, 122L, 253L, 253L, 251L, 125L, 252L, 252L, 125L, 252L, 120L, 251L, 127L, 123L, 127L, 251L, 126L, 125L, 254L, 121L, 246L, 116L, 248L, 121L, 249L, 123L, 127L, 254L, 125L, 254L, 123L, 249L, 125L, 252L, 122L, 250L, 127L, 253L, 124L, 249L, 125L, 252L, 124L, 253L, 252L, 125L, 125L, 254L, 254L, 127L, 122L, 126L, 253L, 126L, 253L, 120L]})
            self.aList.append({'ssrc': 4269109084L, 'version': 95, 'sequence': 22871, 'timestamp': 1650087771, 'payload_length': 68, 'type': 99, 'payload': [229L, 234L, 218L, 224L, 216L, 220L, 219L, 219L, 226L, 230L, 231L, 120L, 252L, 104L, 104L, 94L, 93L, 91L, 87L, 91L, 86L, 92L, 87L, 100L, 94L, 101L, 239L, 104L, 227L, 233L, 229L, 219L, 220L, 217L, 219L, 213L, 222L, 218L, 223L, 238L, 229L, 114L, 126L, 108L, 106L, 99L, 103L, 101L, 94L, 116L, 94L, 109L, 114L, 109L, 236L, 247L, 229L, 226L, 221L, 220L, 218L, 218L, 220L, 221L, 227L, 231L, 249L, 241L]})
            self.aList.append({'ssrc': 2147416828, 'version': 123, 'sequence': 63994, 'timestamp': 4244174589L, 'payload_length': 68, 'type': 124, 'payload': [246L, 251L, 124L, 241L, 253L, 247L, 239L, 242L, 235L, 237L, 235L, 235L, 238L, 236L, 234L, 240L, 239L, 246L, 123L, 109L, 113L, 116L, 113L, 244L, 233L, 223L, 216L, 212L, 214L, 217L, 224L, 239L, 103L, 90L, 85L, 77L, 75L, 75L, 75L, 78L, 85L, 96L, 115L, 248L, 223L, 223L, 217L, 212L, 214L, 214L, 220L, 222L, 233L, 242L, 122L, 108L, 104L, 100L, 98L, 97L, 102L, 254L, 246L, 239L, 229L, 237L, 237L, 114L]})
            self.aList.append({'ssrc': 4235193449L, 'version': 241, 'sequence': 28140, 'timestamp': 3983704053L, 'payload_length': 68, 'type': 110, 'payload': [247L, 110L, 235L, 108L, 243L, 255L, 115L, 237L, 108L, 238L, 117L, 123L, 240L, 109L, 238L, 110L, 240L, 113L, 247L, 126L, 123L, 248L, 121L, 250L, 124L, 255L, 247L, 116L, 240L, 118L, 249L, 250L, 118L, 239L, 111L, 243L, 254L, 117L, 239L, 110L, 242L, 118L, 254L, 247L, 111L, 239L, 114L, 253L, 244L, 109L, 235L, 107L, 238L, 120L, 114L, 233L, 103L, 237L, 122L, 115L, 238L, 109L, 241L, 119L, 125L, 243L, 108L, 235L]})
            self.aList.append({'ssrc': 3908499427L, 'version': 100, 'sequence': 25186, 'timestamp': 4177000041L, 'payload_length': 68, 'type': 96, 'payload': [249L, 253L, 114L, 102L, 101L, 93L, 94L, 91L, 89L, 102L, 122L, 252L, 230L, 217L, 223L, 221L, 214L, 219L, 221L, 222L, 236L, 253L, 113L, 108L, 97L, 92L, 95L, 98L, 100L, 123L, 242L, 251L, 241L, 238L, 239L, 236L, 236L, 247L, 117L, 111L, 108L, 101L, 98L, 97L, 95L, 100L, 120L, 246L, 242L, 228L, 224L, 230L, 221L, 219L, 223L, 225L, 233L, 243L, 254L, 110L, 104L, 95L, 95L, 100L, 103L, 111L, 125L, 122L]})
            self.aList.append({'ssrc': 4278124287L, 'version': 127, 'sequence': 32383, 'timestamp': 4278156926L, 'payload_length': 68, 'type': 126, 'payload': [254L, 254L, 127L, 126L, 126L, 125L, 125L, 126L, 126L, 126L, 127L, 127L, 255L, 255L, 126L, 254L, 255L, 255L, 127L, 127L, 127L, 126L, 255L, 126L, 254L, 255L, 255L, 254L, 127L, 254L, 254L, 254L, 255L, 254L, 255L, 255L, 254L, 254L, 254L, 255L, 254L, 254L, 254L, 254L, 254L, 127L, 126L, 126L, 126L, 255L, 255L, 254L, 126L, 255L, 126L, 126L, 127L, 127L, 254L, 126L, 126L, 126L, 126L, 127L, 254L, 255L, 126L, 126L]})
            self.aList.append({'ssrc': 4286577919L, 'version': 126, 'sequence': 32383, 'timestamp': 4278123646L, 'payload_length': 68, 'type': 254, 'payload': [126L, 125L, 253L, 125L, 252L, 125L, 254L, 253L, 127L, 127L, 126L, 125L, 125L, 126L, 122L, 255L, 126L, 254L, 247L, 227L, 232L, 93L, 249L, 117L, 102L, 241L, 228L, 242L, 96L, 233L, 106L, 95L, 120L, 237L, 105L, 122L, 234L, 240L, 108L, 237L, 235L, 112L, 252L, 239L, 248L, 109L, 247L, 239L, 106L, 125L, 241L, 116L, 117L, 248L, 123L, 118L, 117L, 241L, 125L, 122L, 237L, 253L, 241L, 234L, 115L, 240L, 112L, 109L]})
            self.aList.append({'ssrc': 1971125242, 'version': 253, 'sequence': 64251, 'timestamp': 2097085175, 'payload_length': 68, 'type': 252, 'payload': [113L, 121L, 125L, 254L, 252L, 254L, 252L, 252L, 250L, 252L, 252L, 125L, 251L, 125L, 252L, 121L, 124L, 125L, 254L, 255L, 123L, 123L, 125L, 125L, 254L, 252L, 251L, 250L, 126L, 254L, 254L, 252L, 126L, 123L, 121L, 124L, 125L, 124L, 254L, 251L, 251L, 252L, 252L, 254L, 254L, 254L, 254L, 126L, 125L, 127L, 124L, 126L, 253L, 252L, 254L, 126L, 124L, 126L, 126L, 252L, 126L, 127L, 254L, 127L, 254L, 254L, 251L, 127L]})
            self.aList.append({'ssrc': 4193348989L, 'version': 91, 'sequence': 28527, 'timestamp': 1633838952, 'payload_length': 68, 'type': 91, 'payload': [221L, 207L, 222L, 113L, 94L, 94L, 123L, 225L, 207L, 204L, 201L, 192L, 191L, 188L, 188L, 190L, 194L, 207L, 254L, 79L, 69L, 79L, 83L, 250L, 222L, 232L, 234L, 91L, 79L, 72L, 74L, 78L, 88L, 118L, 107L, 91L, 94L, 88L, 88L, 75L, 77L, 85L, 90L, 98L, 88L, 102L, 115L, 113L, 235L, 246L, 236L, 225L, 226L, 219L, 244L, 109L, 124L, 120L, 250L, 247L, 232L, 222L, 221L, 203L, 212L, 217L, 209L, 221L]})
            self.aList.append({'ssrc': 2105179253, 'version': 121, 'sequence': 30328, 'timestamp': 2071099766, 'payload_length': 68, 'type': 121, 'payload': [125L, 251L, 123L, 248L, 126L, 247L, 254L, 249L, 255L, 248L, 254L, 249L, 127L, 249L, 254L, 126L, 126L, 127L, 124L, 254L, 123L, 126L, 122L, 125L, 123L, 125L, 124L, 127L, 124L, 253L, 126L, 126L, 252L, 123L, 251L, 126L, 253L, 255L, 254L, 126L, 254L, 252L, 127L, 253L, 254L, 255L, 252L, 125L, 252L, 254L, 255L, 127L, 125L, 255L, 255L, 125L, 250L, 122L, 249L, 125L, 254L, 127L, 253L, 124L, 254L, 125L, 255L, 254L]})
            self.aList.append({'ssrc': 2130640767, 'version': 126, 'sequence': 32382, 'timestamp': 4269702783L, 'payload_length': 68, 'type': 126, 'payload': [254L, 255L, 126L, 255L, 126L, 254L, 255L, 254L, 126L, 254L, 254L, 254L, 255L, 254L, 254L, 127L, 254L, 254L, 255L, 254L, 255L, 254L, 253L, 253L, 254L, 127L, 126L, 127L, 127L, 126L, 126L, 125L, 255L, 127L, 254L, 126L, 254L, 255L, 254L, 127L, 126L, 255L, 126L, 127L, 126L, 127L, 127L, 126L, 126L, 255L, 127L, 126L, 254L, 126L, 126L, 126L, 126L, 126L, 127L, 254L, 255L, 254L, 255L, 253L, 253L, 254L, 252L, 254L]})
            self.aList.append({'ssrc': 4084824040L, 'version': 110, 'sequence': 62840, 'timestamp': 4059823093L, 'payload_length': 68, 'type': 112, 'payload': [249L, 243L, 105L, 107L, 104L, 96L, 101L, 95L, 100L, 102L, 101L, 113L, 110L, 124L, 223L, 217L, 218L, 232L, 230L, 222L, 230L, 242L, 245L, 237L, 248L, 109L, 109L, 117L, 115L, 106L, 106L, 117L, 253L, 252L, 253L, 242L, 243L, 125L, 120L, 251L, 244L, 247L, 125L, 124L, 117L, 106L, 105L, 105L, 107L, 106L, 105L, 111L, 115L, 117L, 123L, 251L, 250L, 254L, 240L, 224L, 220L, 230L, 238L, 234L, 232L, 244L, 118L, 248L]})
            self.aList.append({'ssrc': 1314282078, 'version': 104, 'sequence': 55653, 'timestamp': 2045569513, 'payload_length': 68, 'type': 239, 'payload': [85L, 88L, 126L, 108L, 215L, 210L, 216L, 199L, 215L, 206L, 216L, 231L, 255L, 98L, 93L, 82L, 93L, 91L, 90L, 236L, 109L, 223L, 225L, 227L, 234L, 127L, 107L, 88L, 88L, 80L, 82L, 85L, 112L, 103L, 228L, 207L, 221L, 202L, 206L, 207L, 215L, 219L, 246L, 102L, 101L, 85L, 88L, 97L, 85L, 254L, 122L, 247L, 219L, 230L, 233L, 242L, 111L, 92L, 89L, 85L, 80L, 86L, 109L, 101L, 238L, 208L, 222L, 205L]})
            self.aList.append({'ssrc': 2080308859, 'version': 124, 'sequence': 63613, 'timestamp': 2080111476, 'payload_length': 68, 'type': 120, 'payload': [251L, 125L, 239L, 111L, 248L, 254L, 117L, 244L, 127L, 254L, 119L, 125L, 249L, 120L, 250L, 118L, 253L, 246L, 111L, 244L, 118L, 255L, 248L, 117L, 244L, 112L, 246L, 117L, 255L, 251L, 125L, 247L, 126L, 252L, 251L, 121L, 249L, 252L, 124L, 250L, 125L, 245L, 252L, 123L, 254L, 126L, 249L, 119L, 255L, 251L, 254L, 126L, 255L, 254L, 125L, 122L, 254L, 127L, 247L, 121L, 126L, 254L, 255L, 124L, 254L, 117L, 249L, 123L]})
            self.aList.append({'ssrc': 4286578302L, 'version': 255, 'sequence': 65535, 'timestamp': 2122285055, 'payload_length': 68, 'type': 255, 'payload': [127L, 255L, 255L, 255L, 255L, 255L, 126L, 127L, 255L, 126L, 254L, 126L, 127L, 127L, 127L, 126L, 255L, 127L, 255L, 254L, 254L, 254L, 127L, 126L, 126L, 126L, 127L, 254L, 255L, 127L, 255L, 127L, 255L, 127L, 254L, 254L, 255L, 254L, 255L, 254L, 127L, 254L, 127L, 254L, 254L, 255L, 127L, 254L, 254L, 254L, 254L, 254L, 254L, 127L, 255L, 126L, 126L, 126L, 125L, 126L, 126L, 126L, 126L, 126L, 126L, 255L, 255L, 254L]})
            self.aList.append({'ssrc': 3496796395L, 'version': 228, 'sequence': 24315, 'timestamp': 1810529511, 'payload_length': 68, 'type': 223, 'payload': [227L, 228L, 221L, 254L, 219L, 125L, 93L, 220L, 96L, 124L, 235L, 115L, 245L, 83L, 98L, 95L, 95L, 119L, 115L, 221L, 218L, 119L, 221L, 119L, 94L, 238L, 107L, 223L, 226L, 234L, 223L, 126L, 110L, 109L, 111L, 237L, 238L, 91L, 121L, 223L, 117L, 111L, 110L, 113L, 110L, 110L, 239L, 112L, 108L, 240L, 115L, 111L, 127L, 109L, 120L, 229L, 237L, 104L, 231L, 125L, 250L, 116L, 91L, 124L, 114L, 219L, 245L, 87L]})
            self.aList.append({'ssrc': 1904082932, 'version': 107, 'sequence': 63867, 'timestamp': 4042190063L, 'payload_length': 68, 'type': 111, 'payload': [107L, 105L, 102L, 102L, 102L, 103L, 105L, 107L, 111L, 111L, 125L, 242L, 231L, 223L, 222L, 222L, 223L, 227L, 228L, 233L, 235L, 248L, 119L, 108L, 102L, 101L, 103L, 105L, 109L, 121L, 126L, 239L, 239L, 235L, 238L, 243L, 248L, 123L, 117L, 111L, 106L, 104L, 103L, 102L, 102L, 103L, 105L, 108L, 110L, 117L, 253L, 238L, 227L, 223L, 222L, 223L, 227L, 227L, 229L, 231L, 238L, 252L, 113L, 107L, 103L, 105L, 102L, 106L]})
            self.aList.append({'ssrc': 4261215358L, 'version': 246, 'sequence': 32510, 'timestamp': 2147417852, 'payload_length': 68, 'type': 122, 'payload': [253L, 255L, 126L, 126L, 255L, 254L, 127L, 126L, 255L, 252L, 123L, 253L, 126L, 124L, 254L, 124L, 254L, 127L, 254L, 126L, 254L, 126L, 253L, 125L, 254L, 127L, 126L, 124L, 124L, 125L, 124L, 125L, 255L, 124L, 251L, 254L, 250L, 254L, 246L, 126L, 254L, 252L, 125L, 255L, 123L, 126L, 122L, 248L, 226L, 247L, 107L, 123L, 111L, 127L, 114L, 252L, 117L, 252L, 125L, 251L, 127L, 245L, 252L, 249L, 253L, 248L, 122L, 253L]})
            self.aList.append({'ssrc': 1582914904, 'version': 250, 'sequence': 25703, 'timestamp': 1532910435, 'payload_length': 68, 'type': 252, 'payload': [94L, 111L, 111L, 240L, 221L, 233L, 207L, 220L, 206L, 213L, 208L, 217L, 214L, 230L, 226L, 239L, 107L, 111L, 97L, 90L, 99L, 84L, 93L, 89L, 88L, 91L, 91L, 90L, 98L, 96L, 255L, 105L, 221L, 244L, 216L, 217L, 217L, 210L, 216L, 215L, 220L, 222L, 240L, 233L, 110L, 111L, 101L, 101L, 91L, 105L, 86L, 98L, 91L, 91L, 94L, 90L, 93L, 94L, 108L, 104L, 248L, 231L, 239L, 213L, 226L, 210L, 217L, 214L]})
            self.aList.append({'ssrc': 1802332265, 'version': 232, 'sequence': 31727, 'timestamp': 1852338557, 'payload_length': 68, 'type': 232, 'payload': [105L, 109L, 109L, 105L, 112L, 107L, 106L, 114L, 108L, 113L, 124L, 250L, 251L, 231L, 233L, 230L, 222L, 228L, 224L, 226L, 229L, 236L, 237L, 252L, 119L, 121L, 105L, 108L, 108L, 103L, 108L, 107L, 110L, 108L, 118L, 111L, 111L, 255L, 106L, 122L, 113L, 117L, 119L, 124L, 241L, 124L, 227L, 242L, 231L, 225L, 241L, 222L, 243L, 228L, 245L, 246L, 247L, 110L, 255L, 104L, 116L, 103L, 108L, 108L, 104L, 114L, 104L, 114L]})
            self.aList.append({'ssrc': 1937341438, 'version': 234, 'sequence': 60140, 'timestamp': 4176736238L, 'payload_length': 68, 'type': 232, 'payload': [117L, 112L, 113L, 111L, 113L, 110L, 111L, 110L, 110L, 111L, 110L, 110L, 111L, 113L, 116L, 121L, 126L, 249L, 245L, 239L, 237L, 234L, 233L, 231L, 233L, 232L, 236L, 237L, 241L, 243L, 254L, 254L, 119L, 117L, 113L, 111L, 111L, 110L, 111L, 110L, 110L, 111L, 111L, 115L, 111L, 117L, 113L, 117L, 119L, 122L, 124L, 253L, 248L, 246L, 239L, 238L, 236L, 236L, 234L, 235L, 235L, 237L, 239L, 241L, 246L, 250L, 127L, 124L]})
            self.aList.append({'ssrc': 2122317695, 'version': 126, 'sequence': 32383, 'timestamp': 4269768318L, 'payload_length': 68, 'type': 254, 'payload': [126L, 125L, 125L, 126L, 124L, 125L, 126L, 255L, 254L, 254L, 254L, 254L, 253L, 254L, 254L, 255L, 253L, 254L, 254L, 254L, 254L, 254L, 253L, 127L, 254L, 255L, 126L, 254L, 126L, 125L, 255L, 125L, 255L, 126L, 126L, 126L, 255L, 127L, 126L, 255L, 126L, 254L, 255L, 126L, 254L, 127L, 254L, 255L, 254L, 254L, 254L, 255L, 254L, 127L, 126L, 126L, 125L, 125L, 125L, 126L, 126L, 126L, 127L, 127L, 255L, 254L, 254L, 127L]})
            self.aList.append({'ssrc': 4269765997L, 'version': 251, 'sequence': 26987, 'timestamp': 1801938275, 'payload_length': 68, 'type': 112, 'payload': [248L, 245L, 248L, 249L, 127L, 124L, 118L, 113L, 111L, 108L, 111L, 109L, 113L, 125L, 122L, 244L, 237L, 238L, 232L, 233L, 232L, 233L, 235L, 237L, 245L, 249L, 254L, 117L, 118L, 113L, 110L, 111L, 112L, 113L, 117L, 120L, 124L, 122L, 255L, 253L, 254L, 253L, 254L, 127L, 124L, 121L, 122L, 120L, 120L, 121L, 121L, 124L, 126L, 254L, 249L, 247L, 242L, 241L, 240L, 240L, 241L, 244L, 247L, 247L, 252L, 254L, 124L, 122L]})
            self.aList.append({'ssrc': 3991567715L, 'version': 108, 'sequence': 24154, 'timestamp': 1599953751, 'payload_length': 68, 'type': 93, 'payload': [210L, 217L, 212L, 206L, 218L, 210L, 223L, 221L, 238L, 239L, 117L, 96L, 111L, 83L, 93L, 89L, 81L, 92L, 85L, 89L, 87L, 95L, 90L, 252L, 114L, 231L, 216L, 228L, 207L, 221L, 212L, 220L, 222L, 227L, 242L, 236L, 105L, 107L, 102L, 90L, 99L, 90L, 95L, 89L, 95L, 91L, 90L, 100L, 95L, 239L, 116L, 219L, 219L, 219L, 205L, 222L, 207L, 218L, 221L, 221L, 246L, 231L, 101L, 110L, 107L, 84L, 121L, 84L]})
            self.aList.append({'ssrc': 1852009825, 'version': 250, 'sequence': 27878, 'timestamp': 1886674294, 'payload_length': 68, 'type': 239, 'payload': [95L, 96L, 103L, 106L, 104L, 97L, 114L, 251L, 214L, 213L, 222L, 207L, 214L, 212L, 227L, 112L, 225L, 102L, 109L, 90L, 97L, 114L, 94L, 102L, 112L, 240L, 220L, 230L, 234L, 234L, 243L, 110L, 102L, 93L, 106L, 99L, 104L, 101L, 98L, 102L, 94L, 102L, 100L, 98L, 104L, 109L, 219L, 206L, 221L, 212L, 211L, 214L, 217L, 110L, 223L, 247L, 120L, 98L, 94L, 117L, 103L, 94L, 104L, 110L, 236L, 246L, 216L, 227L]})
            self.aList.append({'ssrc': 2087417190, 'version': 229, 'sequence': 31101, 'timestamp': 1617519977, 'payload_length': 68, 'type': 224, 'payload': [236L, 121L, 238L, 241L, 118L, 108L, 106L, 96L, 92L, 92L, 94L, 91L, 104L, 240L, 253L, 238L, 207L, 228L, 216L, 208L, 223L, 219L, 222L, 244L, 248L, 110L, 106L, 97L, 100L, 100L, 102L, 114L, 109L, 244L, 255L, 243L, 249L, 246L, 107L, 111L, 106L, 94L, 95L, 97L, 89L, 104L, 123L, 110L, 243L, 217L, 230L, 219L, 209L, 222L, 217L, 217L, 233L, 235L, 247L, 109L, 106L, 101L, 99L, 95L, 105L, 101L, 112L, 116L]})
            self.aList.append({'ssrc': 4067880408L, 'version': 209, 'sequence': 51673, 'timestamp': 3721646042L, 'payload_length': 68, 'type': 216, 'payload': [86L, 102L, 89L, 82L, 93L, 84L, 84L, 93L, 83L, 93L, 91L, 94L, 122L, 239L, 244L, 212L, 214L, 217L, 203L, 214L, 211L, 209L, 220L, 223L, 224L, 108L, 252L, 95L, 90L, 94L, 85L, 89L, 92L, 84L, 93L, 89L, 90L, 94L, 94L, 106L, 237L, 126L, 220L, 209L, 230L, 202L, 216L, 212L, 209L, 221L, 220L, 225L, 118L, 252L, 96L, 94L, 93L, 88L, 89L, 92L, 86L, 92L, 90L, 90L, 91L, 96L, 95L, 242L]})
            self.aList.append({'ssrc': 3738950099L, 'version': 111, 'sequence': 57848, 'timestamp': 3671579110L, 'payload_length': 68, 'type': 114, 'payload': [234L, 242L, 115L, 108L, 100L, 95L, 100L, 92L, 102L, 99L, 101L, 121L, 105L, 125L, 127L, 116L, 252L, 114L, 111L, 108L, 104L, 101L, 97L, 98L, 96L, 97L, 107L, 110L, 126L, 234L, 226L, 223L, 215L, 216L, 215L, 212L, 218L, 221L, 223L, 238L, 253L, 119L, 104L, 102L, 105L, 95L, 109L, 103L, 106L, 126L, 109L, 243L, 127L, 249L, 243L, 125L, 251L, 118L, 111L, 110L, 101L, 102L, 97L, 99L, 103L, 106L, 126L, 252L]})
            self.aList.append({'ssrc': 1701014395, 'version': 225, 'sequence': 57562, 'timestamp': 4024953822L, 'payload_length': 68, 'type': 224, 'payload': [102L, 106L, 111L, 120L, 250L, 253L, 244L, 126L, 245L, 254L, 246L, 123L, 121L, 110L, 103L, 96L, 93L, 94L, 95L, 102L, 120L, 235L, 230L, 227L, 226L, 221L, 219L, 223L, 224L, 231L, 227L, 241L, 122L, 107L, 104L, 105L, 103L, 108L, 109L, 127L, 249L, 248L, 247L, 253L, 239L, 245L, 245L, 126L, 121L, 119L, 106L, 100L, 95L, 97L, 100L, 104L, 114L, 246L, 236L, 232L, 229L, 223L, 222L, 223L, 224L, 230L, 230L, 244L]})
            self.aList.append({'ssrc': 1851944549, 'version': 219, 'sequence': 64754, 'timestamp': 1684434415, 'payload_length': 68, 'type': 228, 'payload': [117L, 235L, 235L, 249L, 111L, 108L, 111L, 107L, 104L, 101L, 102L, 102L, 97L, 94L, 92L, 94L, 111L, 219L, 207L, 214L, 220L, 229L, 218L, 216L, 221L, 228L, 245L, 237L, 121L, 108L, 98L, 94L, 94L, 95L, 102L, 109L, 124L, 245L, 246L, 252L, 122L, 118L, 120L, 122L, 117L, 109L, 107L, 98L, 96L, 95L, 97L, 103L, 127L, 221L, 216L, 220L, 222L, 223L, 215L, 218L, 221L, 233L, 239L, 241L, 125L, 113L, 99L, 95L]})
            self.aList.append({'ssrc': 4285492073L, 'version': 247, 'sequence': 32250, 'timestamp': 1785687931, 'payload_length': 68, 'type': 241, 'payload': [254L, 124L, 112L, 103L, 106L, 109L, 253L, 238L, 237L, 239L, 125L, 113L, 109L, 111L, 255L, 237L, 232L, 232L, 242L, 253L, 125L, 123L, 244L, 240L, 235L, 237L, 246L, 252L, 118L, 114L, 111L, 110L, 121L, 125L, 252L, 252L, 123L, 119L, 110L, 108L, 109L, 113L, 254L, 245L, 238L, 238L, 248L, 115L, 109L, 111L, 122L, 241L, 239L, 234L, 238L, 244L, 245L, 251L, 247L, 253L, 124L, 251L, 245L, 235L, 236L, 127L, 107L, 98L]})
            self.aList.append({'ssrc': 4286118653L, 'version': 247, 'sequence': 30459, 'timestamp': 2122152177, 'payload_length': 68, 'type': 116, 'payload': [120L, 244L, 122L, 123L, 126L, 249L, 253L, 123L, 123L, 124L, 249L, 124L, 255L, 120L, 246L, 254L, 125L, 123L, 254L, 247L, 123L, 255L, 124L, 244L, 126L, 126L, 122L, 247L, 126L, 125L, 126L, 123L, 246L, 120L, 251L, 124L, 254L, 125L, 252L, 125L, 127L, 253L, 126L, 253L, 123L, 255L, 121L, 247L, 126L, 254L, 125L, 126L, 250L, 124L, 124L, 125L, 251L, 124L, 125L, 124L, 249L, 123L, 126L, 123L, 252L, 248L, 121L, 126L]})
            self.aList.append({'ssrc': 1701208929, 'version': 244, 'sequence': 27502, 'timestamp': 1600086882, 'payload_length': 68, 'type': 122, 'payload': [104L, 106L, 111L, 233L, 223L, 218L, 214L, 211L, 212L, 219L, 218L, 230L, 244L, 127L, 109L, 100L, 93L, 94L, 94L, 95L, 111L, 255L, 234L, 238L, 229L, 224L, 116L, 233L, 113L, 107L, 107L, 98L, 103L, 93L, 102L, 100L, 95L, 108L, 99L, 105L, 107L, 111L, 236L, 230L, 217L, 215L, 216L, 207L, 222L, 217L, 223L, 238L, 240L, 112L, 107L, 98L, 92L, 97L, 91L, 107L, 117L, 242L, 223L, 249L, 221L, 232L, 105L, 230L]})
            self.aList.append({'ssrc': 2130640894, 'version': 255, 'sequence': 32765, 'timestamp': 4278124286L, 'payload_length': 68, 'type': 254, 'payload': [126L, 126L, 126L, 125L, 126L, 124L, 126L, 126L, 127L, 125L, 127L, 127L, 255L, 255L, 127L, 126L, 126L, 127L, 127L, 127L, 255L, 254L, 255L, 127L, 127L, 127L, 127L, 127L, 255L, 254L, 255L, 255L, 254L, 254L, 254L, 254L, 254L, 254L, 255L, 126L, 126L, 126L, 126L, 254L, 255L, 255L, 126L, 255L, 254L, 253L, 255L, 254L, 255L, 254L, 255L, 126L, 126L, 255L, 127L, 255L, 255L, 127L, 255L, 126L, 127L, 125L, 254L, 127L]})
            self.aList.append({'ssrc': 1946058109, 'version': 238, 'sequence': 65526, 'timestamp': 4235523707L, 'payload_length': 68, 'type': 113, 'payload': [249L, 119L, 124L, 250L, 117L, 243L, 111L, 239L, 118L, 254L, 123L, 248L, 117L, 254L, 250L, 253L, 117L, 238L, 117L, 252L, 246L, 123L, 250L, 253L, 255L, 126L, 126L, 249L, 122L, 252L, 253L, 122L, 125L, 250L, 119L, 124L, 250L, 123L, 124L, 247L, 253L, 250L, 247L, 246L, 244L, 248L, 243L, 243L, 247L, 247L, 240L, 248L, 254L, 244L, 251L, 120L, 252L, 123L, 116L, 119L, 116L, 114L, 110L, 110L, 109L, 106L, 108L, 105L]})
            self.aList.append({'ssrc': 3687829212L, 'version': 103, 'sequence': 23902, 'timestamp': 2104256608, 'payload_length': 68, 'type': 99, 'payload': [233L, 249L, 237L, 253L, 110L, 109L, 115L, 247L, 244L, 119L, 112L, 112L, 124L, 246L, 234L, 240L, 252L, 124L, 121L, 122L, 111L, 106L, 105L, 108L, 102L, 95L, 92L, 94L, 103L, 105L, 105L, 250L, 216L, 205L, 211L, 222L, 239L, 237L, 235L, 121L, 104L, 105L, 118L, 242L, 252L, 116L, 111L, 127L, 245L, 238L, 236L, 252L, 252L, 121L, 123L, 114L, 108L, 108L, 108L, 108L, 102L, 94L, 93L, 97L, 103L, 105L, 111L, 229L]})
            self.aList.append({'ssrc': 4236017404L, 'version': 246, 'sequence': 31224, 'timestamp': 2122153979, 'payload_length': 68, 'type': 120, 'payload': [126L, 122L, 249L, 122L, 252L, 127L, 125L, 127L, 126L, 252L, 119L, 248L, 123L, 127L, 253L, 253L, 251L, 118L, 245L, 116L, 245L, 116L, 253L, 251L, 124L, 125L, 252L, 252L, 122L, 249L, 121L, 246L, 122L, 251L, 122L, 244L, 119L, 250L, 123L, 250L, 124L, 254L, 124L, 249L, 118L, 249L, 118L, 244L, 118L, 251L, 125L, 251L, 120L, 251L, 254L, 253L, 120L, 249L, 124L, 125L, 125L, 255L, 249L, 113L, 242L, 116L, 245L, 118L]})
            self.aList.append({'ssrc': 1667722093, 'version': 220, 'sequence': 56797, 'timestamp': 2062543331, 'payload_length': 68, 'type': 219, 'payload': [101L, 100L, 99L, 99L, 100L, 97L, 100L, 100L, 102L, 110L, 115L, 246L, 233L, 228L, 222L, 219L, 219L, 220L, 220L, 222L, 229L, 234L, 245L, 118L, 111L, 106L, 102L, 101L, 99L, 99L, 97L, 99L, 97L, 98L, 99L, 100L, 106L, 110L, 124L, 239L, 231L, 225L, 221L, 219L, 219L, 220L, 220L, 226L, 232L, 239L, 126L, 113L, 107L, 104L, 102L, 101L, 100L, 98L, 98L, 98L, 99L, 100L, 101L, 104L, 108L, 116L, 248L, 235L]})
            self.aList.append({'ssrc': 2122284927, 'version': 254, 'sequence': 32126, 'timestamp': 2138996093, 'payload_length': 68, 'type': 126, 'payload': [255L, 127L, 127L, 255L, 126L, 255L, 253L, 254L, 253L, 253L, 254L, 253L, 253L, 127L, 255L, 126L, 126L, 126L, 127L, 125L, 126L, 255L, 126L, 127L, 127L, 126L, 126L, 127L, 127L, 126L, 126L, 127L, 254L, 254L, 254L, 254L, 254L, 255L, 255L, 254L, 127L, 254L, 126L, 126L, 255L, 126L, 126L, 127L, 126L, 254L, 254L, 255L, 255L, 254L, 254L, 253L, 254L, 126L, 254L, 254L, 255L, 254L, 126L, 127L, 254L, 254L, 127L, 254L]})

        else:
            f = open(filename)
            for i in range(0, 120):
                udpdata = f.readline(80*(i+1))
    #             print udpdata +"\r\n" + str(i) + "\r\n"
                data = self.initunPackedRTPData(udpdata,80)
                print data
                self.aList.append(data)

    def RTPPacket(self, udpdata, length):
        self.version, = struct.unpack('B', udpdata[0])
        self.type, = struct.unpack('B', udpdata[1])
        self.sequence, = struct.unpack('<H', udpdata[2:4])
        self.timestamp, = struct.unpack('<I', udpdata[4:8])
        self.ssrc, = struct.unpack('<I', udpdata[8:12])
        self.payload_length = length - 12
        self.payload = array.array("I")
        
        if self.payload_length > 1500:
            self.payload_length = 1500
        for i in range(0, self.payload_length):
            payload_data, = struct.unpack('B', udpdata[12+i])
            self.payload.append(payload_data)

    def initunPackedRTPData(self, udpdata, length):
        self.version, = struct.unpack('B', udpdata[0])
        self.type, = struct.unpack('B', udpdata[1])
        self.sequence, = struct.unpack('<H', udpdata[2:4])
        self.timestamp, = struct.unpack('<I', udpdata[4:8])
        self.ssrc, = struct.unpack('<I', udpdata[8:12])
        self.payload_length = length - 12
        self.payload = array.array("I")
        if self.payload_length > 1500:
            self.payload_length = 1500
        for i in range(0, self.payload_length):
            payload_data, = struct.unpack('B', udpdata[12+i])
            self.payload.append(payload_data)
        aDict = dict(version = self.version,type = self.type,sequence = self.sequence,ssrc = self.ssrc,timestamp=self.timestamp,payload_length=self.payload_length,payload = self.payload)
        return aDict

    def initPackedRTPData(self, udpdata, length):
        version = struct.pack('B', udpdata['version'])
        payload_type = struct.pack('B', udpdata['type'])
        sequence = struct.pack('H', udpdata['sequence'])
        timestamp = struct.pack('I', udpdata['timestamp'])
        ssrc = struct.pack('I', udpdata['ssrc'])
        payload = ""
        for i in range(0, udpdata['payload_length']):
            payload += struct.pack('B', udpdata['payload'][i])

        packet = "".join([version, payload_type, sequence, timestamp, ssrc, payload])
        return packet
    def loopback(self):
        version = struct.pack('B', self.version)
        payload_type = struct.pack('B', self.type)
        sequence = struct.pack('H', self.sequence)
        timestamp = struct.pack('I', self.timestamp)
        ssrc = struct.pack('I', self.ssrc)
        payload = ""
        for i in range(0, self.payload_length):
            payload += struct.pack('B', self.payload[i])

        packet = "".join([version, payload_type, sequence, timestamp, ssrc, payload])
        return packet
    def run(self):
        global service_on
        global INVITE_SDP
        # Create a socket to receive rtp packets and send it back
        sendsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        local_port_num = self.rtp_port
        while service_on:
            try:
                sendsock.bind(('%s' % self.localip, int(local_port_num)))
            except:
                local_port_num += 1
                continue
            break
        sendsock.settimeout(1)
        addCaseLog("#######ipvideotalk_Media_Data thread is started on [%s:%d]"%(self.localip, self.localport))
        self.getUdpData()
        while service_on:
            if INVITE_SDP["ip"] == "NONE" or str(INVITE_SDP["port1"]) == "NONE" or INVITE_SDP["ip"] == "" or INVITE_SDP["port1"] == "" or INVITE_SDP["port1"] is None or INVITE_SDP["ip"] is None:
                continue
            break
#             else:
#                 break
        if self.destip == "":
            self.destip = INVITE_SDP["ip"]
        if self.destport == "":
            self.destport = INVITE_SDP["port1"]
        if service_on != 0:
            for i in range(0,len(self.aList)):
                sendsock.sendto(self.initPackedRTPData(self.aList[i],len(self.aList[i])), (self.destip,int(self.destport)))
                time.sleep(0.02)
                
        while service_on:
            try:
                data, rcvaddress = sendsock.recvfrom(1024)
            except:
                continue    
            #debug_print( "%d data is received\r\n"%len(data), self.verbose)
            if len(data) < 12:
                continue
            rcv_host, rcv_port = rcvaddress
            self.RTPPacket(data, len(data))
            try:
                sendsock.sendto(self.loopback(), rcvaddress)
            except Exception as e:
                print e

        sendsock.close()
        addCaseLog("media service is stopped, local address is [%s:%d], service_on = %s"%(self.localip, self.localport,service_on))

class Media_Service(sipServer_commonlib):
    def __init__(self, local_address, local_port):
        self.service_msg = create_sipObject()
        self.service_msg.local_ip_number = local_address
        self.service_msg.local_port_number = local_port
        sipServer_commonlib.__init__(self,self.service_msg)
    def RTPPacket(self, udpdata, length):
        self.version, = struct.unpack('B', udpdata[0])
        self.type, = struct.unpack('B', udpdata[1])
        self.sequence, = struct.unpack('<H', udpdata[2:4])
        self.timestamp, = struct.unpack('<I', udpdata[4:8])
        self.ssrc, = struct.unpack('<I', udpdata[8:12])
        self.payload_length = length - 12
        self.payload = array.array("I")
        if self.payload_length > 1500:
            self.payload_length = 1500
        for i in range(0, self.payload_length):
            payload_data, = struct.unpack('B', udpdata[12+i])
            self.payload.append(payload_data)
#         print self.version,self.type,self.timestamp,self.ssrc,self.payload
    def loopback(self):
        version = struct.pack('B', self.version)
        payload_type = struct.pack('B', self.type)
        sequence = struct.pack('H', self.sequence)
        timestamp = struct.pack('I', self.timestamp)
        ssrc = struct.pack('I', self.ssrc)
        payload = ""
        for i in range(0, self.payload_length):
            payload += struct.pack('B', self.payload[i])

        packet = "".join([version, payload_type, sequence, timestamp, ssrc, payload])
        return packet

    def run(self):
        global service_on
        # Create a socket to receive rtp packets and send it back
        sendsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        local_port_num = self.localport
        while service_on:
            try:
                sendsock.bind(('%s' % self.localip, int(local_port_num)))
            except:
                local_port_num += 1
                continue
            break
        sendsock.settimeout(1)
        addCaseLog("#######Media_Service thread is started on [%s:%d]"%(self.localip, self.localport))
        while service_on:
            try:
                data, rcvaddress = sendsock.recvfrom(1024)
            except:
                continue    
            if len(data) < 12:
                debug_print("bad rtp format", VERBOSE)
                continue
            rcv_host, rcv_port = rcvaddress
            self.RTPPacket(data, len(data))
            sendsock.sendto(self.loopback(), rcvaddress)
        sendsock.close()
        addCaseLog("media service is stopped, local address is [%s:%d], service_on = %s"%(self.localip, self.localport,service_on))

def set_UserPassed_Global_Param():
    global LOCAL_PC_IP,LOCAL_PC_PORT,SIP_SERVER_IP,SIP_SERVER_PORT,caller_id,rtp_port,meeting_pw,MEETINNG_ROOM_ID
    global VERBOSE,hangup,insist,has_media
 
    parser = OptionParser()
    parser.add_option('-d', '--destaddress', action="store", dest="SIP_SERVER_IP", help="dest ip address")
    parser.add_option('-r', '--destport', action="store", dest="SIP_SERVER_PORT", help="dest port")
    parser.add_option('-l', '--localip', action="store", dest="local_ip", help="local ip address")
    parser.add_option('-p', '--localport', action="store", dest="LOCAL_PC_PORT", help="local port number")
    parser.add_option('-c', '--callerID', action="store", dest="caller_id", help="local phone number")
    parser.add_option('-u', '--conferenceID', action="store", dest="conf_id", help="conference number")
    parser.add_option('-R', '--localRtpPort', action="store", dest="rtp_port", help="local rtp port")
    #-S: set the interval of invite send time 
    #-m: set the interval of message send time 
    #-U: if set -U, will use UDP , not set , will use TCP
    #-I: set the invterval of every user join
    parser.add_option("-P", "--meetingpassword", action="store", dest="meeting_pw", default=False, help="meeting password")
    parser.add_option("-a", "--exceptiontest of status code", action="store", dest="WEBAPI_KEY_URL", default=False, help="web api key url:/user/login")
    (options, args) = parser.parse_args()
    
    print """
      '__'
      (oo)
      (__)````````)\\
    ||-----||  *
    """
    global WEBAPI_KEY_URL,MEETING_PASSWORD,MEETINNG_ROOM_ID
    if not options.local_ip:
        addCaseLog("your localIP is empty , start to get your local IP address...")
        LOCAL_PC_IP = get_ip_address()
    else:
        LOCAL_PC_IP = options.local_ip
    
    if options.LOCAL_PC_PORT:
        LOCAL_PC_PORT = int(options.LOCAL_PC_PORT)
    if options.SIP_SERVER_IP:
        SIP_SERVER_IP = options.SIP_SERVER_IP
    if options.SIP_SERVER_PORT:
        SIP_SERVER_PORT = int(options.SIP_SERVER_PORT)
    if options.caller_id:
        SIP_ID_NUMBER = options.caller_id
    if options.conf_id:
        MEETINNG_ROOM_ID = int(options.conf_id)
    if options.rtp_port:
        LOCAL_PC_RTP_PORT = int(options.rtp_port)
    if options.meeting_pw:
        MEETING_PASSWORD = options.meeting_pw

    if options.WEBAPI_KEY_URL:
        WEBAPI_KEY_URL = options.WEBAPI_KEY_URL

def myhandle(n=0,e=0):
    global service_on
    service_on = 0
    print "close sip server"

# class TestCaseManager:
#     def __init__(self,case_ErrorCount, case_TotalCount, case_html_text):
#         self.mPrintBody = case_html_text
#         self.mPrintBody += "<table>"
#         self.mPrintBody += "<tr>"
#         self.mPrintBody += "<th>Author</th>"
#         self.mPrintBody += "<th>ModuleID</th>"
#         self.mPrintBody += "<th>CaseID</th>"
#         self.mPrintBody += "<th>TestResult</th>"
#         self.mPrintBody += "<th>Log</th>"
#         self.mPrintBody += "</tr>"
#         self.mErrorCount = case_ErrorCount
#         self.mTotalCount = case_TotalCount
#         pass
# 
#     def reportCaseResult(self,author,moduleID,caseID,caseResult,caseLog):
#         self.mPrintBody += "<tr>"
#         self.mPrintBody += "<td> %s </td>" %(author)
#         self.mPrintBody += "<td> %s </td>" %(moduleID)
#         self.mPrintBody += "<td> %s </td>" %(caseID)
# 
# #         if caseResult == 1:
#         if str(caseResult).lower() == "pass":
#             self.mPrintBody += "<td> Pass </td>"
#         else:
#             self.mPrintBody += "<td> <font color=red>Failed</font></td>"
#             self.mErrorCount += 1
#         self.mPrintBody += "<td> %s </td>" %(caseLog)
#         self.mPrintBody += "</tr>"
#         self.mTotalCount += 1
#         pass
# 
#     def printHtml(self):
#         self.mPrintBody += "</table>"
#         self.mPrintBody = "<h2> Total test case: %d , failed case: %d, pass %f</h2>" %(self.mTotalCount, self.mErrorCount, self.mErrorCount * 1.0/self.mTotalCount) + self.mPrintBody
#         print self.mPrintBody
#         pass

class Xserver_info_sender():
    def __init__(self, udpdata, length):
        self.role = "host"
        pass
    
    def info(self,uid,action="",conf_id="",status="",value="1",param = "",target_user="",accept="1"):
        
        if self.role == "host":
            time.sleep(1)
            addCaseLog("uid=%s;action=set_host;conf-id=%s"%(uid,action,conf_id)) #uid is the role dest
            time.sleep(1)
            addCaseLog("uid=%s;action=mute;conf-id=%s;mute-status=1"%(uid, conf_id))
            time.sleep(1)
            addCaseLog("uid=%s;action=mute;conf-id=%s;mute-status=0"%(uid, conf_id))
            time.sleep(1)
            addCaseLog("uid=%s;action=mic;conf-id=%s;mic-status=1"%(uid, conf_id))
            time.sleep(1)
            addCaseLog("uid=%s;action=mic;conf-id=%s;mic-status=0"%(uid, conf_id))
            time.sleep(1)
            addCaseLog("uid=%s;action=mute_user;conf-id=%s;mute-status=1"%(uid, conf_id))
            time.sleep(1)
            addCaseLog("uid=%s;action=mute_user;conf-id=%s;mute-status=0"%(uid,conf_id))
            time.sleep(1)
            addCaseLog("uid=%s;action=set_presenter;conf-id=%s"%(uid, conf_id))
            time.sleep(1)
            #Host invite user- call back
            addCaseLog("uid=%s;action=invite;conf-id=%s"%(uid, conf_id))
            time.sleep(1)
            addCaseLog("uid=none;action=conf_config;conf-id=%s;param=mute-status;value=0"%(conf_id))
            addCaseLog("uid=none;action=conf_config;conf-id=%s;param=mute-status;value=1"%(conf_id))
            addCaseLog("uid=none;action=conf_config;conf-id=%s;param=leave-prompt;value=0"%(conf_id))
            addCaseLog("uid=none;action=conf_config;conf-id=%s;param=leave-prompt;value=1"%(conf_id))
            addCaseLog("uid=none;action=conf_config;conf-id=%s;param=join-prompt;value=0"%(conf_id))
            addCaseLog("uid=none;action=conf_config;conf-id=%s;param=join-prompt;value=1"%(conf_id))
            addCaseLog("uid=all;action=set_userlist_enable;conf-id=%s;enable=1"%(conf_id))
            addCaseLog("uid=all;action=set_userlist_enable;conf-id=%s;enable=0"%(conf_id))
            # conf locked, host accept user join
            addCaseLog("uid=%s;action=join_confirm;conf-id=%s;accept=1"%(target_user, conf_id))
            addCaseLog("uid=%s;action=join_confirm;conf-id=%s;accept=0"%(target_user, conf_id))
            # conf setting - userlist
            addCaseLog("uid=%s;action=userlist_enable_request;conf-id=%s"%(uid,conf_id))
            addCaseLog("uid=%s;action=userlist_enable_confirm;conf-id=%s;accept=0"%(uid, conf_id))
            # host transfer mic to target user
            addCaseLog("uid=%s;action=mic_transfer;conf-id=%s;target=%s"%(uid, conf_id, target_user))
            # user request mic ,host decline
            addCaseLog("uid=%s;action=mic_confirm;conf-id=%s;choice=0;mic-user=none"%(uid, conf_id))
            # user request mic ,host accepet(meeting have free mic)
            addCaseLog("uid=%s;action=mic_confirm;conf-id=%s;choice=1;mic-user=none"%(uid, conf_id))
            # user request mic ,host transfer targe user's mic
            addCaseLog("uid=%s;action=mic_confirm;conf-id=%s;choice=2;mic-user=%s"%(uid, conf_id, target_user))
            # desktop : set mouse control privilege
            addCaseLog("uid=%s;action=desktop;conf-id=%s;status==1"%(uid, conf_id))
            # desktop : revoke mouse control privilege
            addCaseLog("uid=%s;action=desktop;conf-id=%s;status==0"%(uid, conf_id))
            addCaseLog("uid=all;action=whiteboard;conf-id=%s;status==0"%(conf_id))
            # desktop: request to control presenter
            addCaseLog("uid=%s;action=desktop_request;conf-id=%s"%(uid, conf_id))
             
            addCaseLog("uid=%s;action=whiteboard_request;conf-id=%s"%(uid, conf_id))
            addCaseLog("uid=%s;action=whiteboard_confirm;conf-id=%s;accept=0"%(uid, conf_id))
            time.sleep(1)
            addCaseLog("uid=%s;action=record;conf-id=%s;record-status=0"%(uid, conf_id))
            addCaseLog("uid=%s;action=record;conf-id=%s;record-status=1"%(uid, conf_id))
            #user request present, accept it
            addCaseLog("uid=%s;action=present_confirm;conf-id=%s;accept=1"%(uid, conf_id))
            time.sleep(1)
            #user request present, decline it
            addCaseLog("uid=%s;action=present_confirm;conf-id=%s;accept=0"%(uid, conf_id))
            #kick user
            addCaseLog("uid=%s;action=kick;conf-id=%s"%(uid, conf_id))
            time.sleep(10)
            #end meeting
            addCaseLog("uid=all;action=kick;conf-id=%s"%(conf_id))
             
            #exceptional test:
            if self.exception == 1:
                 
                addCaseLog("uid=%s;action=present_request;conf-id=%s"%(uid, conf_id))
     
    # for presenter:    
        elif self.role == "presenter":
            addCaseLog("uid=%s;action=mute;conf-id=%s;mute-status=1"%(uid, conf_id))
            time.sleep(1)
            addCaseLog("uid=%s;action=mute;conf-id=%s;mute-status=0"%(uid, conf_id))
            #presenter start desktop share
            addCaseLog("uid=all;action=ctrl_present;conf-id=%s;present-status=1"%(conf_id)) #uid is the role dest
            time.sleep(1)
            #presenter stop desktop share
            addCaseLog("uid=all;action=ctrl_present;conf-id=%s;present-status=0"%(uid, conf_id))
            time.sleep(1)
            addCaseLog("uid=%s;action=userlist_enable_request;conf-id=%s"%(uid,conf_id))
            time.sleep(1)
            # desktop: user request control me 
            addCaseLog("uid=%s;action=desktop_confirm;conf-id=%s;accept=0"%(uid, conf_id))
            time.sleep(1)
            addCaseLog("uid=%s;action=mic_request;conf-id=%s"%(uid, conf_id))
            time.sleep(1)
    # for attendees:
        elif self.role == "attendee":
#             addCaseLog(self.sendsock, "MESSAGE", service_msg, messagedata)
            addCaseLog("uid=%s;action=mute;conf-id=%s;mute-status=1"%(uid, conf_id))
            time.sleep(1)
            addCaseLog("uid=%s;action=mute;conf-id=%s;mute-status=0"%(uid, conf_id))
            time.sleep(1)
            addCaseLog("uid=%s;action=mic_request;conf-id=%s"%(uid, conf_id))
            time.sleep(1)
            addCaseLog("uid=%s;action=desktop_request;conf-id=%s"%(uid, conf_id))
            time.sleep(1)
            addCaseLog("uid=%s;action=present_request;conf-id=%s"%(uid, conf_id))
            time.sleep(1)
            addCaseLog("uid=%s;action=userlist_enable_request;conf-id=%s"%(uid,conf_id))
     
            #after get desktopshare mouse control , try to freeze mouse control
    #                     addCaseLog("uid=%s;action=desktop;conf-id=%s;status=0"%(service_msg.sipid_number, conf_id))
            time.sleep(1)
            addCaseLog("uid=%s;action=present_request;conf-id=%s"%(uid, conf_id))
            time.sleep(1)
            addCaseLog("uid=%s;action=desktop_request;conf-id=%s"%(uid, conf_id))
            time.sleep(1)
            addCaseLog("uid=%s;action=mic_request;conf-id=%s"%(uid, conf_id))
     
    #                     addCaseLog("uid=%s;action=mute;conf-id=%s;mute-status=1"%(peer_user, conf_id))
            time.sleep(1)

class C0002_Xserver_API_Security_Test_full(projectx_base):
    def __init__(self):
        global caseResult,caseLog,is_Exception_test
        is_Exception_test = 1
        self.AUTHOR="chfshan"
        self.startTime = time.strftime('%H%M%S')
        self.moduleID = "Xserver"
        self.caseID = 0000001
        self.sendsock = ""
        self.testType = "privilege" #common|privilege
        self.exception = 0
        self.sleepTime = 2
        self.caseResult = caseResult
        self.caseLog = caseLog
        self.localsock = ""
        self.OnSetUp()
    def OnSetUp(self):
        pass
    def OnTearDown(self):
        addCaseLog("Case down")
        if self.localsock:
            self.localsock.close()
        exitScript()
    def OnError(self):
        addCaseLog("OnError, case failed")
        setCaseResult("failed")
        self.OnTearDown()
    def OnFail(self):
        addCaseLog("OnFail, case failed")
        setCaseResult("failed")
        self.OnTearDown()
    def OnRun(self):
        global SIP_ID_NUMBER,MEETING_PASSWORD,WEB_SERVER_IP,WEB_SERVER_PORT,SIP_SERVER_IP,SIP_SERVER_PORT,LOCAL_PC_PORT
        print "=" * 80

        client1 = create_sipObject()
        client1.sipid_number = SIP_ID_NUMBER
        client1.meeting_pw = MEETING_PASSWORD
        client1 = x_Join_Meeting(client1)


        client2 = create_sipObject()
        client2.sipid_number = SIP_ID_NUMBER + 2
        client2.rtp_port = LOCAL_PC_RTP_PORT + 2
        client2.localport = LOCAL_PC_PORT + 2
        client2.meeting_pw = MEETING_PASSWORD
        client2 = x_Join_Meeting(client2)

        client3 = create_sipObject()
        client3.sipid_number = SIP_ID_NUMBER + 3
        client3.rtp_port = LOCAL_PC_RTP_PORT + 3
        client3.localport = LOCAL_PC_PORT + 3
        client3.meeting_pw = MEETING_PASSWORD
        client3 = x_Join_Meeting(client3)
              
        while service_on:
                # normal  exception test
            addCaseLog("#######exception test stared########")
            addCaseLog("Start Role privilege test")
            client = client1
            source_user = SIP_ID_NUMBER
            target_user = client2.fromuser
            target_user_1 = client3.fromuser
            invalid_user = "0000"
             
            #### start desktop
            content_of_x_gs_conf_contorl = "uid=all;action=ctrl_present;conf-id=%s;present-status=1;share_type=1"%(int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=ctrl_present;conf-id=%s;present-status=1;share_type=1"%(target_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime) 
            content_of_x_gs_conf_contorl = "uid=%s;action=ctrl_present;conf-id=%s;present-status=1;share_type=1"%(invalid_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=all;action=ctrl_present;conf-id=%s;present-status=6;share_type=1"%(MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=all;action=ctrl_present;conf-id=%s;present-status=1;share_type=10"%(MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime) 
            content_of_x_gs_conf_contorl = "uid=all;action=ctrl_present;conf-id=%s;present-status=1;share_type=1"%(MEETINNG_ROOM_ID)
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            ##### mute test ###############
            content_of_x_gs_conf_contorl = "uid=%s;action=mute;conf-id=%s;mute-status=0"%(source_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mute;conf-id=%s;mute-status=0"%(target_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mute;conf-id=%s;mute-status=0"%(invalid_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mute;conf-id=%s;mute-status=0"%(source_user,int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mute;conf-id=%s;mute-status=10"%(source_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mute;conf-id=%s;mute-status=10"%(source_user,MEETINNG_ROOM_ID)
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            ################ mute_user test ######
            content_of_x_gs_conf_contorl = "uid=%s;action=mute_user;conf-id=%s;mute-status=1"%(target_user,int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)                    
            content_of_x_gs_conf_contorl = "uid=%s;action=mute_user;conf-id=%s;mute-status=1"%(invalid_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mute_user;conf-id=%s;mute-status=1"%(target_user,int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mute_user;conf-id=%s;mute-status=1"%(source_user,MEETINNG_ROOM_ID)
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)                                      
            ################ config test wrong confid ######
            content_of_x_gs_conf_contorl = "uid=none;action=conf_config;conf-id=%s;param=mute-status;value=0"%(int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=none;action=conf_config;conf-id=%s;param=mute-status;value=6"%(MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=none;action=conf_config;conf-id=%s;param=leave-prompt;value=0"%(int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=none;action=conf_config;conf-id=%s;param=leave-prompt;value=6"%(MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=none;action=conf_config;conf-id=%s;param=join-prompt;value=0"%(int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=none;action=conf_config;conf-id=%s;param=join-prompt;value=6"%(MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            ### chat and send files
            content_of_x_gs_conf_contorl = "uid=none;action=conf_config;conf-id=%s;param=options;value=01;update-users=2"%(int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=none;action=conf_config;conf-id=%s;param=options;value=66;update-users=2"%(MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=none;action=conf_config;conf-id=%s;param=options;value=11;update-users=6"%(MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=all;action=set_userlist_enable;conf-id=%s;enable=1"%(int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=all;action=set_userlist_enable;conf-id=%s;enable=6"%(int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            ################ config test no privilege ######
            content_of_x_gs_conf_contorl = "uid=none;action=conf_config;conf-id=%s;param=mute-status;value=0"%(int(MEETINNG_ROOM_ID)+1)
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=none;action=conf_config;conf-id=%s;param=leave-prompt;value=0"%(int(MEETINNG_ROOM_ID)+1)
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=none;action=conf_config;conf-id=%s;param=join-prompt;value=0"%(int(MEETINNG_ROOM_ID)+1)
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=none;action=conf_config;conf-id=%s;param=options;value=01;update-users=2"%(int(MEETINNG_ROOM_ID)+1)
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=all;action=set_userlist_enable;conf-id=%s;enable=1"%(int(MEETINNG_ROOM_ID)+1)
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            ############### lock meeting
            # conf locked, host accept user join
            content_of_x_gs_conf_contorl = "uid=%s;action=join_confirm;conf-id=%s;accept=1"%(target_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=join_confirm;conf-id=%s;accept=1"%(invalid_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=join_confirm;conf-id=%s;accept=6"%(target_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=join_confirm;conf-id=%s;accept=1"%(target_user,int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=join_confirm;conf-id=%s;accept=1"%(target_user,MEETINNG_ROOM_ID)
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            ## cofirm request
            content_of_x_gs_conf_contorl = "uid=%s;action=present_confirm;conf-id=%s;accept=1"%(target_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=present_confirm;conf-id=%s;accept=1"%(invalid_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=present_confirm;conf-id=%s;accept=6"%(target_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=present_confirm;conf-id=%s;accept=1"%(target_user,int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)   
            content_of_x_gs_conf_contorl = "uid=%s;action=present_confirm;conf-id=%s;accept=1"%(target_user,MEETINNG_ROOM_ID)
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            ##### uid request mose control
            content_of_x_gs_conf_contorl = "uid=%s;action=desktop_confirm;conf-id=%s;accept=1"%(target_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=desktop_confirm;conf-id=%s;accept=1"%(invalid_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=desktop_confirm;conf-id=%s;accept=6"%(target_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=desktop_confirm;conf-id=%s;accept=1"%(target_user,int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)   
            content_of_x_gs_conf_contorl = "uid=%s;action=desktop_confirm;conf-id=%s;accept=1"%(target_user,MEETINNG_ROOM_ID)
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)                           
            #######Host invite user- call back
            content_of_x_gs_conf_contorl = "uid=%s;action=invite;conf-id=%s"%(target_user,int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=invite;conf-id=%s"%(invalid_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=invite;conf-id=%s"%(source_user,MEETINNG_ROOM_ID)
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime) 
            ######## mic
            content_of_x_gs_conf_contorl = "uid=%s;action=mic;conf-id=%s;mic-status=1"%(target_user,MEETINNG_ROOM_ID) #uid is the role dest
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mic;conf-id=%s;mic-status=1"%(invalid_user,MEETINNG_ROOM_ID) #uid is the role dest
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mic;conf-id=%s;mic-status=1"%(target_user,int(MEETINNG_ROOM_ID)+1) #uid is the role dest
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mic;conf-id=%s;mic-status=6"%(target_user,MEETINNG_ROOM_ID) #uid is the role dest
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mic;conf-id=%s;mic-status=1"%(target_user,MEETINNG_ROOM_ID) #uid is the role dest
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            # host transfer uid mic to target user
            content_of_x_gs_conf_contorl = "uid=%s;action=mic_transfer;conf-id=%s;target=%s"%(invalid_user,MEETINNG_ROOM_ID,target_user)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mic_transfer;conf-id=%s;target=%s"%(target_user,MEETINNG_ROOM_ID,invalid_user)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mic_transfer;conf-id=%s;target=%s"%(target_user,int(MEETINNG_ROOM_ID)+1,target_user_1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mic_transfer;conf-id=%s;target=%s"%(target_user,MEETINNG_ROOM_ID,target_user_1)
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            # user request mic ,host decline
            content_of_x_gs_conf_contorl = "uid=%s;action=mic_confirm;conf-id=%s;choice=0;mic-user=none"%(target_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mic_confirm;conf-id=%s;choice=0;mic-user=none"%(invalid_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mic_confirm;conf-id=%s;choice=0;mic-user=none"%(target_user,int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mic_confirm;conf-id=%s;choice=9;mic-user=none"%(target_user,MEETINNG_ROOM_ID)
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mic_confirm;conf-id=%s;choice=0;mic-user=none"%(target_user,MEETINNG_ROOM_ID)
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            # user request mic ,host accepet(meeting have free mic)
            content_of_x_gs_conf_contorl = "uid=%s;action=mic_confirm;conf-id=%s;choice=1;mic-user=none"%(invalid_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mic_confirm;conf-id=%s;choice=1;mic-user=none"%(target_user,int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mic_confirm;conf-id=%s;choice=1;mic-user=none"%(target_user,MEETINNG_ROOM_ID)
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            # uid request mic ,host transfer mic-user's mic
            content_of_x_gs_conf_contorl = "uid=%s;action=mic_confirm;conf-id=%s;choice=2;mic-user=%s"%(invalid_user,MEETINNG_ROOM_ID,target_user)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mic_confirm;conf-id=%s;choice=2;mic-user=%s"%(target_user,MEETINNG_ROOM_ID,invalid_user)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)                    
            content_of_x_gs_conf_contorl = "uid=%s;action=mic_confirm;conf-id=%s;choice=2;mic-user=%s"%(target_user,int(MEETINNG_ROOM_ID)+1,target_user_1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mic_confirm;conf-id=%s;choice=10;mic-user=%s"%(target_user,MEETINNG_ROOM_ID,target_user_1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mic_confirm;conf-id=%s;choice=2;mic-user=%s"%(target_user,MEETINNG_ROOM_ID,target_user_1)
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            ###### request test
            # mic request
            content_of_x_gs_conf_contorl = "uid=%s;action=mic_request;conf-id=%s"%(target_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mic_request;conf-id=%s"%(invalid_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)                    
            content_of_x_gs_conf_contorl = "uid=%s;action=mic_request;conf-id=%s"%(source_user,int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)                        
            # presenter request
            content_of_x_gs_conf_contorl = "uid=%s;action=present_request;conf-id=%s"%(source_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=present_request;conf-id=%s"%(invalid_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)                    
            content_of_x_gs_conf_contorl = "uid=%s;action=present_request;conf-id=%s"%(source_user,int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)       
            # desktop request
            content_of_x_gs_conf_contorl = "uid=%s;action=desktop_request;conf-id=%s"%(source_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=desktop_request;conf-id=%s"%(invalid_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)                    
            content_of_x_gs_conf_contorl = "uid=%s;action=desktop_request;conf-id=%s"%(source_user,int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)              
            # user_list
            content_of_x_gs_conf_contorl = "uid=%s;action=userlist_enable_request;conf-id=%s"%(target_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)                    
            content_of_x_gs_conf_contorl = "uid=%s;action=userlist_enable_request;conf-id=%s"%(invalid_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=userlist_enable_request;conf-id=%s"%(target_user,int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)   
            content_of_x_gs_conf_contorl = "uid=%s;action=userlist_enable_request;conf-id=%s"%(target_user,MEETINNG_ROOM_ID)
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
 
            # desktop : set mouse control privilege
            content_of_x_gs_conf_contorl = "uid=%s;action=desktop;conf-id=%s;status=1"%(target_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=desktop;conf-id=%s;status=1"%(invalid_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=desktop;conf-id=%s;status=1"%(target_user,int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=desktop;conf-id=%s;status=6"%(target_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=desktop;conf-id=%s;status=1"%(source_user,MEETINNG_ROOM_ID)
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            ######## start record
            content_of_x_gs_conf_contorl = "uid=%s;action=record;conf-id=%s;record-status=0"%(target_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=record;conf-id=%s;record-status=0"%(invalid_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=record;conf-id=%s;record-status=0"%(source_user,int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=record;conf-id=%s;record-status=6"%(source_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=record;conf-id=%s;record-status=0"%(source_user,MEETINNG_ROOM_ID)
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            ######## start record
            content_of_x_gs_conf_contorl = "uid=%s;action=record;conf-id=%s;record-status=0"%(target_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=record;conf-id=%s;record-status=0"%(invalid_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=record;conf-id=%s;record-status=0"%(source_user,int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=record;conf-id=%s;record-status=6"%(source_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=record;conf-id=%s;record-status=0"%(source_user,MEETINNG_ROOM_ID)
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
             
            ################ set_host test ######
            content_of_x_gs_conf_contorl = "uid=%s;action=set_host;conf-id=%s"%(target_user,int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=set_host;conf-id=%s"%(invalid_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=set_host;conf-id=%s"%(source_user,MEETINNG_ROOM_ID)
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)                    
            ################ set_presenter test ######
            content_of_x_gs_conf_contorl = "uid=%s;action=set_presenter;conf-id=%s"%(target_user,int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=set_presenter;conf-id=%s"%(invalid_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=set_presenter;conf-id=%s"%(source_user,MEETINNG_ROOM_ID)
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)  
            ######## kick user
            content_of_x_gs_conf_contorl = "uid=%s;action=kick;conf-id=%s"%(invalid_user,MEETINNG_ROOM_ID)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=kick;conf-id=%s"%(target_user,int(MEETINNG_ROOM_ID)+1)
            client.send_INFO(client.localsock,client.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)  
            content_of_x_gs_conf_contorl = "uid=%s;action=kick;conf-id=%s"%(target_user,MEETINNG_ROOM_ID)
            client2.send_INFO(client2.localsock,client2.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime) 
            addCaseLog("Stop Role privilege test")                    
            time.sleep(self.sleepTime*10)
 
            addCaseLog("Normal Exception Test started")
            time.sleep(self.sleepTime * 5)
            content_of_x_gs_conf_contorl = ""
            client1.send_INFO(client1.localsock,client1.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "中文~!@#$%^&*()_+-={}[]|/:;”’<>,./?;"
            client1.send_INFO(client1.localsock,client1.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mute;conf-id=%s;mute-status=0"%(str(SIP_ID_NUMBER)*100,MEETINNG_ROOM_ID)
            client1.send_INFO(client1.localsock,client1.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=mute;conf-id=%s;mute-status=0"%("~!中文@#$%^&*()_+-={}[]|/:;”’<>,./?;",MEETINNG_ROOM_ID)
            client1.send_INFO(client1.localsock,client1.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=;action=mute;conf-id=;mute-status=1"
            client1.send_INFO(client1.localsock,client1.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)                               
            content_of_x_gs_conf_contorl = "uid=%s;action=%s;conf-id=%s;mute-status=0"%(SIP_ID_NUMBER,SIP_ID_NUMBER,MEETINNG_ROOM_ID)
            client1.send_INFO(client1.localsock,client1.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)
            content_of_x_gs_conf_contorl = "uid=%s;action=%s;conf-id=%s;mute-status=0"%(SIP_ID_NUMBER,"~中文!@#$%^&*()_+-={}[]|/:;”’<>,./?;",MEETINNG_ROOM_ID)
            client1.send_INFO(client1.localsock,client1.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)                          
            content_of_x_gs_conf_contorl = "uid=%s;action=%s;conf-id=%s;mute-status=0"%(SIP_ID_NUMBER,"mute","~中文!@#$%^&*()_+-={}[]|/:;”’<>,./?;")
            client1.send_INFO(client1.localsock,client1.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)                             
            content_of_x_gs_conf_contorl = "uid=%s;action=%s;conf-id=%s;mute-status=%s"%(SIP_ID_NUMBER,"mute",MEETINNG_ROOM_ID,"")
            client1.send_INFO(client1.localsock,client1.object,content_of_x_gs_conf_contorl)
            time.sleep(self.sleepTime)               
            
            self.localsock = client.localsock
            addCaseLog("illegle sip message test stared")   
            #####No Via test
            content_of_x_gs_conf_contorl = "uid=%s;action=%s;conf-id=%s"%(SIP_ID_NUMBER,"mute",MEETINNG_ROOM_ID)
            sip_request = "%s sip:%s@%s:%d SIP/2.0\r\n"%("INFO",MEETINNG_ROOM_ID ,  SIP_SERVER_IP,SIP_SERVER_PORT)
#                     sip_request += "Via: SIP/2.0/TCP %s:%d;branch=z9hG4bK12345678%x;rport;alias"%(LOCAL_PC_IP,LOCAL_PC_PORT, random.randint(0, 10000)) + "\r\n"
            sip_request += "Contact: <sip:" + SIP_ID_NUMBER + "@" + LOCAL_PC_IP + ":" + "%d"%LOCAL_PC_PORT + ";transport=tcp>\r\n"
            sip_request += "To: <sip:%s@%s:%d>;tag=%s\r\n"%(target_user, SIP_SERVER_IP,SIP_SERVER_PORT,  random.randint(0, 10000))
            sip_request += "From: <sip:%s@%s:%d>;tag=%s\r\n"%(target_user, LOCAL_PC_IP,LOCAL_PC_PORT, random.randint(0, 10000))
            sip_request += "Call-ID: %s\r\n"% random.randint(0, 10000)
            sip_request += "CSeq: %d %s\r\n" %(random.randint(0, 10000), "INFO")
            sip_request += "Authorization: %s\r\n"%"XXXXXX";
            sip_request += "User-Agent: %s \r\n"%("Amanda Test")
            sip_request += "Max-Forwards: 70 \r\n"
            sip_request += "X-GS-Conf-Control: %s\r\n" % (content_of_x_gs_conf_contorl)
            sip_request += "Content-Length: 0\r\n\r\n"
            self.localsock.sendall(sip_request)
            time.sleep(self.sleepTime)
            #### no contact Test
            sip_request = "%s sip:%s@%s:%d SIP/2.0\r\n"%("INFO",MEETINNG_ROOM_ID ,  SIP_SERVER_IP,SIP_SERVER_PORT)
            sip_request += "Via: SIP/2.0/TCP %s:%d;branch=z9hG4bK12345678%x;rport;alias"%(LOCAL_PC_IP,LOCAL_PC_PORT, random.randint(0, 10000)) + "\r\n"
#                     sip_request += "Contact: <sip:" + SIP_ID_NUMBER + "@" + LOCAL_PC_IP + ":" + "%d"%LOCAL_PC_PORT + ";transport=tcp>\r\n"
            sip_request += "To: <sip:%s@%s:%d>;tag=%s\r\n"%(target_user, SIP_SERVER_IP,SIP_SERVER_PORT,  random.randint(0, 10000))
            sip_request += "From: <sip:%s@%s:%d>;tag=%s\r\n"%(target_user, LOCAL_PC_IP,LOCAL_PC_PORT, random.randint(0, 10000))
            sip_request += "Call-ID: %s\r\n"% random.randint(0, 10000)
            sip_request += "CSeq: %d %s\r\n" %(random.randint(0, 10000), "INFO")
            sip_request += "Authorization: %s\r\n"%"XXXXXX";
            sip_request += "User-Agent: %s \r\n"%("Amanda Test")
            sip_request += "Max-Forwards: 70 \r\n"
            sip_request += "X-GS-Conf-Control: %s\r\n" % (content_of_x_gs_conf_contorl)
            sip_request += "Content-Length: 0\r\n\r\n"
            try:
                self.localsock.sendall(sip_request)
            except Exception as e:
                addCaseLog("send INFO no contact exceptional test failed,socket connect failed: %s" % str(e))
                self.OnError()
            time.sleep(self.sleepTime)

            #### no to Test
            sip_request = "%s sip:%s@%s:%d SIP/2.0\r\n"%("INFO",MEETINNG_ROOM_ID ,  SIP_SERVER_IP,SIP_SERVER_PORT)
            sip_request += "Via: SIP/2.0/TCP %s:%d;branch=z9hG4bK12345678%x;rport;alias"%(LOCAL_PC_IP,LOCAL_PC_PORT, random.randint(0, 10000)) + "\r\n"
            sip_request += "Contact: <sip:" + SIP_ID_NUMBER + "@" + LOCAL_PC_IP + ":" + "%d"%LOCAL_PC_PORT + ";transport=tcp>\r\n"
#                     sip_request += "To: <sip:%s@%s:%d>;tag=%s\r\n"%(target_user, SIP_SERVER_IP,SIP_SERVER_PORT,  random.randint(0, 10000))
            sip_request += "From: <sip:%s@%s:%d>;tag=%s\r\n"%(target_user, LOCAL_PC_IP,LOCAL_PC_PORT, random.randint(0, 10000))
            sip_request += "Call-ID: %s\r\n"% random.randint(0, 10000)
            sip_request += "CSeq: %d %s\r\n" %(random.randint(0, 10000), "INFO")
            sip_request += "Authorization: %s\r\n"%"XXXXXX";
            sip_request += "User-Agent: %s \r\n"%("Amanda Test")
            sip_request += "Max-Forwards: 70 \r\n"
            sip_request += "X-GS-Conf-Control: %s\r\n" % (content_of_x_gs_conf_contorl)
            sip_request += "Content-Length: 0\r\n\r\n"
            try:
                self.localsock.sendall(sip_request)
            except Exception as e:
                addCaseLog("send INFO no contact exceptional test failed,socket connect failed: %s") % str(e)
                self.OnError()
            time.sleep(self.sleepTime)

            #### no from Test
            sip_request = "%s sip:%s@%s:%d SIP/2.0\r\n"%("INFO",MEETINNG_ROOM_ID ,  SIP_SERVER_IP,SIP_SERVER_PORT)
            sip_request += "Via: SIP/2.0/TCP %s:%d;branch=z9hG4bK12345678%x;rport;alias"%(LOCAL_PC_IP,LOCAL_PC_PORT, random.randint(0, 10000)) + "\r\n"
            sip_request += "Contact: <sip:" + SIP_ID_NUMBER + "@" + LOCAL_PC_IP + ":" + "%d"%LOCAL_PC_PORT + ";transport=tcp>\r\n"
            sip_request += "To: <sip:%s@%s:%d>;tag=%s\r\n"%(target_user, SIP_SERVER_IP,SIP_SERVER_PORT,  random.randint(0, 10000))
#                     sip_request += "From: <sip:%s@%s:%d>;tag=%s\r\n"%(target_user, LOCAL_PC_IP,LOCAL_PC_PORT, random.randint(0, 10000))
            sip_request += "Call-ID: %s\r\n"% random.randint(0, 10000)
            sip_request += "CSeq: %d %s\r\n" %(random.randint(0, 10000), "INFO")
            sip_request += "Authorization: %s\r\n"%"XXXXXX";
            sip_request += "User-Agent: %s \r\n"%("Amanda Test")
            sip_request += "Max-Forwards: 70 \r\n"
            sip_request += "X-GS-Conf-Control: %s\r\n" % (content_of_x_gs_conf_contorl)
            sip_request += "Content-Length: 0\r\n\r\n"
            try:
                self.localsock.sendall(sip_request)
            except Exception as e:
                addCaseLog("send INFO no contact exceptional test failed,socket connect failed: %s") % str(e)
                self.OnError()
            time.sleep(self.sleepTime)
            #### no call -ID Test
            sip_request = "%s sip:%s@%s:%d SIP/2.0\r\n"%("INFO",MEETINNG_ROOM_ID ,  SIP_SERVER_IP,SIP_SERVER_PORT)
            sip_request += "Via: SIP/2.0/TCP %s:%d;branch=z9hG4bK12345678%x;rport;alias"%(LOCAL_PC_IP,LOCAL_PC_PORT, random.randint(0, 10000)) + "\r\n"
            sip_request += "Contact: <sip:" + SIP_ID_NUMBER + "@" + LOCAL_PC_IP + ":" + "%d"%LOCAL_PC_PORT + ";transport=tcp>\r\n"
            sip_request += "To: <sip:%s@%s:%d>;tag=%s\r\n"%(target_user, SIP_SERVER_IP,SIP_SERVER_PORT,  random.randint(0, 10000))
            sip_request += "From: <sip:%s@%s:%d>;tag=%s\r\n"%(target_user, LOCAL_PC_IP,LOCAL_PC_PORT, random.randint(0, 10000))
#                     sip_request += "Call-ID: %s\r\n"% random.randint(0, 10000)
            sip_request += "CSeq: %d %s\r\n" %(random.randint(0, 10000), "INFO")
            sip_request += "Authorization: %s\r\n"%"XXXXXX";
            sip_request += "User-Agent: %s \r\n"%("Amanda Test")
            sip_request += "Max-Forwards: 70 \r\n"
            sip_request += "X-GS-Conf-Control: %s\r\n" % (content_of_x_gs_conf_contorl)
            sip_request += "Content-Length: 0\r\n\r\n"
            try:
                self.localsock.sendall(sip_request)
            except Exception as e:
                addCaseLog("send INFO no contact exceptional test failed,socket connect failed: %s") % str(e)
                self.OnError()
            time.sleep(self.sleepTime)                    
            #### no cseq Test
            sip_request = "%s sip:%s@%s:%d SIP/2.0\r\n"%("INFO",MEETINNG_ROOM_ID ,  SIP_SERVER_IP,SIP_SERVER_PORT)
            sip_request += "Via: SIP/2.0/TCP %s:%d;branch=z9hG4bK12345678%x;rport;alias"%(LOCAL_PC_IP,LOCAL_PC_PORT, random.randint(0, 10000)) + "\r\n"
            sip_request += "Contact: <sip:" + SIP_ID_NUMBER + "@" + LOCAL_PC_IP + ":" + "%d"%LOCAL_PC_PORT + ";transport=tcp>\r\n"
            sip_request += "To: <sip:%s@%s:%d>;tag=%s\r\n"%(target_user, SIP_SERVER_IP,SIP_SERVER_PORT,  random.randint(0, 10000))
            sip_request += "From: <sip:%s@%s:%d>;tag=%s\r\n"%(target_user, LOCAL_PC_IP,LOCAL_PC_PORT, random.randint(0, 10000))
            sip_request += "Call-ID: %s\r\n"% random.randint(0, 10000)
#                     sip_request += "CSeq: %d %s\r\n" %(random.randint(0, 10000), "INFO")
            sip_request += "Authorization: %s\r\n"%"XXXXXX";
            sip_request += "User-Agent: %s \r\n"%("Amanda Test")
            sip_request += "Max-Forwards: 70 \r\n"
            sip_request += "X-GS-Conf-Control: %s\r\n" % (content_of_x_gs_conf_contorl)
            sip_request += "Content-Length: 0\r\n\r\n"
            try:
                self.localsock.sendall(sip_request)
            except Exception as e:
                addCaseLog("send INFO no contact exceptional test failed,socket connect failed: %s") % str(e)
                self.OnError()
            time.sleep(self.sleepTime)     
            #### no content-len Test
            sip_request = "%s sip:%s@%s:%d SIP/2.0\r\n"%("INFO",MEETINNG_ROOM_ID ,  SIP_SERVER_IP,SIP_SERVER_PORT)
            sip_request += "Via: SIP/2.0/TCP %s:%d;branch=z9hG4bK12345678%x;rport;alias"%(LOCAL_PC_IP,LOCAL_PC_PORT, random.randint(0, 10000)) + "\r\n"
            sip_request += "Contact: <sip:" + SIP_ID_NUMBER + "@" + LOCAL_PC_IP + ":" + "%d"%LOCAL_PC_PORT + ";transport=tcp>\r\n"
            sip_request += "To: <sip:%s@%s:%d>;tag=%s\r\n"%(target_user, SIP_SERVER_IP,SIP_SERVER_PORT,  random.randint(0, 10000))
            sip_request += "From: <sip:%s@%s:%d>;tag=%s\r\n"%(target_user, LOCAL_PC_IP,LOCAL_PC_PORT, random.randint(0, 10000))
            sip_request += "Call-ID: %s\r\n"% random.randint(0, 10000)
            sip_request += "CSeq: %d %s\r\n" %(random.randint(0, 10000), "INFO")
            sip_request += "Authorization: %s\r\n"%"XXXXXX";
            sip_request += "User-Agent: %s \r\n"%("Amanda Test")
            sip_request += "Max-Forwards: 70 \r\n"
            sip_request += "X-GS-Conf-Control: %s\r\n" % (content_of_x_gs_conf_contorl)
#                     sip_request += "Content-Length: 0\r\n\r\n"
            try:
                self.localsock.sendall(sip_request)
            except Exception as e:
                addCaseLog("send INFO no contact exceptional test failed,socket connect failed: %s") % str(e)
                self.OnError()
            time.sleep(self.sleepTime)    

            #### no content-type Test
            chat_content = "amanda"
            sip_request = "%s sip:%s@%s:%d SIP/2.0\r\n"%("MESSAGE",MEETINNG_ROOM_ID ,  SIP_SERVER_IP,SIP_SERVER_PORT)
            sip_request += "Via: SIP/2.0/TCP %s:%d;branch=z9hG4bK12345678%x;rport;alias"%(LOCAL_PC_IP,LOCAL_PC_PORT, random.randint(0, 10000)) + "\r\n"
            sip_request += "Contact: <sip:" + SIP_ID_NUMBER + "@" + LOCAL_PC_IP + ":" + "%d"%LOCAL_PC_PORT + ";transport=tcp>\r\n"
            sip_request += "To: <sip:%s@%s:%d>;tag=%s\r\n"%(target_user, SIP_SERVER_IP,SIP_SERVER_PORT,  random.randint(0, 10000))
            sip_request += "From: <sip:%s@%s:%d>;tag=%s\r\n"%(target_user, LOCAL_PC_IP,LOCAL_PC_PORT, random.randint(0, 10000))
            sip_request += "Call-ID: %s\r\n"% random.randint(0, 10000)
            sip_request += "CSeq: %d %s\r\n" %(random.randint(0, 10000), "MESSAGE")
            sip_request += "Authorization: %s\r\n"%"XXXXXX";
            sip_request += "User-Agent: %s \r\n"%("Amanda Test")
            sip_request += "Max-Forwards: 70 \r\n"
            sip_request += "X-GS-Message-Users: %s\r\n"%("all")
#             sip_request += "Content-Type: text/plain;charset=utf-8\r\n"
            sip_request += "Content-Length: %d\r\n\r\n"%(len(chat_content))
            sip_request += chat_content
            try:
                self.localsock.sendall(sip_request)
            except Exception as e:
                addCaseLog("send INFO no contact exceptional test failed,socket connect failed: %s") % str(e)
                self.OnError()
            time.sleep(self.sleepTime)

            #### no content-type Test
            chat_content = ""
            sip_request = "%s sip:%s@%s:%d SIP/2.0\r\n"%("MESSAGE",MEETINNG_ROOM_ID ,  SIP_SERVER_IP,SIP_SERVER_PORT)
            sip_request += "Via: SIP/2.0/TCP %s:%d;branch=z9hG4bK12345678%x;rport;alias"%(LOCAL_PC_IP,LOCAL_PC_PORT, random.randint(0, 10000)) + "\r\n"
            sip_request += "Contact: <sip:" + SIP_ID_NUMBER + "@" + LOCAL_PC_IP + ":" + "%d"%LOCAL_PC_PORT + ";transport=tcp>\r\n"
            sip_request += "To: <sip:%s@%s:%d>;tag=%s\r\n"%(target_user, SIP_SERVER_IP,SIP_SERVER_PORT,  random.randint(0, 10000))
            sip_request += "From: <sip:%s@%s:%d>;tag=%s\r\n"%(target_user, LOCAL_PC_IP,LOCAL_PC_PORT, random.randint(0, 10000))
            sip_request += "Call-ID: %s\r\n"% random.randint(0, 10000)
            sip_request += "CSeq: %d %s\r\n" %(random.randint(0, 10000), "MESSAGE")
            sip_request += "Authorization: %s\r\n"%"XXXXXX";
            sip_request += "User-Agent: %s \r\n"%("Amanda Test")
            sip_request += "Max-Forwards: 70 \r\n"
            sip_request += "X-GS-Message-Users: %s\r\n"%("all")
            sip_request += "Content-Type: text/plain;charset=utf-8\r\n"
            sip_request += "Content-Length: %d\r\n\r\n"%(len(chat_content))
            sip_request += chat_content
            try:
                self.localsock.sendall(sip_request)
            except Exception as e:
                addCaseLog("send INFO no contact exceptional test failed,socket connect failed: %s") % str(e)
                self.OnError()            
            time.sleep(self.sleepTime)

            #### no content-type Test
            chat_content = "amanda"
            sip_request = "%s sip:%s@%s:%d SIP/2.0\r\n"%("MESSAGE",MEETINNG_ROOM_ID ,  SIP_SERVER_IP,SIP_SERVER_PORT)
            sip_request += "Via: SIP/2.0/TCP %s:%d;branch=z9hG4bK12345678%x;rport;alias"%(LOCAL_PC_IP,LOCAL_PC_PORT, random.randint(0, 10000)) + "\r\n"
            sip_request += "Contact: <sip:" + SIP_ID_NUMBER + "@" + LOCAL_PC_IP + ":" + "%d"%LOCAL_PC_PORT + ";transport=tcp>\r\n"
            sip_request += "To: <sip:%s@%s:%d>;tag=%s\r\n"%(target_user, SIP_SERVER_IP,SIP_SERVER_PORT,  random.randint(0, 10000))
            sip_request += "From: <sip:%s@%s:%d>;tag=%s\r\n"%(target_user, LOCAL_PC_IP,LOCAL_PC_PORT, random.randint(0, 10000))
            sip_request += "Call-ID: %s\r\n"% random.randint(0, 10000)
            sip_request += "CSeq: %d %s\r\n" %(random.randint(0, 10000), "MESSAGE")
            sip_request += "Authorization: %s\r\n"%"XXXXXX";
            sip_request += "User-Agent: %s \r\n"%("Amanda Test")
            sip_request += "Max-Forwards: 70 \r\n"
            sip_request += "X-GS-Message-Users: %s\r\n"%("all")
            sip_request += "Content-Type: text/plain;charset=utf-8\r\n"
#             sip_request += "Content-Length: %d\r\n\r\n"%(len(chat_content))
            sip_request += chat_content
            try:
                self.localsock.sendall(sip_request)
            except Exception as e:
                addCaseLog("send INFO no contact exceptional test failed,socket connect failed: %s") % str(e)
                self.OnError()            
            time.sleep(self.sleepTime)

            addCaseLog("illegle sip message test finished")             
            addCaseLog("Normal Exception Test stoped")
            time.sleep(self.sleepTime * 5)
            addCaseLog("#######exception test stopped########")

#######################
# local_webapi_key_url: "/user/voip", the url that web supply. http://api.ipvideotalk.com(/xxxx/xxxx)
#######################
class C0001_ErrorCode_WebPageServer_ForPC(projectx_base):
    def __init__(self,local_webapi_key_url = ""):
        global WEBAPI_KEY_URL
        if local_webapi_key_url == "":
            self.local_webapi_key_url = WEBAPI_KEY_URL
        else:
            self.local_webapi_key_url = local_webapi_key_url
    def OnSetUp(self):
        pass
    def OnTearDown(self):
        pass
    def OnError(self):
        pass
    def OnFail(self):
        pass
    def OnRun(self):
        a = web_Exceptional_Common(self.local_webapi_key_url)
        a.Run()

class C0004_PC_Simulator(projectx_base):    
    def __init__(self):
        global is_Exception_test
        is_Exception_test = 1
        self.AUTHOR="chfshan"
        self.startTime = time.strftime('%H%M%S')
        self.moduleID = "Xserver"
        self.caseID = 0000001
        self.sendsock = ""
        self.exception = 0
        self.sleepTime = 2
        self.OnSetUp()
        self.localsock = ''
    def OnSetUp(self):
        pass
    def OnTearDown(self):
        global caseResult,caseLog, case_Report_Manager
        global client_list
        addCaseLog("Case onTeardown")
#         print (case_Report_Manager.mErrorCount)
#         case_Report_Manager.reportCaseResult(self.AUTHOR,self.moduleID,self.caseID,self.caseResult,self.caseLog)
        if self.localsock:
            self.localsock.close()
        for i in range(len(client_list)):
            if client_list[i].localsock:
                client_list[i].localsock.close()
#         exitScript()
    def OnError(self):
        addCaseLog("OnError, case failed")
        setCaseResult("failed")
        self.OnTearDown()
    def OnFail(self):
        addCaseLog("OnFail, case failed")
        setCaseResult("failed")
        self.OnTearDown()
    def OnRun(self):
        global SIP_ID_NUMBER,MEETING_PASSWORD,WEB_SERVER_IP,WEB_SERVER_PORT,SIP_SERVER_IP,SIP_SERVER_PORT,LOCAL_PC_PORT
        print "=" * 80
        global client_list
        client_list = []
        client = []
        client0 = create_sipObject()
        client0.sipid_number = SIP_ID_NUMBER
        client0.local_port_number = LOCAL_PC_PORT
        client0.rtp_media_port = LOCAL_PC_RTP_PORT
        client0.meeting_id_to_user = MEETINNG_ROOM_ID
        client0.meeting_pw = MEETING_PASSWORD
        client0.user_agent = 'windows'
        client0.display_name = 'last @#$啊'
        client0 = x_Join_Meeting(client0)
        client.append(client0)
        client_list.append(client0)

        clientType = ['ios','ios','ios','grandstream gxv*']
        for i in range(len(clientType)):
#         for i in range(0):
            temp_client = create_sipObject()
            temp_client.sipid_number = 7200+i
            temp_client.sipid_password = temp_client.sipid_number
            temp_client.local_port_number = LOCAL_PC_PORT+i
            temp_client.rtp_media_port = LOCAL_PC_RTP_PORT+i
            temp_client.meeting_id_to_user = MEETINNG_ROOM_ID
            temp_client.meeting_pw = MEETING_PASSWORD
            temp_client.user_agent = clientType[i%len(clientType)]
            temp_client.display_name = 'py $%^&我 ' + str(i)
            temp_client = x_Join_Meeting(temp_client)
            client.append(temp_client)
            client_list.append(temp_client)

        for i in range(0,60):
#         for i in range(0):
            temp_client = create_sipObject()
            temp_client.sipid_number = 7300+i
            temp_client.sipid_password = temp_client.sipid_number
            temp_client.local_port_number = LOCAL_PC_PORT+i
            temp_client.rtp_media_port = LOCAL_PC_RTP_PORT+i
            temp_client.meeting_id_to_user = MEETINNG_ROOM_ID
            temp_client.meeting_pw = MEETING_PASSWORD
            temp_client.user_agent = clientType[i%len(clientType)]
            temp_client.display_name = 'py $%^&我 ' + str(i)
            temp_client = x_Join_Meeting(temp_client)
            client.append(temp_client)
            client_list.append(temp_client)
        while 1:
            pass

#             
             
        addCaseLog("inited %s clients , they are %s" % (len(client),client))
         
        while service_on:
#         while 0:
            for i in range(len(clientType)):
                # normal  exception test
                addCaseLog("#######Demo test stared########")
                time.sleep(self.sleepTime)
                print i
                client[i].send_MESSAGE(client[i].localsock,client[i].object,"all")
                time.sleep(self.sleepTime)
                content_of_x_gs_conf_contorl = "uid=%s;action=mute;conf-id=%s;mute-status=0"%(client[i].fromuser,MEETINNG_ROOM_ID)
                client[i].send_INFO(client[i].localsock,client[i].object,content_of_x_gs_conf_contorl)
                time.sleep(self.sleepTime)
                content_of_x_gs_conf_contorl = "uid=%s;action=mute;conf-id=%s;mute-status=1"%(client[i].fromuser,MEETINNG_ROOM_ID)
                client[i].send_INFO(client[i].localsock,client[i].object,content_of_x_gs_conf_contorl)
                time.sleep(self.sleepTime)
#                 content_of_x_gs_conf_contorl = "uid=%s;action=mute_user;conf-id=%s;mute-status=0"%(client[i].fromuser,MEETINNG_ROOM_ID)
#                 client[i].send_INFO(client[i].localsock,client[i].object,content_of_x_gs_conf_contorl)
#                 time.sleep(self.sleepTime)
#                 content_of_x_gs_conf_contorl = "uid=%s;action=mute_user;conf-id=%s;mute-status=1"%(client[i].fromuser,MEETINNG_ROOM_ID)
#                 client[i].send_INFO(client[i].localsock,client[i].object,content_of_x_gs_conf_contorl)
#                 time.sleep(self.sleepTime)
#                 #### start desktop
#                 content_of_x_gs_conf_contorl = "uid=%s;action=mic_request;conf-id=%s"%(client[i].fromuser,MEETINNG_ROOM_ID)
#                 client[i].send_INFO(client[i].localsock,client[i].object,content_of_x_gs_conf_contorl)
#                 time.sleep(self.sleepTime)                        
#                 # presenter request
#                 content_of_x_gs_conf_contorl = "uid=%s;action=present_request;conf-id=%s"%(client[i].fromuser,MEETINNG_ROOM_ID)
#                 client[i].send_INFO(client[i].localsock,client[i].object,content_of_x_gs_conf_contorl)
#                 time.sleep(self.sleepTime)      
#                 # desktop request
#                 content_of_x_gs_conf_contorl = "uid=%s;action=desktop_request;conf-id=%s"%(client[i].fromuser,MEETINNG_ROOM_ID)
#                 client[i].send_INFO(client[i].localsock,client[i].object,content_of_x_gs_conf_contorl)
#                 time.sleep(self.sleepTime)            
#                 # user_list
#                 content_of_x_gs_conf_contorl = "uid=%s;action=userlist_enable_request;conf-id=%s"%(client[i].fromuser,MEETINNG_ROOM_ID)
#                 client[i].send_INFO(client[i].localsock,client[i].object,content_of_x_gs_conf_contorl)
#                 time.sleep(self.sleepTime)

def getPassedTime(starttime='',endtime='',timeType='seconds'):
    result = 0
    if starttime=='':
        starttime = datetime.datetime.now()
    if endtime=='':
        endtime = datetime.datetime.now()
    usedtime = endtime-starttime
    if timeType == 'seconds':
        result = usedtime.seconds
    if timeType == 'microseconds':
        result = usedtime.microseconds 
    
    return result

class C0006_ipvidotalk_PC_Simulator(projectx_base):
    def __init__(self):
        global is_Exception_test
        is_Exception_test = 1
        self.AUTHOR="chfshan"
        self.startTime = time.strftime('%H%M%S')
        self.moduleID = "Xserver"
        self.caseID = 0000001
        self.sendsock = ""
        self.exception = 0
        self.sleepTime = 10
        self.OnSetUp()
        self.localsock = ''
    def OnSetUp(self):
        pass
    def OnTearDown(self):
        global caseResult,caseLog, case_Report_Manager
        addCaseLog("Case onTeardown(C0006_ipvidotalk_PC_Simulator)")
#         print (case_Report_Manager.mErrorCount)
#         case_Report_Manager.reportCaseResult(self.AUTHOR,self.moduleID,self.caseID,self.caseResult,self.caseLog)
        if self.localsock:
            self.localsock.close()

    def OnError(self):
        addCaseLog("OnError, case failed")
        setCaseResult("failed")
        self.OnTearDown()
    def OnFail(self):
        addCaseLog("OnFail, case failed")
        setCaseResult("failed")
        self.OnTearDown()
    def OnRun(self):
        global SIP_ID_NUMBER,MEETING_PASSWORD,WEB_SERVER_IP,WEB_SERVER_PORT,SIP_SERVER_IP,SIP_SERVER_PORT,LOCAL_PC_PORT,SIP_SERVER_DOMAIN_NAME
        global SESSIONINFO
        print "=" * 80
        global service_on
        success = []
        failed  = []
        client0 = create_sipObject()
        client0.sipid_number = SIP_ID_NUMBER
        client0.sipid_password = SIP_ID_NUMBER
        client0.local_port_number = LOCAL_PC_PORT
        client0.rtp_media_port = LOCAL_PC_RTP_PORT
        client0.meeting_id_to_user = MEETINNG_ROOM_ID
        client0.meeting_pw = MEETING_PASSWORD
        client0.dest_ip_domain_name = SIP_SERVER_DOMAIN_NAME
        client0.protocol = 'tcp'
        client0.user_agent = 'windows'
        client0.display_name = 'last'
        client0.isSrtp = 0
        client0 = x_Join_Meeting(client0)
        starttime = datetime.datetime.now()
        ## SESSIONINFO.append({'fromuser':self.fromuser,'call_id':invite_call_id_str,'fromtag':from_tag_str,'totag':'None'})
        while service_on:
            if getPassedTime(starttime) >= 32:
                service_on = 0
                setCaseResult("failed")
                break
            time.sleep(30)

            if client0.receivedThread.invite_200OK_index > 0:
                client0.object.call_id = client0.get(client0.object, 'call_id')
                client0.object.totag = client0.get(client0.object, 'totag')
                client0.object.fromtag = client0.get(client0.object, 'fromtag')
                client0.object.hastotag = True

                sdp_content = "v=0\r\no=user1 8000 8000 IN IP4 %s\r\ns=SIP Call\r\nc=IN IP4 %s\r\nt=0 0\r\n"%(client0.object.local_ip_number,client0.object.local_ip_number)
                sdp_content +=  "m=audio %d RTP/SAVP 0 101\r\na=sendrecv\r\na=rtpmap:0 PCMU/8000\r\na=ptime:20\r\na=rtpmap:101 telephone-event/8000\r\na=fmtp:101 0-15\r\n"%(35589)
                sdp_content += "a=crypto:1 AES_CM_256_HMAC_SHA1_80 inline:75f0VtA/4DiQX8hp5DSi0qkYUV99q44ua5vkdL4W1e32yRr92ZMIaKDLDqtSKg==|2^31\r\n"
                sdp_content += "a=crypto:2 AES_CM_256_HMAC_SHA1_32 inline:W/UvV5zFQg7jIRrso3CS2dj1yxJE6DvR0zLfnCDGjCcQl2PnnDljNa0YGRogTw==|2^31\r\n"
                sdp_content += "a=crypto:3 AES_CM_128_HMAC_SHA1_80 inline:cr3pJrFmUyt7LmXrD0ZhTZTgZoyLvTXPZFQQZyyc|2^31\r\n"
                sdp_content += "a=crypto:4 AES_CM_128_HMAC_SHA1_32 inline:vqRjdqxU7Lot2R3d4ub2PDXWbwf/qerNSpvInzBj|2^31\r\n"
                sdp_content += "m=video 33930 RTP/SAVP 99 100 101 120 122\r\n"
                sdp_content += "b=AS:2240\r\n"
                sdp_content += "a=sendrecv\r\n"
                sdp_content += "a=rtpmap:99 H264/90000\r\n"
                sdp_content += "a=fmtp:99 profile-level-id=428028; packetization-mode=1\r\n"
                sdp_content += "a=rtpmap:100 H264/90000\r\n"
                sdp_content += "a=fmtp:100 profile-level-id=4D0028; packetization-mode=1\r\n"
                sdp_content += "a=rtpmap:101 H264/90000\r\n"
                sdp_content += "a=fmtp:101 profile-level-id=640028; packetization-mode=1\r\n"
                sdp_content += "a=rtpmap:120 ulpfec/90000\r\n"
                sdp_content += "a=rtpmap:122 red/90000\r\n"
                sdp_content += "a=framerate:30\r\n"
                sdp_content += "a=crypto:1 AES_CM_256_HMAC_SHA1_80 inline:xB3uztF/dbE1Dcvo6ffIck/MdozIne/qYtFkk6+FOlqxnU708WxZu678b/4z+g==|2^31\r\n"
                sdp_content += "a=crypto:2 AES_CM_256_HMAC_SHA1_32 inline:ogJCQcOarAFIXgKMSYtmvaV3egVCr3oTca9mH289V9QHYvPYVQb8+acnAvV8tQ==|2^31\r\n"
                sdp_content += "a=crypto:3 AES_CM_128_HMAC_SHA1_80 inline:OeauDmVIqxHyqN/hIOsuOFs5nWWohBDjPLgumCeB|2^31\r\n"
                sdp_content += "a=crypto:4 AES_CM_128_HMAC_SHA1_32 inline:YKcttPnytVtwL9tgyKag1BCEQd0G36U610fvdQIF|2^31\r\n"
                sdp_content += "a=content:main\r\n"
                sdp_content += "a=label:11\r\n"
                client0.set(client0.object, "sdp", sdp_content)
                client0.object.sdp = sdp_content
                client0.send_invite(client0.localsock, client0.object)
                time.sleep(5)
                

        print "total call time = 4 "
        
        print "success call : %s, success time = %d " %  (str(success),len(success))
        print "failed call : %s,failed time = %d" % (str(failed), len(failed))

class C0007_ipvidotalk_loopcall(projectx_base):
    def __init__(self):
        global is_Exception_test
        is_Exception_test = 1
        self.AUTHOR="chfshan"
        self.startTime = time.strftime('%H%M%S')
        self.moduleID = "Xserver"
        self.caseID = 0000001
        self.sendsock = ""
        self.exception = 0
        self.sleepTime = 10
        self.OnSetUp()
        self.localsock = ''
    def OnSetUp(self):
        pass
    def OnTearDown(self):
        global caseResult,caseLog, case_Report_Manager
        addCaseLog("Case onTeardown(C0006_ipvidotalk_PC_Simulator)")
#         print (case_Report_Manager.mErrorCount)
#         case_Report_Manager.reportCaseResult(self.AUTHOR,self.moduleID,self.caseID,self.caseResult,self.caseLog)
        if self.localsock:
            self.localsock.close()

    def OnError(self):
        addCaseLog("OnError, case failed")
        setCaseResult("failed")
        self.OnTearDown()
    def OnFail(self):
        addCaseLog("OnFail, case failed")
        setCaseResult("failed")
        self.OnTearDown()
    def OnRun(self):
        global SIP_ID_NUMBER,MEETING_PASSWORD,WEB_SERVER_IP,WEB_SERVER_PORT,SIP_SERVER_IP,SIP_SERVER_PORT,LOCAL_PC_PORT,SIP_SERVER_DOMAIN_NAME
        global SESSIONINFO
        print "=" * 80
        global service_on
        success = []
        failed  = []
        for j in range(0,5):
            service_on = 1
            SESSIONINFO = []
            print SESSIONINFO
#             client0.receivedThread.invite_200OK_index = 0
            client0 = create_sipObject()
            client0.sipid_number = SIP_ID_NUMBER
            client0.local_port_number = LOCAL_PC_PORT
            client0.rtp_media_port = LOCAL_PC_RTP_PORT
            client0.meeting_id_to_user = MEETINNG_ROOM_ID
            client0.meeting_pw = MEETING_PASSWORD
            client0.dest_ip_domain_name = SIP_SERVER_DOMAIN_NAME
            client0.protocol = 'tcp'
            client0.user_agent = 'windows'
            client0.display_name = 'last'
            client0.isSrtp = 1
            client0 = x_Join_Meeting(client0)
            starttime = datetime.datetime.now()
            ## SESSIONINFO.append({'fromuser':self.fromuser,'call_id':invite_call_id_str,'fromtag':from_tag_str,'totag':'None'})
            while service_on:
                if getPassedTime(starttime) >= 32:
                    service_on = 0
                    setCaseResult("failed")
                    break
                if client0.receivedThread.invite_200OK_index > 0:
                    for i in range(0,len(SESSIONINFO)):
                        if SESSIONINFO[i]['fromuser'] == SIP_ID_NUMBER:
                            client0.object.call_id = SESSIONINFO[i]['call_id']
                            client0.object.totag = SESSIONINFO[i]['totag']
                            client0.object.fromtag = SESSIONINFO[i]['fromtag']
                            time.sleep(10)
                            client0.send_BYE(client0.localsock, client0.object)
                            service_on = 0
                            setCaseResult("success")
                            success.append({j:SESSIONINFO[i]['call_id']})
                            break
        print "total call time = 4 "
        print "success call : %s, success time = %d " %  (str(success),len(success))
        print "failed call : %s,failed time = %d" % (str(failed), len(failed))


#         clientType = ['ios','grandstream gxv','grandstream gxp','other','windows','mac','android','websocket','pstn']
#         sipid_number = ['2022','1031','2166','2088','2010','2011','2012','2480','2025']
#         for i in range(len(clientType)):
#             temp_client = create_sipObject()
#             temp_client.dest_ip_domain_name = SIP_SERVER_DOMAIN_NAME
#             temp_client.sipid_number = int(SIP_ID_NUMBER) + i
#             temp_client.local_port_number = LOCAL_PC_PORT + i
#             temp_client.rtp_media_port = LOCAL_PC_RTP_PORT + i
#             temp_client.meeting_id_to_user = sipid_number[i%len(sipid_number)]
#             temp_client.meeting_pw = MEETING_PASSWORD
#             temp_client.user_agent = clientType[i%len(clientType)]
#             temp_client.display_name = 'py $%^&我 ' + str(i)
#             temp_client.protocol = 'tls'
#             temp_client = sipServer_commonlib(temp_client)
#             temp_client.start_Xserver()
#             client.append(temp_client)
#             client_list.append(temp_client)
#              
#              
#         addCaseLog("inited %s clients , they are %s" % (len(client),client))
#          
#         while service_on:
# #         while 0:
#             for i in range(len(clientType)):
#                 # normal  exception test
#                 addCaseLog("#######Demo test stared########")
#                 time.sleep(self.sleepTime)
#                 client[i].send_MESSAGE("all")
#                 time.sleep(self.sleepTime)

#######################
# sipmethod: "info" | "invite" | "register" | "message"
# testnum  : 1-n  , the test time of sipmethod, if =1, the first "sipmethod" request will start errorcode test
# role     : "all"(default) | "host" | "presenter" | "creater" | "attendee" , all: i am host+ presenter+creater
#######################
class C0005_ErrorCode_Xserver_ForPC(projectx_base):
    def __init__(self,sipMethod="",testnum="",role=""):
        self.sipMethod = sipMethod
        self.testnum = testnum
        self.role = role
    def OnSetUp(self):
        pass
    def OnTearDown(self):
        pass
    def OnError(self):
        pass
    def OnFail(self):
        pass
    def OnRun(self):
        a = xserver_Exceptional_Common(self.sipMethod,self.testnum,self.role)
        a.startXServer()
class runCase():
    def __init__(self,pythonExeDir):
        if pythonExeDir != 'python':
            if not os.path.exists(pythonExeDir):
                sys.exit(1)
        self.runEXE = pythonExeDir
        self.path = os.path.abspath(os.curdir)
#         self.path = os.path.abspath(currentPath + '..\..\..\..\TestCases\projectX')

    def cycleRun(self):
        r=re.compile("M\d{2,}") #match the path
        pathlist=[]
        for temp in os.listdir(self.path):
            if r.search(temp) is not None:
                tpath=os.path.join(self.path,temp)
                if os.path.exists(tpath):
                    pathlist.append(tpath)
#                 sys.exit(1)
        if len(pathlist) <= 0:
            print ("no test cases need run, please check the filename,should be :MXX")
            sys.exit(1)
        print "Script will run these cases:\n%s "%(pathlist)
        print "please chooise if or not to run them[y/n]:"
        ok=raw_input()
        if ok in ('y','ye','yes'): 
            print "start to tun"
        elif ok in ('n','no','nop','nope'): sys.exit(1)
        else: raise IOError,'bad input! exit'
   
        for case in pathlist:
            print case
            timetmpstart = time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime( time.time()-5 )) 
            print "the case %s start time is %s" % (case,timetmpstart)
            cmd = "%s %s" % (self.runEXE,case)
            print cmd
            p = subprocess.Popen(cmd,shell=False)
            p.wait()
            if p.returncode != 0:
                print "Error."
                return -1  
            log = p.communicate()
            print log

def testMaxTcpConnection(looptime):
    success = 0
    failed = 0
    testtime = 0
    starttime = datetime.datetime.now()
    print "test Start Time = %s" % str(starttime)
    destserver_address = "54.223.151.142"
    destserver_port = "30000"
    sendsock = []
    while testtime<=looptime:
        testtime = testtime +1
        sendsock.append(testtime)
        sendsock[testtime-1] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (destserver_address, int(destserver_port))
        try:
            a = sendsock[testtime-1].connect(server_address)
            sendsock[testtime-1].settimeout(3)
        except socket.error or socket.timeout:
            sendsock[testtime-1].close()
            sendsock[testtime-1] = 0
            failed = failed + 1
            print("failed, failed time = %d" % failed)
        success = success+1
        print("success, success time = %d"% (success-failed))
        time.sleep(0.02)

        endtime = datetime.datetime.now()
        usedtime = endtime - starttime
        if usedtime.seconds % 60 == 0:
            for i in (0,range(0,len(sendsock)-1)):
                if sendsock[testtime-1] != 0:
                    print "send server reply time = %s,socket = %s" % (str(i),str(sendsock[testtime-1]))
                    sendsock[testtime-1].sendall('OKOKOK')
    endtime = datetime.datetime.now()
    print "test Start Time = %s" % str(starttime)
    print "test End time = %s" % str(endtime)
    usedtime = endtime - starttime
    print "test used %s(seconds) time" % usedtime.seconds
    print "test used %s(microseconds) time" % usedtime.microseconds
    print("success time = %d"% (success-failed))
    print("failed time = %d"% (failed))
    while True:
        time.sleep(60)
        for i in (0,range(0,len(sendsock)-1)):
            if sendsock[testtime-1] != 0:
                print "send server reply time = %s,socket = %s" % (str(i),str(sendsock[testtime-1]))
                sendsock[testtime-1].sendall('OKOKOK')    

if __name__ == '__main__':
    signal.signal(signal.SIGINT, myhandle)
    ############ 以下参数必须设对 #################

# ##Project X server
#     SIP_SERVER_IP = "172.172.172.26"
#     SIP_SERVER_PORT = int(5060)
#     LOGIN_WEB_ACCOUNT = "a4@test.com"
#     LOGIN_WEB_ACCOUNT_PASSWORD = "111111"
#     WEB_SERVER_IP = "172.172.172.24"
#     WEB_SERVER_PORT = "80"
# ##Project X server info stop

# ipvideotalk Server infor
# for ipvideotalk,domain name must be: "pro-beta.ipvideotalk.com"|"domain1"|"domain2"|"pro.ipvideotalk.com"|"Org-SIP-Frankfurt-1302815344.us-west-2.elb.amazonaws.com"
    SIP_SERVER_IP = "xmeetings.ipvideotalk.com"
    SIP_SERVER_DOMAIN_NAME = "xmeetings.ipvideotalk.com"
#     SIP_SERVER_PORT = int(20000)
    SIP_SERVER_PORT = int(10080)
# ipvideotalk Server stop
    LOCAL_PC_RTP_PORT = int(10000)
    LOCAL_PC_PORT = int(5068)
########### end ######################### 
    MEETINNG_ROOM_ID = '78577655' ## MEETINNG_ROOM_ID 设置为空, 程序会直接调用 Web server的接口 创建一个会议
    MEETING_PASSWORD = '' ## MEETING_PASSWORD 和 MEETINNG_ROOM_ID 配套使用，如果MEETINNG_ROOM_ID为空，密码会自动从web获取
    SIP_ID_NUMBER = '7200' ## SIP_ID_NUMBER 如果为空，自动会调用    LOGIN_WEB_ACCOUNT 去web查询sipID，并使用
    SIP_ID_PASSWORD = '7200'
    WEBAPI_KEY_URL = "/user/voip" ## WEBAPI_KEY_URL 只为 WEBAPI的error code使用，从 -a 参数传入
    set_UserPassed_Global_Param()
    case = C0004_PC_Simulator()
#     case = C0007_ipvidotalk_loopcall()
#     case = C0001_ErrorCode_WebPageServer_ForPC()
#     case = C0005_ErrorCode_Xserver_ForPC("info",2,"all")
#     case= C0002_Xserver_API_Security_Test_full()
#     case = C0006_ipvidotalk_PC_Simulator()
    case.Run()
###

#     testMaxTcpConnection(1000)
print "bye!!!"

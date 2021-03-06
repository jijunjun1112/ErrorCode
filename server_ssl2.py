# ! /usr/bin/python
#coding=utf-8
#Author: Amanda Shan <chfshan@grandstream.cn>;jhai@grandstream.cn
import sys
import logging
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
import binascii
import array
import threading
import hashlib,md5
import json
import subprocess
from optparse import OptionParser
from base64 import b64encode, b64decode
from sys import argv
import ssl
#from OpenSSL import SSL
#from M2Crypto import RSA
#import HTMLTestRunner
from log_for_server import *
from projectx_base import *
from create_sipObject import *
from global_variables import *

def get_ip_address():
    localIP = socket.gethostbyname(socket.gethostname())
    return localIP

def exitScript():
    sys.exit()
def deleteconnection(item):  
    global connectionlist  
    del connectionlist['connection'+item]
def get_datalength(msg):  
    global g_code_length  
    global g_header_length          
    g_code_length = ord(msg[1]) & 127  
    received_length = 0;  
    if g_code_length == 126:  
        #g_code_length = msg[2:4]  
        #g_code_length = (ord(msg[2])<<8) + (ord(msg[3]))  
        g_code_length = struct.unpack('>H', str(msg[2:4]))[0]  
        g_header_length = 8  
    elif g_code_length == 127:  
        #g_code_length = msg[2:10]  
        g_code_length = struct.unpack('>Q', str(msg[2:10]))[0]  
        g_header_length = 14  
    else:  
        g_header_length = 6  
    g_code_length = int(g_code_length)  
    return g_code_length  
def parse_data(self,msg):  
        global g_code_length  
        g_code_length = ord(msg[1]) & 127  
        received_length = 0;  
        if g_code_length == 126:  
            g_code_length = struct.unpack('>H', str(msg[2:4]))[0]  
            masks = msg[4:8]  
            data = msg[8:]  
        elif g_code_length == 127:  
            g_code_length = struct.unpack('>Q', str(msg[2:10]))[0]  
            masks = msg[10:14]  
            data = msg[14:]  
        else:  
            masks = msg[2:6]  
            data = msg[6:]  
        i = 0  
        raw_str = ''   
        for d in data:  
            raw_str += chr(ord(d) ^ ord(masks[i%4]))  
            i += 1
#        print raw_str        
        return raw_str    

class Websocket(threading.Thread):
    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    def __init__( self,conn,remote, path="/"):
        
        threading.Thread.__init__(self)
#        self.localsock = sock
        self.loopsend = 0
        ########################
        self.errorCode_system = errorCodeSystem
        
        self.errorCode_Statuserror = {'1':'404','2':'505','3':'400','4':'500','5':'481','6':'403'}
#         self.errorCode_Statuserror = {'1':'404'}
        self.errorCode_noRespond = {'1':'timeout'}
#        self.sipMethod = sipMethod
        
#        if testnum == "":
#            testnum = 2
#        self.testnum = testnum
        self.infoReceivedTime = 0
        self.av_invite_totag = "NONE"
        self.call_id = "NONE"
#        self.role = role
        self.refreshTime = 2
        self.getalltime=1
#        self.conn = conn    
#        self.remote = remote  
#        self.path = path  
        self.buffer = ""  
        self.buffer_utf8 = ""  
        self.length_buffer = 0
        self.conn = conn    
        self.remote = remote  
        self.path = path  
        self.buffer = ""  
        self.buffer_utf8 = ""  
        self.length_buffer = 0 
        self.sipMethod=''
        if LOCAL_PC_IP=='' or LOCAL_PC_IP==None:
            self.localip=get_ip_address()
        else:
            self.localip=LOCAL_PC_IP
        self.localport=''
        self.dest_address=''
        self.dest_port=''
        self.localsock=''
        self.display_name=''
        self.role=''
        self.join_flag=0
        self.info_times=0
        self.message_times=0
    def sendMessage(self,message):  
        global connectionlist  
        message_utf_8 = message.encode('utf-8')  
        for connection in connectionlist.values():  
            back_str = []  
            back_str.append('\x81')  
            data_length = len(message_utf_8)  
            if data_length <= 125:  
                back_str.append(chr(data_length))  
            elif data_length <= 65535 :  
                back_str.append(struct.pack('b', 126))  
                back_str.append(struct.pack('>h', data_length))  
                #back_str.append(chr(data_length >> 8))  
                #back_str.append(chr(data_length & 0xFF))  
                #a = struct.pack('>h', data_length)  
                #b = chr(data_length >> 8)  
                #c = chr(data_length & 0xFF)  
            elif data_length <= (2^64-1):  
                #back_str.append(chr(127))  
                back_str.append(struct.pack('b', 127))  
                back_str.append(struct.pack('>q', data_length))  
                #back_str.append(chr(data_length >> 8))  
                #back_str.append(chr(data_length & 0xFF))        
            else :  
                print "error"          
            msg = ''  
            for c in back_str:  
                msg += c;  
            back_str = str(msg)   + message_utf_8#.encode('utf-8') 
            if back_str != None and len(back_str) > 0:    
                self.conn.write(back_str) 
    def send_BYE(self,sock,msg_info,index):
        
        hangup="X-Hangup: "+errorCodeSystem[str(index)][0]+"\r\n"
        ECode="X-ECode: "+errorCodeSystem[str(index)][1]+"\r\n"
        
        bye_request = "BYE sip:%s@%s;rtcweb-breaker=no;click2call=no;transport=ws;+g.oma.sip-im;ovid=asdfghjkl;ov-ob=lkjhgfdsa;ri=%s;options=010 SIP/2.0\r\n"%(msg_info.sipid_number, msg_info.invalid,msg_info.local_ip_number)
        bye_request += "Via: SIP/2.0/WS %s:10080;branch=z9hG4bKyIWsI4MGBGLZaDtX4Cs9l0MVqPsFgZ;rport\r\n"%msg_info.local_ip_number
        bye_request += "To: <sip:%s@webrtc.grandstream.com>;tag=%s\r\n"%(msg_info.sipid_number,from_tag)
        bye_request += "From: <sip:%s@127.0.0.1>;tag=20150101000000\r\n"%(msg_info.meeting_id_to_user)
        bye_request += "Call-ID: %s\r\n"%call_id
        bye_request += "CSeq: 103 BYE\r\n"
        bye_request += "Server:python\r\n"
        bye_request += hangup
        bye_request += ECode        
        bye_request += "X-Channel-User-Id: %s\r\n"%msg_info.sipid_number
        bye_request += "X-Channel-Conf-Id: %s\r\n"%msg_info.meeting_id_to_user
        bye_request += "X-Gs-Server-Id: %s\r\n"%msg_info.local_ip_number
        bye_request += "Content-Length: 0\r\n\r\n"
        self.sendMessage(bye_request)
        log('info',"line%s:Say GoodBye to the girl"%sys._getframe().f_lineno)
        log('debug',"line%s:The content of the BYE:\r\n%s"%(sys._getframe().f_lineno,bye_request))
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1

    def send_INFO_response_200(self,sock,buffer,msg_info):
        ok_response = "SIP/2.0 200 OK\r\n"
        ok_response += msg_info.via_header + "\r\n"
        if self.compare_string(msg_info.snd_via_header, 'NONE') != 0:
            ok_response += msg_info.snd_via_header + "\r\n"
        if msg_info.hastotag == True:
            ok_response += "To :%s"%msg_info.to_header + "\r\n"
        else:
            ok_response += "To: %s"%msg_info.to_header + ";tag=201203271"+"\r\n"   
            msg_info.totag = "201203271"
        ok_response += "From: %s"%msg_info.from_header + "\r\n"
        ok_response += "Call-ID: %s\r\n" % msg_info.call_id
        ok_response += "CSeq: %s\r\n" %msg_info.cseq
        ok_response += "X-Gs-Conf-Control-Action-Result: OK\r\n"
        ok_response += "Server: python\r\n"
        expiresindex1 = msg_info.expires_header.find('NONE')
        if expiresindex1 == -1:
            ok_response += "%s\r\n"%msg_info.expires_header
        ok_response += "Content-Length: 0\r\n\r\n"
        self.sendMessage(ok_response)
        log('info',"line%s:Send 200OK to the INFO"%sys._getframe().f_lineno)
        log('debug',"line%s:The content of the 200OK:\r\n%s"%(sys._getframe().f_lineno,ok_response))
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1
        return True

    def compare_string(self,buffer1, buffer2):
        #print "[%s][%s]"%(buffer1, buffer2)
        result = int(buffer1.find(buffer2))
        if result != -1:
            result = int(buffer2.find(buffer1))
            if result != -1:
                return 0
        return 1

    # add by junjunji
    def send_INVITE_response_200(self,sock, msg_info):
        
        sdp_content =  "v=0\r\n"
        sdp_content += "o=root 176267762 176267762 IN IP4 {localIP}\r\n"
        sdp_content += "s=GrandStream X-Server 1.0.2.6 (M)\r\n"
        sdp_content += "c=IN IP4 {localIP}\r\n"
        sdp_content += "t=0 0\r\n"
        sdp_content += "m=audio 48888 RTP/SAVPF 9 0 8 3\r\n"
        sdp_content += "a=rtpmap:9 G722/8000\r\n"
        sdp_content += "a=rtpmap:0 PCMU/8000\r\n"
        sdp_content += "a=rtpmap:8 PCMA/8000\r\n"
        sdp_content += "a=rtpmap:3 GSM/8000\r\n"
        sdp_content += "a=maxptime:150\r\n"
        sdp_content += "a=ice-ufrag:66bc032d5162cf772b4a77b004e291e2\r\n"
        sdp_content += "a=ice-pwd:6a913b70289bde762512c5e34495e139\r\n"
        sdp_content += "a=candidate:Hacacac06 1 UDP 2130706431 {localIP} 48888 typ host\r\n"
        sdp_content += "a=candidate:Hacacac06 2 UDP 2130706430 {localIP} 48889 typ host\r\n"
        sdp_content += "a=connection:new\r\na=setup:passive\r\n"
        sdp_content += "a=fingerprint:sha-256 67:04:9D:03:6D:64:FA:31:2C:83:B1:4F:90:8F:E4:33:5D:F1:A4:F8:6C:59:8D:38:B7:DA:94:7F:92:73:52:BE\r\n"
        sdp_content += "a=sendrecv\r\n"
        sdp_content=sdp_content.format(localIP=msg_info.local_ip_number)
    
        ok_response = "SIP/2.0 200 OK\r\n"
        ok_response += msg_info.via_header + "\r\n"
        if self.compare_string(msg_info.snd_via_header, 'NONE') != 0:
            ok_response += msg_info.snd_via_header + "\r\n"
        if self.compare_string(msg_info.third_via_header, 'NONE') != 0:
            ok_response += msg_info.third_via_header + "\r\n"
        ok_response +="Record-Route: <sip:%s:5060;transport=udp;lr>\r\n"%msg_info.local_ip_number
        ok_response +="Record-Route: <sip:127.0.0.1:5060;transport=tcp;lr>\r\n"
        ok_response +="Record-Route: <sip:127.0.0.1:6060;transport=tcp;lr;ovid=asdfghjkl>\r\n"
        ok_response +="Record-Route: <sip:lkjhgfdsa@%s:10080;transport=ws;lr;ovid=asdfghjkl>\r\n"%msg_info.local_ip_number
        ok_response +="X-Conf-Serial-No: 24FC31292C5A42BC9B0A3B06D8EA5267\r\n"
        ok_response +="X-Conf-User-Id: 8200433\r\n"
        ok_response +="X-Conf-Id: %s\r\n"%msg_info.meeting_id_to_user
        ok_response +="X-GS-SERVER-ID: d+E3zQ/tUz6D8kHdXwOKQC+gSmpXjHKaTRbpUkBycXZHq/0JMhfpwQ+N05tv\r\n"
        
        ok_response += "Contact: <sip:%s@%s:5062>\r\n" % (msg_info.meeting_id_to_user,msg_info.local_ip_number)
        ok_response += "Server: GrandStream X-Server 1.0.2.6 (M)\r\n"
        
        ok_response +="Allow: INVITE,ACK,CANCEL,OPTIONS,BYE,REFER,SUBSCRIBE,NOTIFY,INFO,PUBLISH,MESSAGE,UPDATE\r\n"
        if msg_info.hastotag == True:
            ok_response += "To: %s"%msg_info.to_header + "\r\n"
        else:
            ok_response += "To: %s;tag=20150101000000\r\n"%(msg_info.to_header)
            
        ok_response += "From: %s\r\n"%msg_info.from_header
        ok_response += "Call-ID: %s\r\n" % msg_info.call_id
        ok_response += "CSeq: %s\r\n" %msg_info.cseq
    
        if self.compare_string(msg_info.sessionExpires, 'NONE') != 0:
#             ok_response += "Session-Expires: %s\r\n" %msg_info.sessionExpires
            ok_response += "Session-Expires: 600\r\n" 
        if self.compare_string(msg_info.minSE, 'NONE') != 0:
            ok_response += "Min-SE: %s\r\n" %msg_info.minSE
    
        if self.compare_string(msg_info.supported, 'NONE') != 0:
            ok_response += "Supported: %s,replaces\r\n" %msg_info.supported
    
        if self.compare_string(msg_info.requires, 'NONE') != 0:
            ok_response += "Require: %s\r\n" %msg_info.requires
        ok_response +="Require: timer\r\n"
        ok_response += "Content-Type: %s\r\n"%msg_info.contentType    
        ok_response += "Content-Length: %d\r\n\r\n"%(len(sdp_content))
        ok_response += sdp_content
        self.sendMessage(ok_response)
        log('info',"line%s:Send 200OK to the INVITE"%sys._getframe().f_lineno)
        log('debug',"line%s:The content of the 200OK:\r\n%s"%(sys._getframe().f_lineno,ok_response))            
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1
        return True

    # add by junjunji    
    def send_response_error(self,sock, msg_info,index): 
        
        FirstLine="SIP/2.0 "+errorCodeSystem[str(index)][0]+"\r\n"
        ECode="X-ECode: "+errorCodeSystem[str(index)][1]+"\r\n"
                     
        ok_response = FirstLine
        ok_response += msg_info.via_header + "\r\n"
        ok_response += "From: %s\r\n"%msg_info.from_header
        if msg_info.hastotag == True:
            ok_response += "To: %s"%msg_info.to_header + "\r\n"
        else:
            ok_response += "To: %s;tag=20150101000000\r\n"%(msg_info.to_header)
        ok_response += "Call-ID: %s\r\n" % msg_info.call_id
        ok_response += "CSeq: %s\r\n" %msg_info.cseq
        ok_response += ECode #1014,1015,1016,1017
        ok_response += "Content-Length: 0\r\n\r\n"           
        
        self.sendMessage(ok_response)
        log('debug',"line%s:The content of the error status:\r\n%s"%(sys._getframe().f_lineno,ok_response))            
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1
        return True
    
    # add by junjunji
    def send_MESSAGE_response_200(self,sock, msg_info):
        ok_response = "SIP/2.0 200 OK\r\n" 
        ok_response += msg_info.via_header + "\r\n"
        if self.compare_string(msg_info.snd_via_header, 'NONE') != 0:
            ok_response += msg_info.snd_via_header + "\r\n"
        if msg_info.hastotag == True:
            ok_response += "To: %s"%msg_info.to_header + "\r\n"
        else:
            ok_response += "To: %s"%msg_info.to_header + ";tag=20160427"+"\r\n"
            msg_info.totag = "20160427"
        ok_response += "From: %s"%msg_info.from_header + "\r\n"
        ok_response += "Call-ID: %s\r\n" %msg_info.call_id
        ok_response += "CSeq: %s\r\n" %msg_info.cseq
        expiresindex1 = msg_info.expires_header.find('NONE')
        if expiresindex1 == -1:
            ok_response += "%s\r\n"%msg_info.expires_header
        ok_response += "Server: python\r\n"
        ok_response += "Content-Length: 0\r\n\r\n"
       
        self.sendMessage(ok_response)
        log('info',"line%s:Send 200OK to the message request"%sys._getframe().f_lineno)
        log('debug',"line%s:The content of the response:\r\n%s"%(sys._getframe().f_lineno,ok_response))
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1
        return True
        
    def send_register_response_200(self,sock, buffer, msg_info): 
        ok_response = "SIP/2.0 200 OK\r\n"
        ok_response += msg_info.via_header + "\r\n"
        if self.compare_string(msg_info.snd_via_header, 'NONE') != 0:
            ok_response += msg_info.snd_via_header + "\r\n"
        ok_response += "Contact: <sip:reg@%s;rtcweb-breaker=no;click2all=no;transport=ws;+g.oma.sip-im;ovid=asdfghjkl;ri=%s;options=010>;expires=180\r\n"%(msg_info.invalid,msg_info.local_ip_number)
        if msg_info.hastotag == True:
            ok_response += "To :%s"%msg_info.to_header + "\r\n"
        else:
            ok_response += "To: %s"%msg_info.to_header + ";tag=201203271"+"\r\n"   
            msg_info.totag = "201203271"
        ok_response += "From: %s"%msg_info.from_header + "\r\n"
        ok_response += "Call-ID: %s\r\n" % msg_info.call_id
        ok_response += "CSeq: %s\r\n" %msg_info.cseq
        ok_response += "Path: <sip:127.0.0.1:6060;transport=udp;lr;ovid=asdfghjkl>\r\n"
        ok_response += "Path: <sip:lkjhgfdsa@%s:10080;transport=ws;lr;ovid=asdfghjkl;ob>\r\n"%msg_info.local_ip_number
        ok_response += "Server: python\r\n"
        expiresindex1 = msg_info.expires_header.find('NONE')
        if expiresindex1 == -1:
            ok_response += "%s\r\n"%msg_info.expires_header
        ok_response += "Content-Length: 0\r\n\r\n"
        self.sendMessage(ok_response)
        log('info',"line%s:Send 200OK to the REGISTER"%sys._getframe().f_lineno)
        log('debug',"line%s:The content of the 200OK:\r\n%s"%(sys._getframe().f_lineno,ok_response))
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1
        return True

    def send_response_errorcode(self,sock, buffer, msg_info):
#         ok_response = "SIP/2.0 403 Forbidden\r\n"      
        ok_response = "SIP/2.0 480 All Occupied\r\n" 
        ok_response += msg_info.via_header + "\r\n"
        if self.compare_string(msg_info.snd_via_header, 'NONE') != 0:
            ok_response += msg_info.snd_via_header + "\r\n"
        if msg_info.hastotag == True:
            ok_response += "To: %s"%msg_info.to_header + "\r\n"
        else:
            ok_response += "To: %s"%msg_info.to_header + ";tag=201203271"+"\r\n"
            msg_info.totag = "201203271"
        ok_response += "From: %s"%msg_info.from_header + "\r\n"
        ok_response += "Call-ID: %s\r\n" %msg_info.call_id
        ok_response += "CSeq: %s\r\n" %msg_info.cseq
#         ok_response += "X-Ecode: 1022\r\n"
        ok_response += "X-ECode: 1014\r\n"
        expiresindex1 = msg_info.expires_header.find('NONE')
        if expiresindex1 == -1:
            ok_response += "%s\r\n"%msg_info.expires_header
        ok_response += "Content-Length: 0\r\n\r\n"
        self.sendMessage(ok_response)
        log('info',"line%s:Send response to the request"%sys._getframe().f_lineno)
        log('debug',"line%s:The content of the response:\r\n%s"%(sys._getframe().f_lineno,ok_response))
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1
        return True
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
        self.sendMessage(ack_request)
        log('info',"line%s:Send ACK to the 200OK"%sys._getframe().f_lineno)
        logging.debug("The content of the ACK:\r\n%s"%ack_request)
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1
        return True

    def send_invite(self,sock,msg_info): #not used
        msg_info = self.checkAndInitData(sock, msg_info)
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
        self.sendMessage(invite_request)           
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1

    def parse(self,text):
        """Parses the incoming SUBSCRIBE."""
        try:
            lines = text.split('\r\n')
            # Line 1 conatains the SUBSCRIBE and our MAC
            msg = create_sipObject(pkt=text)
            result = int(lines[0][0:7].find('SIP/2.0'))
            if result == -1:
                msg.msg_isReq = True
            else:
                msg.msg_isReq == False
            if msg.msg_isReq == False:
                temp_buffer = lines[0].split(' ')
                msg.statusCode = int(temp_buffer[1])
                msg.statusPhase = temp_buffer[2]
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
            lineindex = self.get_headerline_by_name(text, "Via")
            if lineindex == 0:
                return None          
            msg.via_header = lines[lineindex]
            b=str(msg.via_header).split(';')
            c=str(b[0])
            d=c.split()
            msg.invalid=d[2]      
            result = int(msg.via_header.find(";branch="))
            if result != -1:
                temp_buffer_list =  msg.via_header[result + 8:].split(';')
                msg.branchStr = temp_buffer_list[0].strip()
            
#             lineindex = self.get_snd_via_header(text)
            lineindex = self.get_headerline_by_name(text,"Via",1)            
            if lineindex > 1:
                msg.snd_via_header = lines[lineindex]
            
#             lineindex = self.get_third_via_header(text)
            lineindex = self.get_headerline_by_name(text,"Via",2)
            if lineindex > 1:
                msg.third_via_header = lines[lineindex]
            lineindex = self.get_headerline_by_name(text, "From")
            if lineindex == 0:
                return None
            temp_buffer_list = lines[lineindex].split(':')
            msg.from_header = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
#            log('debug',"line%s:msg.from_header=%s"%(sys._getframe().f_lineno,msg.from_header))
            a=str(msg.from_header).split('<')
            msg.display_name=a[0]
            result = int(msg.from_header.find(";tag="))
            if result != -1:
                user_buffer =  msg.from_header[result + 5:].split(';')
                msg.fromtag = user_buffer[0]
            result = msg.from_header.find("@")
            if result != -1:
                user_buffer = msg.from_header.split('@')
#                 user_index = user_buffer[0].find('sip:')
                user_index = user_buffer[len(user_buffer)-2].find('sip:')
                if user_index == -1:
                    return None
                user_name = user_buffer[len(user_buffer)-2][user_index + 4:]
                msg.sipid_number = user_name.strip()
            else:
                user_index = msg.from_header.find('sip:')
                if user_index == -1:
                    return None
                msg.sipid_number = 'none'
            lineindex = self.get_headerline_by_name(text, "To")
            if lineindex == 0:
                return None
            temp_buffer_list = lines[lineindex].split(':')
            msg.to_header = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
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
                                    log('debug',"video sdp parse error"%sys._getframe().f_lineno)
                if msg.bHasBody == False:
                    sdp_index = text.find('\r\n\r\n')
                    if sdp_index != -1:
                        msg.body = text[sdp_index+4:]
                        msg.bHasBody = True        
        
            lineindex = self.get_headerline_by_name(text, "Refer-To")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.refer_to_header = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
            else:
                lineindex = self.get_headerline_by_name(text, "Refer-to")
                if lineindex > 0:
                    temp_buffer_list = lines[lineindex].split(':')
                    msg.refer_to_header = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
            lineindex = self.get_headerline_by_name(text, "Referred-By")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.referred_by_header = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
            lineindex = self.get_headerline_by_name(text, "Event")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.eventType = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
            lineindex = self.get_headerline_by_name(text, "Replaces")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.replaces = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
            
            lineindex = self.get_headerline_by_name(text, "Subscription-State")
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
            lineindex = self.get_headerline_by_name(text, "WWW-Authenticate")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.www_authenticate_header = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
                result = int(msg.www_authenticate_header.find('realm=\"'));
                if result != -1:
                    realm_string_1 = msg.www_authenticate_header[result+7:].split('"')
                    msg.realm = realm_string_1[0]
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
            lineindex = self.get_headerline_by_name(text, "X-GS-Conf-Control")
            if lineindex > 0:
                temp_buffer_list = lines[lineindex].split(':')
                msg.x_gs_conf_control = lines[lineindex][len(temp_buffer_list[0]) + 1:].strip()
            return msg
        except:
            log('error',"line%s:Can not parse the message,maybe it is not a sip message"%sys._getframe().f_lineno)
            return None
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
                logging.error("to user is empty or dest ip|port is empty")
                return False
            if msg_info.sipid_number == "" or msg_info.local_ip_number == "" or msg_info.local_port_number == "":
                logging.error("from user is empty or local ip|port is empty (checkInitData)")
                return False
            if sock =="":
                logging.error("Sock may create failed (checkInitData)")
                return False
            if msg_info.cseq_num == "":
                msg_info.cseq_num = XSERVER_PUBLICKEY["cseq_num_all"]
        except Exception as e:         
            logging.error("check data failed")
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
                
    def send_Nofity(self,sock,msg_info,flag=0):
#        if msg_info.rtp_media_port == "":
#            msg_info.rtp_media_port = self.rtp_port
#        if msg_info.user_agent == "":
#            msg_info.user_agent = 'windows'
        if msg_info.display_name == "":
            msg_info.display_name = self.display_name
        if msg_info.meeting_id_to_user == "":
            log('info',"meeting number is empty (send_invite)")
            self.OnError()
        # send INVITE request to sip server
        if msg_info.cseq_num == "":
            msg_info.cseq_num = XSERVER_PUBLICKEY["cseq_num_all"]
        #flag = 1(join meeting notify), flag = 2(start recording),flag=3(stop recording)
        notify_request = "NOTIFY sip:%s@%s;rtcweb-breaker=no;click2call=no;transport=ws;+g.oma.sip-im;ovid=asdfghjkl;ri=%s;options=010 SIP/2.0\r\n"%(msg_info.sipid_number,msg_info.invalid,msg_info.local_ip_number)
        if flag == 1: #when entering the confer
            park_content = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
            park_content +="<conference-info refresh=\"{refresh_times}\" entity=\"{confer_entity}\" state=\"partial\" s=\"1101100001110000\" options=\"10\">"
            park_content +="<users><user entity=\"{user_entity}\" state=\"full\" display={display_name} ua=\"Grandstream WebRTC/firefox 41.0\" type=\"5\" s=\"0111\" options=\"10\"/>"
            park_content +="</users></conference-info>" 
            park_content=park_content.format(refresh_times=self.refreshTime,
                                confer_entity=msg_info.meeting_id_to_user,
                                user_entity=str(msg_info.sipid_number),
                                display_name=msg_info.display_name)

            notify_request += "From:<sip:%s@%s:5060>;tag=20151106\r\n"%(msg_info.sipid_number,msg_info.local_ip_number)
            self.refreshTime += 1
            
        elif flag==0: #get all users
            notify_request += "From:<sip:%s@%s:5060>;tag=20151106\r\n"%(msg_info.meeting_id_to_user,msg_info.local_ip_number)
            park_content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><conference-info entity=\"%s\"  state=\"full\"  s=\"11001000011\"  options=\"10\"  maxusercount=\"100\"  usercount=\"30\"  maxmic=\"15\"  active=\"1\"  creater=\"8201002\"  host=\"8201002\"  presenter=\"8201002\"  mic_count=\"15\"  now_time=\"%s\"><users><user entity=\"8201002\"  state=\"full\"  display=\"I am the meeting host\" ua=\"Grandstream GVC3200 10.15.10.25\"  type=\"9\"  s=\"0011\"  options=\"10\"/><user entity=\"8211\"  state=\"full\"  display=\"python1\" ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8212\"  state=\"full\"  display=\"python2\" ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8213\"  state=\"full\"  display=\"python3\" ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8214\"  state=\"full\"  display=\"python4\" ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8215\"  state=\"full\"  display=\"python5\" ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8216\"  state=\"full\"  display=\"python6\" ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8217\"  state=\"full\"  display=\"python7\" ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8218\"  state=\"full\"  display=\"python8\" ua=\"python\"  type=\"1\"  s=\"0000\"  options=\"00\"/><user entity=\"8219\"  state=\"full\"  display=\"python9\"  ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8220\"  state=\"full\"  display=\"python10\" ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8221\"  state=\"full\"  display=\"python11\"  ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8222\"  state=\"full\"  display=\"python12\"  ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8223\"  state=\"full\"  display=\"python13\"  ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8224\"  state=\"full\"  display=\"python14\"  ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8225\"  state=\"full\"  display=\"python15\"  ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8226\"  state=\"full\"  display=\"python16\"  ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8227\"  state=\"full\"  display=\"python17\"  ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8228\"  state=\"full\"  display=\"python18\"  ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8229\"  state=\"full\"  display=\"python19\"  ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8230\"  state=\"full\"  display=\"python20\"  ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8231\"  state=\"full\"  display=\"python21\"  ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8232\"  state=\"full\"  display=\"python22\"  ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8233\"  state=\"full\"  display=\"python23\"  ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8234\"  state=\"full\"  display=\"python24\"  ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8235\"  state=\"full\"  display=\"python25\"  ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8236\"  state=\"full\"  display=\"python26\"  ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8237\"  state=\"full\"  display=\"python27\"  ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8238\"  state=\"full\"  display=\"python28\"  ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"%s\"  state=\"full\"  display=%s  ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"10\"/></users></conference-info>"%(str(msg_info.meeting_id_to_user),time.strftime('%Y%m%d%H%M%S'),msg_info.sipid_number,msg_info.display_name)       
        elif flag == 2:
            park_content = "<?xml version=\"1.0\" encoding=\"utf-8\"?><conference-info refresh=\"%s\" entity=\"%s\" state=\"partial\" s=\"11011000011\" share_type=\"0\"/>" %(self.refreshTime,str(msg_info.meeting_id_to_user))
            notify_request += "From:<sip:%s@%s:5060>;tag=20151106\r\n"%(msg_info.sipid_number,msg_info.local_ip_number)
            self.refreshTime += 1
        elif flag == 3:
            park_content = "<?xml version=\"1.0\" encoding=\"utf-8\"?><conference-info refresh=\"%s\" entity=\"%s\" state=\"partial\" s=\"11011000011\" share_type=\"0\"/>" %(self.refreshTime,str(msg_info.meeting_id_to_user))
            self.refreshTime += 1
            notify_request += "From:<sip:%s@%s:5060>;tag=20151106\r\n"%(msg_info.sipid_number,msg_info.local_ip_number)
        elif flag == 4:
            park_content = "<?xml version=\"1.0\" encoding=\"utf-8\"?><conference-info refresh=\"%s\" entity=\"%s\" state=\"partial\"><users><user entity=\"%s\" state=\"partial\" s=\"1011\"/></users></conference-info>" %(self.refreshTime,msg_info.meeting_id_to_user,str(msg_info.sipid_number))
            self.refreshTime += 1
            notify_request += "From:<sip:%s@%s:5060>;tag=20151106\r\n"%(msg_info.sipid_number,msg_info.local_ip_number)
        elif flag ==5:
#            park_content = "<?xml version=\"1.0\" encoding=\"utf-8\"?><conference-info refresh=\"%s\" entity=\"%s\" state=\"partial\"><users><user entity=\"8239\" state=\"partial\" s=\"1011\"/></users></conference-info>" %(self.refreshTime,msg_info.meeting_id_to_user)
            park_content = "<?xml version=\"1.0\" encoding=\"utf-8\"?><conference-info refresh=\"%s\" entity=\"%s\" state=\"partial\" s=\"11001000011\" options=\"00\"><users><user entity=\"8239\" state=\"full\" display=\"hello girl\" ua=\"python\" type=\"9\" s=\"0011\" options=\"00\"/></users></conference-info>" %(self.refreshTime,msg_info.meeting_id_to_user)
            notify_request += "From:<sip:8239@%s:5060>;tag=20151106\r\n"%msg_info.local_ip_number
            self.refreshTime += 1
        elif flag ==6:
            park_content = "<?xml version=\"1.0\" encoding=\"utf-8\"?><conference-info refresh=\"%s\" entity=\"%s\" state=\"partial\" s=\"11011000011\" options=\"00\" time=\"%s_20161110061340\"><users><user entity=\"8201002\" state=\"full\" display=\"I am the host\" ua=\"Grandstream GVC3200 10.15.10.25\" type=\"9\" s=\"0011\" options=\"00\"/></users></conference-info>" %(self.refreshTime,msg_info.meeting_id_to_user,time.strftime('%Y%m%d%H%M%S'))
            notify_request += "From:<sip:8201002@%s:5060>;tag=20151106\r\n"%msg_info.local_ip_number
            self.refreshTime += 1
        elif flag==7:
            notify_request += "From:<sip:%s@%s:5060>;tag=20151106\r\n"%(msg_info.meeting_id_to_user,msg_info.local_ip_number)
            park_content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><conference-info entity=\"%s\"  state=\"full\"  s=\"11001000011\"  options=\"00\"  maxusercount=\"100\"  usercount=\"31\"  maxmic=\"15\"  active=\"1\"  creater=\"8201002\"  host=\"8201002\"  presenter=\"8201002\"  mic_count=\"15\"  now_time=\"%s\"  start_time=\"%s\"  time=\"%s_20151110061340\"><users><user entity=\"8201002\"  state=\"full\"  display=\"I am the meeting host\" ua=\"Grandstream GVC3200 10.15.10.25\"  type=\"9\"  s=\"0011\"  options=\"00\"/><user entity=\"8211\"  state=\"full\"  display=\"python1\" ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8212\"  state=\"full\"  display=\"python2\" ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8213\"  state=\"full\"  display=\"python3\" ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8214\"  state=\"full\"  display=\"python4\" ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8215\"  state=\"full\"  display=\"python5\" ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8216\"  state=\"full\"  display=\"python6\" ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8217\"  state=\"full\"  display=\"python7\" ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8218\"  state=\"full\"  display=\"python8\" ua=\"python\"  type=\"1\"  s=\"0000\"  options=\"00\"/><user entity=\"8219\"  state=\"full\"  display=\"python9\"  ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8220\"  state=\"full\"  display=\"python10\" ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8221\"  state=\"full\"  display=\"python11\"  ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8222\"  state=\"full\"  display=\"python12\"  ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8223\"  state=\"full\"  display=\"python13\"  ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8224\"  state=\"full\"  display=\"python14\"  ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8225\"  state=\"full\"  display=\"python15\"  ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8226\"  state=\"full\"  display=\"python16\"  ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8227\"  state=\"full\"  display=\"python17\"  ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8228\"  state=\"full\"  display=\"python18\"  ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8229\"  state=\"full\"  display=\"python19\"  ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8230\"  state=\"full\"  display=\"python20\"  ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8231\"  state=\"full\"  display=\"python21\"  ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8232\"  state=\"full\"  display=\"python22\"  ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8233\"  state=\"full\"  display=\"python23\"  ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8234\"  state=\"full\"  display=\"python24\"  ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8235\"  state=\"full\"  display=\"python25\"  ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8236\"  state=\"full\"  display=\"python26\"  ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/><user entity=\"8237\"  state=\"full\"  display=\"python27\"  ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8238\"  state=\"full\"  display=\"python28\"  ua=\"python\"  type=\"1\"  s=\"0001\"  options=\"00\"/><user entity=\"8239\"  state=\"full\"  display=\"python29\" ua=\"python\"  type=\"9\"  s=\"0001\"  options=\"00\"/><user entity=\"%s\"  state=\"full\"  display=%s  ua=\"python\"  type=\"1\"  s=\"0011\"  options=\"00\"/></users></conference-info>"%(str(msg_info.meeting_id_to_user),time.strftime('%Y%m%d%H%M%S'),time.strftime('%Y%m%d%H%M%S'),time.strftime('%Y%m%d%H%M%S'),msg_info.sipid_number,msg_info.display_name)            
        elif flag==8:
            park_content = "<?xml version=\"1.0\" encoding=\"utf-8\"?><conference-info refresh=\"%s\" entity=\"%s\" state=\"partial\"><users><user entity=\"%s\" state=\"partial\" s=\"0011\"/></users></conference-info>" %(self.refreshTime,msg_info.meeting_id_to_user,str(msg_info.sipid_number))
            self.refreshTime += 1
            notify_request += "From:<sip:%s@%s:5060>;tag=20151106\r\n"%(msg_info.sipid_number,msg_info.local_ip_number)            
        else:
            park_content = "<?xml version=\"1.0\" encoding=\"utf-8\"?><conference-info refresh=\"%s\" entity=\"%s\" state=\"partial\"><users><user entity=\"%s\" state=\"partial\" s=\"0011\"/></users></conference-info>" %(self.refreshTime,msg_info.meeting_id_to_user,str(msg_info.sipid_number))
            self.refreshTime += 1 
            notify_request += "From:<sip:%s@%s:5060>;tag=20151106\r\n"%(msg_info.sipid_number,msg_info.local_ip_number)       
        notify_request += "Via: SIP/2.0/WS %s:10080;branch=z9hG4bK1e3effada91dc37fd5a0c95cbf6767d2%d;rport\r\n"%(msg_info.local_ip_number,msg_info.cseq_num)
#        notify_request += "Via: SIP/2.0/UDP %s:5060;branch=z9hG4bK81c8.9e64ae84.1;received=%s:5060;rport=5060\r\n"%(msg_info.local_ip_number,msg_info.local_ip_number)
        notify_request += "Record-Route: <sip:lkjhgfdsa@%s:10080;transport=ws;lr;ovid=asdfghjkl>\r\n"%msg_info.local_ip_number
        notify_request += "Record-Route: <sip:127.0.0.1:6060;transport=udp;lr;ovid=asdfghjkl>\r\n"
        notify_request += "To: <sip:%s@%s:5060>\r\n"%(msg_info.meeting_id_to_user,msg_info.local_ip_number)
#        if msg_info.hastotag == True:
#            notify_request += "From: %s\r\n"%msg_info.to_header
#        else:
#            notify_request += "From: %s;tag=201203271\r\n"%msg_info.to_header
        notify_request += "Call-ID: d39b69ff-4ba9-6fb8-ac8b-55c457c2f%s\r\n"%(random.randint(0, 10000))
#        notify_request += "Max-Forwards: 69\r\n"
#        notify_request += "User-Agent: conference\r\n" 
        notify_request += "Event: X-GS-CONFERENCE\r\n"
        notify_request += "X-GS-Notify-Users: all\r\n"
#        notify_request += "X-Gs-Server-Id: %s\r\n"%msg_info.local_ip_number
        notify_request += "Content-Type: application/conference-info+xml\r\n"
        notify_request += "CSeq: 1000 NOTIFY\r\n"
        notify_request += "Content-Length: %d\r\n\r\n" % (len(park_content))
        notify_request += park_content
        self.sendMessage(notify_request)
        log('info',"line%s:Send NOTIFY to the girl"%sys._getframe().f_lineno)
        log('debug',"line%s:The content of the NOTIFY:\r\n%s"%(sys._getframe().f_lineno,notify_request))
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1
        return True

    def send_av_invite(self,sock,msg_info):
        if msg_info.rtp_media_port == "":
            msg_info.rtp_media_port = self.rtp_port
        if msg_info.user_agent == "":
            msg_info.user_agent = 'windows'
        if msg_info.display_name == "":
            msg_info.display_name = self.display_name
        if msg_info.meeting_id_to_user == "":
            log('info',"meeting number is empty (send_invite)")
            self.OnError()
        # send INVITE request to sip server
        if sock =="":
            sock = self.localsock
        if msg_info.cseq_num == "":
            msg_info.cseq_num = XSERVER_PUBLICKEY["cseq_num_all"]
#         sdp_content = "v=0\r\no=root 865661064 865661064 IN IP4 %s\r\ns=SIP Call\r\nc=IN IP4 %s\r\nt=0 0\r\nm=audio %d RTP/AVP 0 101\r\na=sendrecv\r\na=rtpmap:0 PCMU/8000\r\na=ptime:20\r\na=rtpmap:101 telephone-event/8000\r\na=fmtp:101 0-15"%(msg_info.local_ip_number, msg_info.local_ip_number, msg_info.rtp_media_port)
#         sdp_content += "\r\na=maxptime:150\r\na=sendrecv\r\nm=video 29116 RTP/AVP 31 34 98 99 104 100\r\na=rtpmap:31 H261/90000\r\na=rtpmap:34 H263/90000\r\na=rtpmap:98 h263-1998/90000\r\na=rtpmap:99 H264/90000\r\na=rtpmap:104 MP4V-ES/90000\r\na=rtpmap:100 VP8/90000\r\na=rtcp-fb:* ccm fir\r\na=sendrecv"
        sdp_content = "v=0\r\no=root 1100670332 1100670333 IN IP4 %s\r\ns=GrandStream X-Server 0.0.0.41 (M)\r\nc=IN IP4 %s\r\nb=CT:384\r\nt=0 0\r\nm=audio 47566 RTP/SAVPF 9 0 8 3\r\na=rtpmap:9 G722/8000\r\na=rtpmap:0 PCMU/8000\r\na=rtpmap:8 PCMA/8000\r\na=rtpmap:3 GSM/8000\r\na=maxptime:150\r\na=ice-ufrag:6fce635a2975c3242b8d15c565f6765e\r\na=ice-pwd:26be079e1696e5ae302cd019190629a7\r\na=candidate:Hacacac06 1 UDP 2130706431 %s 47566 typ host\r\na=candidate:Hacacac06 2 UDP 2130706430 %s 47567 typ host\r\na=connection:existing\r\na=setup:active\r\na=fingerprint:sha-256 67:04:9D:03:6D:64:FA:31:2C:83:B1:4F:90:8F:E4:33:5D:F1:A4:F8:6C:59:8D:38:B7:DA:94:7F:92:73:52:BE\r\na=sendrecv\r\nm=video 48970 RTP/SAVPF 105 100\r\na=ice-ufrag:0249719f47a3474975bde9d001fa6e66\r\na=ice-pwd:6778a62517c87da67d285e2b4bdff28b\r\na=candidate:Hacacac06 1 UDP 2130706431 %s 48970 typ host\r\na=candidate:Hacacac06 2 UDP 2130706430 %s 48971 typ host\r\na=connection:new\r\na=setup:active\r\na=fingerprint:sha-256 67:04:9D:03:6D:64:FA:31:2C:83:B1:4F:90:8F:E4:33:5D:F1:A4:F8:6C:59:8D:38:B7:DA:94:7F:92:73:52:BE\r\na=rtpmap:105 H264/90000\r\na=fmtp:105 profile-level-id=42e01f;level-asymmetry-allowed=1;packetization-mode=1\r\na=rtpmap:100 VP8/90000\r\na=rtcp-fb:* ccm fir\r\na=sendrecv\r\n" %(msg_info.local_ip_number,msg_info.local_ip_number,msg_info.local_ip_number,msg_info.local_ip_number,msg_info.local_ip_number,msg_info.local_ip_number)
        if msg_info.meeting_pw == "NONE" or msg_info.meeting_pw == "":
            invite_request = "INVITE sip:%s@%s SIP/2.0\r\n"%(msg_info.meeting_id_to_user, msg_info.local_ip_number)
        else:
            invite_request = "INVITE sip:%s*%s@%s SIP/2.0\r\n"%(msg_info.meeting_id_to_user, msg_info.meeting_pw, msg_info.local_ip_number)
        if msg_info.protocol == 'udp':
            invite_request += "Via: SIP/2.0/UDP %s:%d;branch=z9hG4bK12345678%x;rport;alias"%(msg_info.local_ip_number,msg_info.local_port_number, random.randint(0, 10000)) + "\r\n"
            invite_request += "Contact: <sip:" + msg_info.sipid_number + "@" + msg_info.local_ip_number + ":" + "%d"%msg_info.local_port_number + ";transport=udp>\r\n"
        else:
            invite_request += "Via: SIP/2.0/TCP %s:5060;branch=z9hG4bK12345678%x"%(msg_info.local_ip_number, random.randint(0, 10000)) + "\r\n"
            invite_request += "Via: SIP/2.0/UDP %s:5062;received=%s;branch=z9hG4bK12345678%x;rport=5062"%(msg_info.local_ip_number,msg_info.local_ip_number, random.randint(0, 10000)) + "\r\n"
            invite_request += "Contact: <sip:%s@%s:5062;transport=tcp>\r\n"%(str(msg_info.sipid_number), str(msg_info.local_ip_number))
        if msg_info.hastotag == True:
            if msg_info.meeting_pw == "NONE" or msg_info.meeting_pw == "":
                invite_request += "To: <sip:%s@%s:%s>;tag=%s\r\n"%(msg_info.meeting_id_to_user, msg_info.local_ip_number, msg_info.local_port_number, self.av_invite_totag)
            else:
                invite_request += "To: <sip:%s*%s@%s:%d>;tag=%s\r\n"%(msg_info.meeting_id_to_user, msg_info.meeting_pw, msg_info.local_ip_number, msg_info.local_port_number, self.av_invite_totag)
    
        else:
            if msg_info.meeting_pw == "NONE" or msg_info.meeting_pw == "":
                invite_request += "To: <sip:%s@%s>;tag=%s\r\n"%(msg_info.meeting_id_to_user, msg_info.local_ip_number,self.av_invite_totag)
            else:
                invite_request += "To: <sip:%s*%s@%s>;tag=%s\r\n"%(msg_info.meeting_id_to_user, msg_info.meeting_pw, msg_info.local_ip_number,self.av_invite_totag)
    
        invite_request += "From: <sip:%s@%s>;tag=%s\r\n"%(msg_info.sipid_number, msg_info.local_ip_number, "201203271")
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
#         invite_request += "P-Preferred-Identity: \"%s\" <sip:"%(str(msg_info.display_name)) + str(msg_info.sipid_number) + "@" + str(msg_info.dest_ip_number) + ">\r\n"
        invite_request += "Supported: replaces, path, timer, eventlist\r\n"
        invite_request += "Allow: INVITE, ACK, OPTIONS, CANCEL, BYE, SUBSCRIBE, NOTIFY, INFO, REFER, UPDATE, MESSAGE\r\n"
        invite_request += "Content-Type: application/sdp\r\n"
        invite_request += "Accept: application/sdp, application/dtmf-relay\r\n"
        invite_request += "X-GS-SERVER-ID: %s \r\n"%(msg_info.local_ip_number)
        invite_request += "Content-Length: %d\r\n\r\n"%(len(sdp_content))

        invite_request += sdp_content
        self.sendMessage(invite_request)
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1

    def send_av_stop_invite(self,sock,msg_info):
        if msg_info.rtp_media_port == "":
            msg_info.rtp_media_port = self.rtp_port
        if msg_info.user_agent == "":
            msg_info.user_agent = 'windows'
        if msg_info.display_name == "":
            msg_info.display_name = self.display_name
        if msg_info.meeting_id_to_user == "":
            log('info',"meeting number is empty (send_invite)")
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
                log('error',"send request %s  failed,socket connect failed: %s(send_INVITE)") % (msg_info.call_id,str(e))
                self.OnError()
            
        XSERVER_PUBLICKEY["cseq_num_all"] = XSERVER_PUBLICKEY["cseq_num_all"] + 1

    def parseReceivedData( self, data, sipMethod):
        
        global LOOPTIMES_Xserver_errorCode
        global LOCAL_PC_PORT,LOCAL_PC_IP
        global from_tag,call_id,to_tag,join_flag
        global invite_times,register_times,bye_times
        
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
            log('info',"line%s:Receive %s request"%(sys._getframe().f_lineno,service_msg.msg_method))
            log('debug',"line%s:The content of the %s:\r\n%s"%(sys._getframe().f_lineno,service_msg.msg_method,data))                
            if str(service_msg.msg_method).lower() == "invite":                       
                
                if service_msg.totag == True:
                    self.infoReceivedTime = 0
                    
                self.send_INVITE_response_200(self.localsock, service_msg)
                
                for i in range(0,0):
                    if self.join_flag==0:
                        self.send_INVITE_response_200(self.localsock, service_msg)
                    else:
                        self.send_response_errorcode(self.localsock,None, service_msg)
#                        if self.join_flag==0:
#                            self.send_Nofity(self.localsock,service_msg,1)
#                            self.join_flag=1
                from_tag=service_msg.fromtag
                call_id=service_msg.call_id
                to_tag=service_msg.totag
                self.av_invite_totag = service_msg.fromtag
                self.call_id = service_msg.call_id
                
            elif str(service_msg.msg_method).lower() == "ack":
                bye_times=bye_times+1
                if bye_times>=2 and bye_times<=13:
                    self.send_BYE(self.localsock, service_msg,bye_times+46)
                    return
                
                if self.join_flag==0:
                    self.send_Nofity(self.localsock,service_msg,1)
                    log('info',"Join meeting success")
                    self.join_flag=1
                else:
                    log('info',"Session timer success")
            elif str(service_msg.msg_method).lower() == "info":
                
                self.info_times =self.info_times+1
                
                if (self.info_times>=3 and self.info_times<=30) or (self.info_times>=34 and self.info_times<=49) or (self.info_times==62): 
                    self.send_response_error(self.localsock,service_msg,self.info_times-2)
                    return 
                
#                 self.send_INFO_response_200(self.localsock,None, service_msg)

                if str(str(service_msg.x_gs_conf_control).find("ctrl_present")) != "-1":
                    if str(str(service_msg.x_gs_conf_control).find("present-status=1")) != "-1":
                        self.send_av_invite(self.localsock,service_msg)
                        self.send_Nofity(self.localsock,service_msg,2)
                    else:
                        self.send_av_stop_invite(self.localsock,service_msg)
                        self.send_Nofity(self.localsock,service_msg,3)
                        
                elif str(str(service_msg.x_gs_conf_control).find("get_all_users")) != "-1":
                    log('debug',"line%s:send response to the INFO"%sys._getframe().f_lineno)
                    self.send_INFO_response_200(self.localsock,None, service_msg)
                    time.sleep(0.5)
                    if self.getalltime==1:
                        self.send_Nofity(self.localsock,service_msg,0)
#                         self.send_av_invite(self.localsock, service_msg)
                        self.getalltime +=1
                    else:
                        self.send_Nofity(self.localsock, service_msg, 7)
                
                elif str(str(service_msg.x_gs_conf_control).find("mute")) != "-1":
                    self.send_INFO_response_200(self.localsock,None, service_msg)
                    if str(str(service_msg.x_gs_conf_control).find("mute-status=1")) != "-1":
                        self.send_Nofity(self.localsock,service_msg,4)
                    else:
                        self.send_Nofity(self.localsock,service_msg,8)
                        time.sleep(3)
                        self.send_Nofity(self.localsock, service_msg, 5)
                        time.sleep(3)
                        self.send_Nofity(self.localsock, service_msg, 3)
                        time.sleep(3)
                    
                else:
                    print "hello"
                    self.send_INFO_response_200(self.localsock,None, service_msg)
         #           self.send_Nofity(self.localsock,service_msg)
                
            elif str(service_msg.msg_method).lower() == "message":  
                self.send_MESSAGE_response_200(self.localsock,service_msg)
                
            elif str(service_msg.msg_method).lower() == "register":
                self.send_register_response_200(self.localsock,None, service_msg)

            elif str(service_msg.msg_method).lower() == "bye":
                log('info',"line%s:The girl leaves the meeting"%sys._getframe().f_lineno)
                
            else:
                if str(service_msg.msg_method).lower() == "invite":
                    if service_msg.statusCode == 200:
                        self.send_ACK_request(self.localsock, service_msg)
        else:
            log('info',"line%s:Receive %s response for %s"%(sys._getframe().f_lineno,service_msg.statusCode,service_msg.msg_method))
            log('debug',"line%s:Response content:\r\n%s"%(sys._getframe().f_lineno,data))
            if str(service_msg.msg_method).lower() == "invite" and service_msg.statusCode == 200:
                self.send_ACK_request(self.localsock, service_msg,service_msg.dest_ip_number,service_msg.dest_port_number)
                                 
    def run(self):
        headers = {}  
        self.handshaken = False  
        while True:  
            if self.handshaken == False:  
#                log('info',"line%s:Socket Start Handshaken with %s!"%(sys._getframe().f_lineno,self.remote))  
                self.buffer=self.conn.read() 
                if self.buffer.find('\r\n\r\n') != -1: 
                    header, data = self.buffer.split('\r\n\r\n', 1)  
                    for line in header.split("\r\n")[1:]:  
                        key, value = line.split(": ", 1)  
                        headers[key] = value  
                    headers["Location"] = ("ws://%s%s" %(headers["Host"], self.path))  
                    key = headers['Sec-WebSocket-Key']  
                    token = b64encode(hashlib.sha1(str.encode(str(key + self.GUID))).digest())  
                    handshake="HTTP/1.1 101 Switching Protocols\r\n"\
                        "Upgrade: websocket\r\n"\
                        "Connection: Upgrade\r\n"\
                        "Sec-WebSocket-Accept: "+bytes.decode(token)+"\r\n"\
                        "Sec-WebSocket-Protocol:sip\r\n"\
                        "Server:python\r\n\r\n"
                    try:
                        self.conn.write(str(handshake))  
                        self.handshaken = True    
                        log('info',"line%s:Socket Handshaken with %s success!"%(sys._getframe().f_lineno, self.remote))    
                        self.buffer_utf8 = ""  
                        g_code_length = 0 
                    except Exception as e:
                        log('info',"line%s:Socket Handshaken with %s failed!  %s") % (sys._getframe().f_lineno,str(e))                                       
            else:  
                global g_code_length  
                global g_header_length  
                mm=self.conn.read()  
                if len(mm) <= 0:  
                    continue
                if g_code_length == 0:  
                    get_datalength(mm)  
                #????????  
                self.length_buffer = self.length_buffer + len(mm)  
                self.buffer = self.buffer + mm  
                if self.length_buffer - g_header_length < g_code_length :  
                    continue  
                else :  
                    self.buffer_utf8 = parse_data(self,self.buffer) #utf8                  
                    msg_unicode = str(self.buffer_utf8).decode('utf-8', 'ignore') 
                    self.parseReceivedData(msg_unicode,self.sipMethod)
                    self.buffer_utf8 = ""  
                    self.buffer = ""  
                    g_code_length = 0  
                    self.length_buffer = 0  
            self.buffer = ""  
class WebSocketServer(object):
    def __init__(self,sipMethod="",testnum="",role="",localaddress = '',localport = ''):
        self.service_msg = create_sipObject()
        if LOCAL_PC_IP=='' or LOCAL_PC_IP==None:
            self.service_msg.local_ip_number=get_ip_address()
        else:
            self.service_msg.local_ip_number=LOCAL_PC_IP
        self.service_msg.local_port_number = localport
#        sipServer_commonlib.__init__(self,self.service_msg)
        if sipMethod == "":
            self.sipMethod = "info"
        else:
            self.sipMethod = sipMethod
        if testnum == "" or int(testnum)<=0:
            self.testnum = 1
        self.testnum = testnum
        self.role = role
    def begin(self):
        log('info',"line%s:WebSocketServer Start"%sys._getframe().f_lineno)
        serveraddr="%s"%self.service_msg.local_port_number  
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  
        self.socket.bind((serveraddr,10080))  
        self.socket.listen(50)  
        global connectionlist  
        i=0  
        while True: 
            connection, address = self.socket.accept()
            ssl_sock=ssl.wrap_socket(connection,
                     server_side=True,
                     certfile="test.pem",
                     keyfile="test.key",
                     ca_certs="test.pem")
            T1 = Websocket(ssl_sock,self.service_msg,self.sipMethod)
            T1.start()   
            connectionlist['connection'+str(i)]=connection  
#            i = i + 1 

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
    
    global WEBAPI_KEY_URL,MEETING_PASSWORD,MEETINNG_ROOM_ID
    
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
        a = WebSocketServer(self.sipMethod,self.testnum,self.role)
        a.begin()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, myhandle)
    SIP_SERVER_IP = ""
    SIP_SERVER_DOMAIN_NAME = "xmeetings.ipvideotalk.com"
    WEB_SERVER_IP = "api.ipvideotalk.com"
    WEB_SERVER_PORT = "80"
    SIP_SERVER_PORT = int(30000)
    LOCAL_PC_RTP_PORT = int(10000)
    LOCAL_PC_PORT = int(20000)
    LOCAL_PC_IP=""
    MEETINNG_ROOM_ID = '' ## MEETINNG_ROOM_ID ???????, ??????????? Web server???? ???????????
    MEETING_PASSWORD = '' ## MEETING_PASSWORD ?? MEETINNG_ROOM_ID ???????????MEETINNG_ROOM_ID??????????????web???
    SIP_ID_NUMBER = '' ## SIP_ID_NUMBER ???????????????xmeeting?????    LOGIN_WEB_ACCOUNT ?web???sipID???????
    SIP_ID_PASSWORD = ''
    WEBAPI_KEY_URL = "/xmeeting/user/voip" ## WEBAPI_KEY_URL ?? WEBAPI??error code?????? -a ????????
    set_UserPassed_Global_Param()
    case = C0005_ErrorCode_Xserver_ForPC()
    case.Run()
###

#     testMaxTcpConnection(1000)
print "bye!!!"

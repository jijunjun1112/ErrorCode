from distutils.command.build_scripts import first_line_re
First_Line=""
ECode=""
global LOCAL_PC_IP,LOCAL_PC_PORT
global MEETINNG_ROOM_ID,MEETING_PASSWORD
global VERBOSE,service_on
VERBOSE = 0   ## is open debug log
service_on = 1###############################################

global LOOPTIMES_webAPI_errorCode
LOOPTIMES_webAPI_errorCode = 1

global invite_times,register_times,bye_times
invite_times = 0
register_times = 0
bye_times=0

global SIP_SERVER_IP,SIP_SERVER_PORT

global XSERVER_PUBLICKEY
XSERVER_PUBLICKEY = {}.fromkeys(('cseq_num_all'),"NONE") # every sip command vi this key to parse
XSERVER_PUBLICKEY["cseq_num_all"] = 0

SESSIONINFO = []
LOOPTIMES_Xserver_errorCode = 1

global SIP_ID_NUMBER,SIP_ID_PASSWORD,LOCAL_PC_RTP_PORT
global INVITE_SDP
INVITE_SDP = {}.fromkeys(("ip","port1",'port2',"port3","port4","port5"),"NONE")
connectionlist = {}  
g_code_length = 0 
g_header_length = 0 

# add by junjunji
global errorCodeSystem
errorCodeSystem={'1':('400 Bad Request','1000'),\
             '2':('400 No Message Body','1001'),\
             '3':('400 Parse Error','1002'),\
             '4':('400 No User List Found','1003'),\
             '5':('403 Conference Forbidden','1004'),\
             '6':('500 Internal Error','1005'),\
             '7':('404 Dest Address Not Found','1006'),\
             '8':('404 Not Found','1007'),\
             '9':('404 Not Found','1008'),\
             '10':('404 Not Found','1009'),\
             '11':('404 Conference Not Found','1010'),\
             '12':('404 Dest Address Not Found','1011'),\
             '13':('404 Not Found','1012'),\
             '14':('404 Bad Conference ID','1013'),\
             '15':('480 Confroom User Amount Reaches Max Number','1014'),\
             '16':('480 Media Resource Unavailable','1015'),\
             '17':('480 Redis Operation Error','1016'),\
             '18':('480 Unknown Service','1017'),\
             '19':('481 Call Does Not Exist','1018'),\
             '20':('483 Too Many Hops','1019'),\
             '21':('500 Relay Error','1020'),\
             '22':('500 Redis Data Not Found','1021'),\
             '23':('500 Invalid Operation','1022'),\
             '24':('503 Conference Operation Error','1023'),\
             '25':('603 Conference Room Not Found','1024'),\
             '26':('603 Peer Not Found','1025'),\
             '27':('408 Time out','1026'),\
             '28':('403 Forbidden(Permission Denied)','1027'),\
             '29':('','1028'),\
             '30':('','1029'),\
             '31':('','1030'),\
             '32':('403 Forbidden','1031'),\
             '33':('503 Service Unavailable','1032'),\
             '34':('500 Other Account Conflict Processing','1033'),\
             '35':('503 Service Unavailable','1034'),\
             '36':('400 Bad Request','3000'),\
             '37':('487 Request Terminate(Not Support)','3001'),\
             '38':('403 Forbidden(Permission Denied)','3002'),\
             '39':('404 User Not Found','3003'),\
             '40':('500 Server Internal Error','3004'),\
             '41':('500 Server Internal Error','3005'),\
             '41':('500 Server Internal Error','3006'),\
             '42':('600 Server Busy Try Later','3007'),\
             '43':('606 Not Acceptable(Conference Max Num Limit)','3008'),\
             '44':('607 Not Acceptable(conference Host Not Exist)','3009'),\
             '45':('608 Not Found CDesktopRequest(No Speaker In Conf)','3010'),\
             '46':('600 Not Acceptable(Conference Host Already Exist)','3011'),\
             '47':('600 Not Acceptable(Mic Max Limit)','3012'),\
             '48':('Kicked By Host','5003'),\
             '49':('MCU Bridge Error','5004'),\
             '50':('MCU SetPresenter Error','5005'),\
             '51':('RS Get MCU Error','5006'),\
             '52':('RS Get Speaker Error','5007'),\
             '53':('Kicked By Web','5008'),\
             '54':('RS Proccess Error','5009'),\
             '55':('Conference Not Exist','5010'),\
             '56':('Conference full','5011'),\
             '57':('LockTimeOut','5012'),\
             '58':('LockRefuse','5013'),\
             '59':('Account Conflict in Conf','5014'),\
             '60':('500 Server Internal Error(Web Code 30008)','30008')}
     

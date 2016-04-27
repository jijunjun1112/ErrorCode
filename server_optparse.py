from optparse import OptionParser

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
#     parser.add_option("-a", "--exceptiontest of status code", action="store", dest="WEBAPI_KEY_URL", default=False, help="web api key url:/user/login")
    (options, args) = parser.parse_args()
    
#     global WEBAPI_KEY_URL
    global MEETING_PASSWORD,MEETINNG_ROOM_ID
    
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

#     if options.WEBAPI_KEY_URL:
#         WEBAPI_KEY_URL = options.WEBAPI_KEY_URL
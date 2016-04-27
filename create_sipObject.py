# ! /usr/bin/python
#coding=utf-8
class create_sipObject(object):
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
        self.invalid=''
        self.ovob=''
# ! /usr/bin/python
#coding=utf-8
#Author=jijunjun
import sys
import logging
import time

log_mode='info'
# log_mode='debug'
logging.basicConfig(level=logging.DEBUG,format='[%(asctime)s] [%(levelname)s] [%(filename)s] [line%(lineno)d]: %(message)s',datefmt='%Y%m%d%H%M%S',filename='E:\share\log_python\AvsTest.log',filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(filename)s] [line%(lineno)d]: %(message)s',datefmt='%Y%m%d%H%M%S')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
def log(level,log):
    if log_mode=='error':
        if level=='error':
            print "%s [%s] %s"%(time.strftime('%Y%m%d%H%M%S'),level,log)
        else:
            return
    elif log_mode=='info':
        if level=='error' or level=='info':
            print "%s [%s] %s"%(time.strftime('%Y%m%d%H%M%S'),level,log)
        else:
            return
    else:
        print "%s [%s] %s"%(time.strftime('%Y%m%d%H%M%S'),level,log)
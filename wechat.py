#/usr/bin/python
# coding=utf-8
#-------------------------------
#	Author: LSK
#	Filename: wechat.py
#	Datetime: 2018-7-5
#-------------------------------
import urllib2 as urllib
import json
import sys
import logging
import ConfigParser


logging.basicConfig(level=logging.DEBUG,filename='./logs/wechat.log',
                    format='%(asctime)s - %(levelname)s: %(message)s')

class Weixin:
    def __init__(self,flag,content):
        self.flag = flag
        self.content = content

    def send_message(self,url,data):

        send_url = "%s/cgi-bin/message/send?access_token=%s" %(url,self.token)
        self.response = urllib.urlopen(urllib.Request(url=send_url,data=data)).read()
        x = json.loads(self.response.decode())['errcode']
        if x==0 :
            logging.debug('Successfully %s ' % (data))
            return 'Successfully'
        else:
            logging.debug('Faild %s' % (data))
            return 'Failed'
    def message(self,touser):
        url = 'https://qyapi.weixin.qq.com/'
        cp = ConfigParser.SafeConfigParser()
        ap = ConfigParser.SafeConfigParser()
        cp.read('./config/wechat.conf')
        ap.read('./config/access_token.conf')
        config = cp.sections()
        access_config = ap.sections()
        agentname = 'test4'
        agentid = cp.get('test4', 'AgentId')
        self.token = ap.get('test4','AgentId')
        for i in config:
            if i !='http' and i!= 'weixin':
                value = cp.get('weixin',i)
                if self.flag == value:
                    agentname = i
                    agentid = cp.get(i, 'AgentId')
        for k in access_config:
            if k == agentname:
                self.token = ap.get(k,'access_token')

        values = {
            "touser": touser,
            "msgtype": 'text',
            "agentid": agentid,
            "text": {'content':self.content},
            "safe": 0
        }
        return self.send_message(url,json.dumps(values))

#接口示例
#   touser = 'LinShuKai'
#   flag = "CPU问题"
#   content = "CPU出现问题，请检修"
#   obj = Weixin(flag,content)
#   ret = obj.message(touser)
#   print ret

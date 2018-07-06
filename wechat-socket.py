#/usr/bin/python
# coding=utf-8
#-------------------------------
#	Author: LSK
#	Filename: wechat-socket.py
#	Datetime: 2018-7-5
#-------------------------------
import threading
import socket
import urllib
import re
import wechat
import logging
import ConfigParser
import json
encoding = 'utf-8'
BUFSIZE = 1024
logging.basicConfig(level=logging.DEBUG,filename='./logs/wechat.log',
                    format='%(asctime)s - %(levelname)s: %(message)s')
class Reader(threading.Thread):
    def __init__(self,client):
        threading.Thread.__init__(self)
        self.client = client
    def run(self):
        while True:
            data = self.client.recv(BUFSIZE)
            if(data):
                string = urllib.unquote(data)
                self.handle_String(string)
                #print string
            else:
                break
    def readline(self):
        rec = self.inputs.readline()
        if rec:
            string = urllib.unquote(rec)
            if len(string) >2:
                string = string[0:-2]
            else:
                string =''
        else:
            string = False
        return string
#接收4567端口的数据，截取分析字符串
    def handle_String(self,s):
        a = s.split('&')
        dict = {}
        for i in range(len(a)):
            if len(re.split('\[',a[i]))>1:
               dict['content']=re.split('content=',a[i])[1]
            elif len(re.split('tos=',a[i]))>1:
                dict['tos']=re.split('tos=',a[i])[1]
        flag = re.split('\[',dict['content'])[5].split('*')[0]
        touser = dict['tos']
        content = dict['content']
        obj = wechat.Weixin(flag, content)
        obj.message(touser)
        logging.debug('Send to %s Wechat %s %s  ' % (touser,flag,content))
        #print dict['content'],dict['tos'],flag

class Listener(threading.Thread):
    def __init__(self,port):
        threading.Thread.__init__(self)
        self.port = port
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.sock.bind(('0.0.0.0',port))
        self.sock.listen(0)
    def run(self):
        print("listener started")
        while True:
            client,cltadd = self.sock.accept()
            Reader(client).start()
            #cltadd = cltadd
            #print("accept a connect")
#定时获取access_token
def get_accesstoken():
    url = 'https://qyapi.weixin.qq.com/'
    ap = ConfigParser.SafeConfigParser()
    cp = ConfigParser.SafeConfigParser()
    ap.read('./config/wechat.conf')
    config = ap.sections()
    for i in config:
        if i != 'http' and i != 'weixin':
            agentid = ap.get(i, 'AgentId')
            corpid = ap.get(i, 'CorpID')
            corpsecret = ap.get(i, 'Secret')
            token_url = '%s/cgi-bin/gettoken?corpid=%s&corpsecret=%s' % (url, corpid, corpsecret)
            access_token = json.loads(urllib.urlopen(token_url).read().decode())['access_token']
            cp.add_section(i)
            cp.set(i,"AgentId",agentid)
            cp.set(i, "access_token", access_token)
            cp.write(open('./config/access_token.conf','w'))
    global timer
    timer = threading.Timer(3600,get_accesstoken)
    timer.start()
if __name__ == '__main__':
    lst = Listener(4567)
    timer = threading.Timer(1,get_accesstoken)
    timer.start()
    lst.start()

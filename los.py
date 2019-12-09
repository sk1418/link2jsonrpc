#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time, subprocess, re, json, requests

RPC_LINK="https://fill.aria2.service.url:6800/jsonrpc"  #aria2 jsonrpc url
RPC_TOKEN='rpcToken'                                    #the aria2 rpc token
DEBUG=False                                             #enalbe or disable debug
##-------
RE_CMD=r'^aria2c "([^"]+)".*?-out "([^"]*)".*?"(Cookie:[^"]*)".*'

class Aria2Req(object):
    def __init__(self, url, out, cookie):
        self.out = out #for output
        self.jsonrpc = '2.0'
        self.method = 'aria2.addUri'
        self.id = str(time.time_ns())
        self.params = ["token:"+RPC_TOKEN, [url], {'out':out, 'header':['user-Agent: LogStatistic', cookie]} ]

    def send(self):
        js_body = json.dumps(self, default=object2dict,indent=2) 
        debug(js_body)
        res = requests.post(RPC_LINK,data=js_body, verify=False) 
        debug(res.text)
        if res.status_code == 200:
            print("[INFO] %s ---> OK! " % self.out)
        else:
            print("[ERROR] %s ---> %s" % (self.out, res.status_code))

def paste_xclip(primary=False):
    p = subprocess.Popen(['xclip', '-selection', 'c', '-o'],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    stdout, stderr = p.communicate()
    return stdout.decode("UTF-8")

def object2dict(obj):
    return {k:v for (k,v) in obj.__dict__.items() if 'out' != k}

def send_cmd(line):
    m = re.match(RE_CMD, line)
    if m:
        Aria2Req(m.group(1), m.group(2), m.group(3)).send()
    else:
        print ("[WARNING] Unknown download cmd: %s"% line)

def debug(info):
    if DEBUG:
        print("[DEBUG] >>>>>>>>>>>>> \n" + info)

if __name__ == '__main__':
    raw = paste_xclip()
    if not raw:
        print ("Nothing to download, clipboard is empty")
        exit(1) 
    for line in raw.splitlines():
        send_cmd(line)

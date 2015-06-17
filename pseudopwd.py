#!/bin/env python

import os
from pwd import struct_passwd

location = os.path.dirname(os.path.abspath(__file__))

class _pwd(object):
    def __init__(self):
        passwd = [ i.strip().split(":") for i in open(os.path.join(location,"passwd"))]
        self.passwd = []
        for s in passwd:
            s[2] = int(s[2])
            s[3] = int(s[3])
            self.passwd.append(struct_passwd(s))
        self.byname = dict([ ( i.pw_name, i,) for i in self.passwd])
        self.byuid = dict([ ( str(i.pw_uid), i,) for i in self.passwd])

_pwdinfo = _pwd()

                          
def getpwuid(uid):
    uid  = str(uid)
    if uid in _pwdinfo.byuid:
        return _pwdinfo.byuid[uid]
    else:
        raise KeyError

def getpwnam(name):
    name  = str(name)
    if name in _pwdinfo.byname:
        return _pwdinfo.byname[name]
    else:
        raise KeyError

def getpwall():
    return _pwdinfo.passwd

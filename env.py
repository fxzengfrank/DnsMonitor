#! /usr/bin/env python
#! _*_ coding:utf-8 _*_

import sys, os

def get_sys_platform():
    ret = sys.platform.replace('\r', '').replace('\n', ' ').replace('\t', ' ')
    return ret
#
def get_sys_version():
    ret = sys.version.replace('\r', '').replace('\n', ' ').replace('\t', ' ')
    return ret
#
def get_os_uname():
    try:
        with os.popen("uname -a") as f:
            l = f.readlines()
            assert len(l) > 0
            ret = l[0].replace('\r', '').replace('\n', ' ').replace('\t', ' ') 
            return ret
    except:
        return ""
#

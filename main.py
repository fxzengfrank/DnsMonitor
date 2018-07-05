#! /usr/bin/env python
#! _*_ coding:utf-8 _*_

import os, time, random

def query(server, domain, port=53, type='A'):
    cmd = "dig +nocmd +norecurse +timeout=1 @%s -p %d %s %s +noall +answer" % (server, port, domain, type)
    with os.popen(cmd) as f:
        ls = f.readlines()
        rs = set()
        for l in ls:
            fs = filter(None, l.split())
            rs.add((fs[-1], fs[-2]))
        return rs
    return None

def main():
    a_time = time.time()
    times = 100
    ql = list()
    ql.append(('www.baidu.com.', 'A'))
    ql.append(('www.baidu.com.', 'CNAME'))
    ql.append(('baidu.com.', 'A'))
    ql.append(('baidu.com.', 'NS'))
    ql.append(('baidu.com.', 'MX'))
    for i in xrange(times):
        q = random.choice(ql)
        print("Q: %s" % repr(q))
        print("R: %s" % repr(query(server="192.168.8.1", domain=q[0], type=q[1])))
    d_time = time.time() - a_time
    print("%d times in %.3fms" % (times, d_time))
#
if __name__ == "__main__":
    main()


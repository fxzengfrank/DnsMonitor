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
            print(repr(fs))
            rs.add((fs[-1], fs[-2]))
        return rs
    return None

def main():
    a_time = time.time()
    times = 100
    ql = list()
    ql.append(('www.icbc.com.cn.', 'CNAME'))
    ql.append(('mybank.icb.com.cn.', 'CNAME'))
    ql.append(('icbc.com.cn.', 'A'))
    ql.append(('icbc.com.cn.', 'NS'))
    ql.append(('icbc.com.cn.', 'MX'))
    for i in xrange(times):
        idx = i % len(ql)
        idx = 3
        #q = random.choice(ql)
        q = ql[idx]
        print("Q: %s" % repr(q))
        print("R: %s" % repr(query(server="8.8.8.8", domain=q[0], type=q[1])))
    d_time = time.time() - a_time
    print("%d times in %.3fms" % (times, d_time))
#
if __name__ == "__main__":
    main()


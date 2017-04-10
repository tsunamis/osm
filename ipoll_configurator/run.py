from apcpe import apcpe
from threading import Thread, Event
import subprocess
from random import randrange
import sys
import time
from pynepim import Pynepim
import os
import re
from configs import *

#results_file = '/tmp/apcpe_thr.ch'

os.system("rm %s" % results_file)

'''
LPC =     {'ip':'10.0.84.101', 'lan' : '10.0.82.101', 'port':22,    'user':'wili',  'pass':'sauletekio15'}
RPC =     {'ip':'10.0.84.103', 'lan' : '10.0.82.103', 'port':22,    'user':'wili',  'pass':'sauletekio15'}
Master =  {'ip':'10.0.82.11',  'lan': '',             'port':22,    'user':'admin', 'pass':'admin01'}
Managed = {'ip':'127.0.0.1',   'lan':'',              'port':11113, 'user':'admin', 'pass':'admin01'}
'''

def Prepare_List(l):
    ll = []
    for a in l:
        if int(a) >= 5100 and int(a) <= 5730:
            ll.append(a)
    return ll

def wait_link(IP):
    status = False

    for i in range(20):
        print ">>>>>>>> Trying %s time" % i
        response = os.system("ping -c 5 -s 1400 %s" % IP)
        if response == 0:
            status = True
            return status

    return status

def run_ping():
    popen = subprocess.Popen(["ping", "-s", "1400", "%s" % RPC['lan']], stdout=subprocess.PIPE)
    lines_iterator = iter(popen.stdout.readline, b"")
    for line in lines_iterator:
        print line


def Gathering_Data():
    Thread(target=run_ping).start()

    print "Jau paleidau"
    time.sleep(10)

    master_data = master.get_wireless_stats()
    managed_data = managed.get_wireless_stats()

    print "Jau stabdau"
    os.system("pkill ping")

    return '| %s | %s |' % (master_data, managed_data)


master = apcpe(Master)
managed = apcpe(Managed)

FRQ_ALL = {}
FRQ_ALL['5']   = master.get_chan_list(bw = '5',   country='CT')
FRQ_ALL['10']  = master.get_chan_list(bw = '10',  country='CT')
FRQ_ALL['20']  = master.get_chan_list(bw = '20',  country='CT')
FRQ_ALL['40-'] = master.get_chan_list(bw = '40-', country='CT')
FRQ_ALL['40+'] = master.get_chan_list(bw = '40+', country='CT')

for i in ['5', '10', '20', '40-', '40+']:
    FRQ_ALL[i] = Prepare_List(FRQ_ALL[i])

for width in ['40+', '40-']:
    FRQ = FRQ_ALL[width]
    master.change_width(width)
    managed.change_width(width)

    for frequency in FRQ:
        STATUS = {'reason':'Not-prepared', 'status':True}
        master.change_frequency(frequency)
        master.reboot()
        managed.reboot()
        print "Laukiu kol devaisas bus pasiekiamas"
        time.sleep(5)

        cac = master.get_cac()
        print "CAC: %s" % cac
        if cac == None:
            print "Negavau CAC"
            STATUS = {'reason':'Can\'t get CAC', 'status':False}
        else:
            if cac > 0:
                print "Lauksiu CAC %s laika" % cac
                for i in progressbar(range(cac+5), "Waiting CAC: ", 100):
                    time.sleep(1)       

        if wait_link(RPC['lan']) == False:
            STATUS = {'reason':'Can\'t ping through', 'status':False}

        if master.check_channel_width(frequency, width) == False:
            STATUS = {'reason':'Channdel doesn\t match', 'status':False}


        if STATUS['status'] == True:
            print "Do test"
            if str(width) == '5':
                rate = 36.1
            elif str(width) == '10':
                rate = 72.2
            elif str(width) == '20':
                rate = 144.4
            elif str(width) == '40+':
                rate = 300
            else:
                rate = 300

            t = Pynepim(ip = LPC['lan'], client_ip=RPC['ip'], username = RPC['user'], password = RPC['pass'])
            t.set_duration(60)
            t.set_client_params('-r %sM' % rate)
            t.set_server_params([])

            try:
                IN_thr = t.start('-s')
            except:
                IN_thr = '-1'
                pass

            try:
                OUT_thr = t.start('')
            except:
                OUT_thr = '-1'
                pass

            print "%s %s" % (IN_thr, OUT_thr)

            fm = open(results_file, 'a')
            fm.writelines("%s/%s [%s | %s] %s\n" % (frequency, width, IN_thr, OUT_thr, Gathering_Data()))
            fm.close()
        else:
            fm = open(results_file, 'a')
            fm.writelines("%s/%s %s\n" % (frequency, width, STATUS['reason']))
            fm.close()


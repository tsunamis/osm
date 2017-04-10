import os
import re
import paramiko
import time
from pynepim import Pynepim
import json
from random import randrange
import sys
from threading import Thread, Event
import subprocess


LPC =     {'ip':'10.0.84.101', 'lan' : '10.0.83.101', 'port':22, 'user':'wili', 'pass':'sauletekio15'}
RPC =     {'ip':'10.0.84.103', 'lan' : '10.0.83.103', 'port':22, 'user':'wili', 'pass':'sauletekio15'}
Master =  {'ip':'10.0.83.11',  'lan': '',             'port':22, 'user':'admin', 'pass':'admin123'}
Managed = {'ip':'127.0.0.1',   'lan':'',              'port':11111, 'user':'admin', 'pass':'admin123'}

results_file = '/tmp/thr.ch'



def progressbar(it, prefix = "", size = 60):
    count = len(it)
    def _show(_i):
        x = int(size*_i/count)
        sys.stdout.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), _i, count))
        sys.stdout.flush()

    _show(0)
    for i, item in enumerate(it):
        yield item
        _show(i+1)
    sys.stdout.write("\n")
    sys.stdout.flush()




def optimize_ch(rawch):
    newch = []

    for raw in rawch:
        if not newch:
            newch.append(raw)
        else:
            FOUND = False
            for CH in newch:
                if CH['frequency'] == raw['frequency']:
                    CH['allowed_widths'] = "%s/%s" % (CH['allowed_widths'], raw['allowed_widths'])
                    FOUND = True
                    break
            if not FOUND:
                newch.append(raw)

    return newch


def capture_frequencies(RAW):
    channels = list()

    for items in RAW:
        items = items.strip()

        mark = re.compile("^([0-9]*)\ ([0-9]*)\ ([0-9]*)\ HT(20|40\-|40\+)")
        finded_elements = mark.search(items)

        match_elements = mark.match(items)
        if match_elements != None:
            chn = dict()
            chn['frequency'] = str(finded_elements.groups()[1])
            chn['channel'] = str(finded_elements.groups()[0])
            chn['max_txpower'] = str(finded_elements.groups()[2])
            chn['min_txpower'] =  None
            chn['allowed_widths'] = str(finded_elements.groups()[3])
            chn['max_eirp'] =  None

            channels.append(chn)

    channels = optimize_ch(channels)

    channels.sort(key = lambda x: x['frequency'])

    NON_STANDART_CH = ['5', '10']
    for CH in channels:
        CH['allowed_widths'] = "%s/%s" % (CH['allowed_widths'], ("/".join(NON_STANDART_CH)))

    for c in channels:
        frequency = c['frequency']
        for w in c['allowed_widths'].split('/'):
            if w == '20':
                L20.append(frequency)
            elif w == '40-':
                L40L.append(frequency)
            elif w == '40+':
                L40U.append(frequency)


def capture_frequencies2(RAW):
    channels = list()

    for items in RAW:
        items = items.strip()

        mark = re.compile("^Channel\s{1,}([0-9]*) : ([0-9]*)[\*\~\s]+Mhz 11[a-z]* ([A-Z]* [A-Z]* [A-Z]*)\s{2,}pwr:[0-9]*\-[0-9]*\(([0-9]*)\)")
        finded_elements = mark.search(items)

        match_elements = mark.match(items)

        if match_elements != None:
            chn = dict()
            chn['frequency'] = str(finded_elements.groups()[1])
            chn['channel'] = str(finded_elements.groups()[0])
            chn['max_txpower'] = str(finded_elements.groups()[3])
            chn['min_txpower'] =  None
            chn['allowed_widths'] = str(finded_elements.groups()[2]).strip().replace('CU', '40+').replace('CL', '40-').replace('C', '20').replace(' ', '/')
            chn['max_eirp'] =  None

            channels.append(chn)

    channels.sort(key = lambda x: x['frequency'])

    NON_STANDART_CH = ['5', '10']
    for CH in channels:
        CH['allowed_widths'] = "%s/%s" % (CH['allowed_widths'], ("/".join(NON_STANDART_CH)))

    for c in channels:
        frequency = c['frequency']
        for w in c['allowed_widths'].split('/'):
            if w == '20':
                L20.append(frequency)
            elif w == '40-':
                L40L.append(frequency)
            elif w == '40+':
                L40U.append(frequency)


def make_con(ip, username, password, port=22):
    i = 0
    while True:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, port = port, username = username, password = password)


            return ssh
            break
            
        except:
            i += 1
            time.sleep(2)
        if i == 30:
            print "Pasiduodu"
            sys.exit(1)




def get_chan_list(DEV, bw = 0, country='US', step = 5):
    channel = []
    bw_athtool = '0'
    bw_real = 'ht20'

    if str(bw) == str('5'):
        bw_athtool = '5'
        bw_real = 'ht5'
    elif str(bw) == str('10'):
        bw_athtool = '10'
        bw_real = 'ht10'
    elif str(bw) == str('20'):
        bw_athtool = '20'
        bw_real = 'ht20'
    elif str(bw) == str('40-'):
        bw_athtool = '20'
        bw_real = 'ht40-'
    elif str(bw) == str('40+'):
        bw_athtool = '20'
        bw_real = 'ht40+'
    elif str(bw) == str('80'):
        bw_athtool = '20'
        bw_real = 'vht80'

    print "%s - %s" % (bw, 'athtool -c %s:%s:0:%s -j' % (step, bw_athtool, country))
    try:
        ssh = make_con(DEV['ip'], username = DEV['user'], password = DEV['pass'], port = DEV['port'])
        stdin, stdout, stderr = ssh.exec_command('athtool -c %s:%s:0:%s -j' % (step, bw_athtool, country) )
        output = stdout.readlines()
        error = stderr.readlines()

        a = beautifier(output)

        ssh.close()

        CH = json.loads(a)

        for ch in CH:
            if ch['mode'] == str(bw_real):
                channel.append(ch['freq'])
    except:
        pass

    return channel

def do_system_reload(DEV={'ip':'localhost', 'port':22}):
    ssh = make_con(ip=DEV['ip'], username = 'admin', password = 'admin01', port = DEV['port']) 
    stdin, stdout, stderr = ssh.exec_command('system_reload')
    print "%s %s" % (stdout.readlines(), stderr.readlines())
    ssh.close()


def set_vhtmcs(DEV={'ip':'localhost', 'port':22, 'user':'admin', 'pass':'admin123'}, mcs = 9):
    ip = DEV['ip'] 
    port = DEV['port']
    username = DEV['user']
    password = DEV['pass']

    ssh = make_con(ip, username = username, password = password, port = port)

    stdin, stdout, stderr = ssh.exec_command('iwpriv ath0 vhtmcs %s' % mcs)
    print "%s %s" % (stdout.readlines(),  stderr.readlines())

    ssh.close()



def get_cac(DEV):
    content = None

    try:
        ssh = make_con(DEV['ip'], username = DEV['user'], password = DEV['pass'], port = DEV['port'])

        stdin, stdout, stderr = ssh.exec_command('stats -p')
        print "%s %s" % (stdout.readlines(), stderr.readlines())
        time.sleep(1)
        stdin, stdout, stderr = ssh.exec_command('cat /var/run/stats/periodic.json') 
        output = stdout.readlines()
        error = stderr.readlines()
        print  ">>>> get_cac >>>> %s %s" % (output, error)

        cac = json.loads(beautifier(output))
        
        content = int(cac['wireless'][0]['cacPeriod'])
        ssh.close()

    except:
        pass

    return content


def beautifier(text):
    a = ''
    for iii in text:
        a = a + iii
    return a


def get_DatRate(DEV):
    content = []

    for i in range(2):
        try:
            ssh = make_con(DEV['ip'], username = DEV['user'], password = DEV['pass'], port = DEV['port'])

            stdin, stdout, stderr = ssh.exec_command('stats -w')
            print "%s %s" % (stdout.readlines(), stderr.readlines())
            time.sleep(1)
            stdin, stdout, stderr = ssh.exec_command('cat /var/run/stats/wireless.json') 
            output = stdout.readlines()
            error = stderr.readlines()
            print  ">>>> get_cac >>>> %s %s" % (output, error)
            RAW = json.loads(beautifier(output))
            tmp_l = {}
            tmp_l['bitrate'] = str(RAW['radios']["dev"]["wifi0"]["bitrate"])
            tmp_l['txRate'] = str(RAW["peers"][0]["txRate"])  
            tmp_l['rxRate'] = str(RAW["peers"][0]["rxRate"])
            tmp_l['signal'] = RAW["peers"][0]["signal"]
            content.append(tmp_l)
            
            ssh.close()

        except:
            pass
        time.sleep(2)

    return content


def get_real_width(DEV):
    content = None

    try:
        ssh = make_con(DEV['ip'], username = DEV['user'], password = DEV['pass'], port = DEV['port'])
        stdin, stdout, stderr = ssh.exec_command('cat /var/run/stats/wireless.json')
        output = stdout.readlines()
        error = stderr.readlines()

        text = json.loads(beautifier(output))
        content = str(text['radios']['dev']['wifi0']['channelWidth'])

    except:
        print "        >>> Can't parse channel"
        pass

    return content



def get_real_channel(DEV):
    content = None

    try:
        ssh = make_con(DEV['ip'], username = DEV['user'], password = DEV['pass'], port = DEV['port'])
        stdin, stdout, stderr = ssh.exec_command('cat /var/run/stats/wireless.json')
        output = stdout.readlines()
        error = stderr.readlines()

        text = json.loads(beautifier(output))
        content = int(text['radios']['dev']['wifi0']['frequency'])

    except:
        print "        >>> Can't parse channel"
        pass

    return content


def check_channel_width(DEV, CH, BW):
    status = False
    CH1 = get_real_channel(DEV)
    BW1 = get_real_width(DEV)

    if CH1 and BW1:
        print "%s %s %s %s" % (CH, BW, CH1, BW1)
        if (int(CH) == int(CH1)) and (str(BW) == str(BW1)):
            status = True

    return status




##### Execute commands ####
def run_ping():
    cmd = 'ping -s 1400 10.0.83.103'
    popen = subprocess.Popen(["ping", "-s", "1400", "10.0.83.103"], stdout=subprocess.PIPE)
    lines_iterator = iter(popen.stdout.readline, b"")
    for line in lines_iterator:
        print line


def execute(DEV, command):
    ssh = make_con(DEV['ip'], username = DEV['user'], password = DEV['pass'], port = DEV['port'])
    stdin, stdout, stderr = ssh.exec_command(str(command))
    output = stdout.readlines()
    error = stderr.readlines()
    print ">>>> execute >>>> %s %s" % (output, error)
    ssh.close()


def wait_link(IP):
    status = False

    for i in range(20):
        print ">>>>>>>> Trying %s time" % i
        response = os.system("ping -c 5 -s 1400 %s" % IP)
        if response == 0:
            status = True
            return status

    return status

##### Parameters ####

def change_frequency(DEV, frequency = '5180'):
    ssh = make_con(DEV['ip'], username = DEV['user'], password = DEV['pass'], port = DEV['port'])

    sftp = ssh.open_sftp()
    f = sftp.file('/tmp/config.json', 'r')
    cfg = json.load(f)
    f.close()

    cfg['channel']['list'] = [int(frequency)]                           # Only for PTP
    #cfg['wireless']['radio'][0]['channel']['list'] = [int(frequency)]       # only for APCPE
    #cfg['wireless']['radio'][0]['channel']['select'] = str('list')          # only for APCPE

    sftp = ssh.open_sftp()
    f = sftp.file('/tmp/config.json', 'w')
    json.dump(cfg, f, indent=4)
    f.close()

    stdin, stdout, stderr = ssh.exec_command('sysconf -w')
    print ">>>> change_frequency >>>> %s %s" % (stdout.readlines(), stderr.readlines())

    ssh.close()


def change_width(DEV, width = '20'):
    extension = 'upper'
    if str(width) == '40-':
       width = '40'
       extension = 'lower'

    if str(width) == '40+':
        width = '40'
        extension = 'upper'

    ssh = make_con(DEV['ip'], username = DEV['user'], password = DEV['pass'], port = DEV['port'])

    sftp = ssh.open_sftp()
    f = sftp.file('/tmp/config.json', 'r')
    cfg = json.load(f)
    f.close()

    cfg['channel']['width'] = int(width)                                    # Only for PTP
    #cfg['wireless']['radio'][0]['channel']['width'] = int(width)           # only for APCPE
    #cfg['wireless']['radio'][0]['channel']['extension'] = str(extension)   # only for APCPE

    sftp = ssh.open_sftp()
    f = sftp.file('/tmp/config.json', 'w')
    json.dump(cfg, f, indent=4)
    f.close()

    stdin, stdout, stderr = ssh.exec_command('sysconf -w')
    print ">>>> change_width >>>> %s %s" % (stdout.readlines(), stderr.readlines())

    ssh.close()

os.system("rm %s" % results_file)

#print check_channel_width(Master, int(5000), str("40+"))

FRQ_ALL = {}

def Prepare_List(l):
    ll = []
    for a in l:
        if int(a) >= 5100 and int(a) <= 5730:
            ll.append(a)       
    return ll

def Gathering_Data():
    Thread(target=run_ping).start()

    print "Jau paleidau"
    time.sleep(10)

    master_data = ''
    for i in get_DatRate(Master):
        master_data += " TX:%s RX:%s {%s/%s}" % (i['txRate'], i['rxRate'], i['signal'][0], i['signal'][1])

    managed_data = ''
    for i in get_DatRate(Managed):
        managed_data += " TX:%s RX:%s {%s/%s}" % (i['txRate'], i['rxRate'], i['signal'][0], i['signal'][1])

    print "Jau stabdau"
    os.system("pkill ping")

    return '| %s | %s |' % (master_data, managed_data)

#print Gathering_Data()
#sys.exit(1)

FRQ_ALL['5']   = get_chan_list(Master, bw = '5',   country='CT')
FRQ_ALL['10']  = get_chan_list(Master, bw = '10',  country='CT')
FRQ_ALL['20']  = get_chan_list(Master, bw = '20',  country='CT')
FRQ_ALL['40-'] = get_chan_list(Master, bw = '40-', country='CT')
FRQ_ALL['40+'] = get_chan_list(Master, bw = '40+', country='CT')
FRQ_ALL['80']  = get_chan_list(Master, bw = '80',  country='CT')

for i in ['5', '10', '20', '40-', '40+', '80']:
    FRQ_ALL[i] = Prepare_List(FRQ_ALL[i])

#print json.dumps(FRQ_ALL, indent = 4)

#for width in ['5', '10', '20', '40+', '80']:
#for width in ['20', '40+', '80']:
for width in ['80']:

    FRQ = FRQ_ALL[width]
    change_width(Managed, width)
    change_width(Master, width)


    for frequency in FRQ:
        STATUS = {'reason':'Not-prepared', 'status':True}

        change_frequency(Master, frequency)
        execute(Managed, 'reboot')
        execute(Master, 'reboot')
        print "Laukiu kol devaisas bus pasiekiamas"
        time.sleep(5)

        cac = get_cac(Master)
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

        if check_channel_width(Master, frequency, width) == False:
            STATUS = {'reason':'Channdel doesn\t match', 'status':False}
  
        if STATUS['status'] == True:
            print "Do test"
            if str(width) == '5':
                rate = 173.3
            elif str(width) == '10':
                rate = 173.3
            elif str(width) == '20':
                rate = 173.3
            elif str(width) == '40+':
                rate = 400
            elif str(width) == '80':
                rate = 866.7
            else:
                rate = 866.7

            t = Pynepim(ip = LPC['lan'], client_ip=RPC['ip'], username = RPC['user'], password = RPC['pass'])
            t.set_duration(60)
            t.set_client_params('-u -r %sM' % rate)
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

            fm = open(results_file, 'a')
            fm.writelines("%s/%s [%s | %s] %s\n" % (frequency, width, IN_thr, OUT_thr, Gathering_Data()))
            fm.close()
        else:
            fm = open(results_file, 'a')
            fm.writelines("%s/%s %s\n" % (frequency, width, STATUS['reason']))
            fm.close()

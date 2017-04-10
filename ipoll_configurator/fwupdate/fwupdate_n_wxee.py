from connection import connection
import time
import threading
from athconfiger_wxee import Configer_wxee
import scp
from config import *
import json
import time
import pdb
from wxee2 import wxee

threads = {}

username = 'admin'
password = 'admin01'
pc = '10.0.10.26'

IP = [
{'ip' : '172.17.0.3', 'port' : 7701, 'user' : username, 'pass' : password, 'real_port' : '101', 'real_ip': '10.1.1.101', 'alias': '192.168.0.1'},
{'ip' : '172.17.0.5', 'port' : 7702, 'user' : username, 'pass' : password, 'real_port' : '102', 'real_ip': '10.1.2.101', 'alias': '192.168.0.2'},
{'ip' : '172.17.0.7', 'port' : 7703, 'user' : username, 'pass' : password, 'real_port' : '103', 'real_ip': '10.1.3.101', 'alias': '192.168.0.3'},
{'ip' : '172.17.0.9', 'port' : 7704, 'user' : username, 'pass' : password, 'real_port' : '104', 'real_ip': '10.1.4.101', 'alias': '192.168.0.4'},
{'ip' : '172.17.0.11', 'port' : 7705, 'user' : username, 'pass' : password, 'real_port' : '105', 'real_ip': '10.1.5.101', 'alias': '192.168.0.5'},
{'ip' : '172.17.0.13', 'port' : 7706, 'user' : username, 'pass' : password, 'real_port' : '106', 'real_ip': '10.1.6.101', 'alias': '192.168.0.6'},
{'ip' : '172.17.0.15', 'port' : 7707, 'user' : username, 'pass' : password, 'real_port' : '107', 'real_ip': '10.1.7.101', 'alias': '192.168.0.7'},
{'ip' : '172.17.0.17', 'port' : 7708, 'user' : username, 'pass' : password, 'real_port' : '108', 'real_ip': '10.1.8.101', 'alias': '192.168.0.8'},

{'ip' : '172.17.0.19', 'port' : 7709, 'user' : username, 'pass' : password, 'real_port' : '201', 'real_ip': '10.2.1.101', 'alias': '192.168.0.9'},
{'ip' : '172.17.0.21', 'port' : 7710, 'user' : username, 'pass' : password, 'real_port' : '202', 'real_ip': '10.2.2.101', 'alias': '192.168.0.10'},
{'ip' : '172.17.0.23', 'port' : 7711, 'user' : username, 'pass' : password, 'real_port' : '203', 'real_ip': '10.2.3.101', 'alias': '192.168.0.11'},
{'ip' : '172.17.0.25', 'port' : 7712, 'user' : username, 'pass' : password, 'real_port' : '204', 'real_ip': '10.2.4.101', 'alias': '192.168.0.12'},
{'ip' : '172.17.0.27', 'port' : 7713, 'user' : username, 'pass' : password, 'real_port' : '205', 'real_ip': '10.2.5.101', 'alias': '192.168.0.13'},
{'ip' : '172.17.0.29', 'port' : 7714, 'user' : username, 'pass' : password, 'real_port' : '206', 'real_ip': '10.2.6.101', 'alias': '192.168.0.14'},
{'ip' : '172.17.0.31', 'port' : 7715, 'user' : username, 'pass' : password, 'real_port' : '207', 'real_ip': '10.2.7.101', 'alias': '192.168.0.15'},
{'ip' : '172.17.0.33', 'port' : 7716, 'user' : username, 'pass' : password, 'real_port' : '208', 'real_ip': '10.2.8.101', 'alias': '192.168.0.16'},

{'ip' : '172.17.0.35', 'port' : 7717, 'user' : username, 'pass' : password, 'real_port' : '301', 'real_ip': '10.3.1.101', 'alias': '192.168.0.17'},
{'ip' : '172.17.0.37', 'port' : 7718, 'user' : username, 'pass' : password, 'real_port' : '302', 'real_ip': '10.3.2.101', 'alias': '192.168.0.18'},
{'ip' : '172.17.0.39', 'port' : 7719, 'user' : username, 'pass' : password, 'real_port' : '303', 'real_ip': '10.3.3.101', 'alias': '192.168.0.19'},
{'ip' : '172.17.0.41', 'port' : 7720, 'user' : username, 'pass' : password, 'real_port' : '304', 'real_ip': '10.3.4.101', 'alias': '192.168.0.20'},
{'ip' : '172.17.0.43', 'port' : 7721, 'user' : username, 'pass' : password, 'real_port' : '305', 'real_ip': '10.3.5.101', 'alias': '192.168.0.21'},
{'ip' : '172.17.0.45', 'port' : 7722, 'user' : username, 'pass' : password, 'real_port' : '306', 'real_ip': '10.3.6.101', 'alias': '192.168.0.22'},
{'ip' : '172.17.0.47', 'port' : 7723, 'user' : username, 'pass' : password, 'real_port' : '307', 'real_ip': '10.3.7.101', 'alias': '192.168.0.23'},
#{'ip' : '172.17.0.49', 'port' : 7724, 'user' : username, 'pass' : password, 'real_port' : '308', 'real_ip': '10.3.8.101', 'alias': '192.168.0.24'},

{'ip' : '172.17.0.51', 'port' : 7725, 'user' : username, 'pass' : password, 'real_port' : '401', 'real_ip': '10.4.1.101', 'alias': '192.168.0.25'},
{'ip' : '172.17.0.53', 'port' : 7726, 'user' : username, 'pass' : password, 'real_port' : '402', 'real_ip': '10.4.2.101', 'alias': '192.168.0.26'},
{'ip' : '172.17.0.55', 'port' : 7727, 'user' : username, 'pass' : password, 'real_port' : '403', 'real_ip': '10.4.3.101', 'alias': '192.168.0.27'},
{'ip' : '172.17.0.57', 'port' : 7728, 'user' : username, 'pass' : password, 'real_port' : '404', 'real_ip': '10.4.4.101', 'alias': '192.168.0.28'},
#{'ip' : '172.17.0.59', 'port' : 7729, 'user' : username, 'pass' : password, 'real_port' : '405', 'real_ip': '10.4.5.101', 'alias': '192.168.0.29'},
#{'ip' : '172.17.0.61', 'port' : 7730, 'user' : username, 'pass' : password, 'real_port' : '406', 'real_ip': '10.4.6.101', 'alias': '192.168.0.30'},
#{'ip' : '172.17.0.63', 'port' : 7731, 'user' : username, 'pass' : password, 'real_port' : '407', 'real_ip': '10.4.7.101', 'alias': '192.168.0.31'},
#{'ip' : '172.17.0.65', 'port' : 7732, 'user' : username, 'pass' : password, 'real_port' : '408', 'real_ip': '10.4.8.101', 'alias': '192.168.0.32'},

{'ip' : '172.17.0.67', 'port' : 7733, 'user' : username, 'pass' : password, 'real_port' : '501', 'real_ip': '10.5.1.101', 'alias': '192.168.0.33'},
{'ip' : '172.17.0.69', 'port' : 7734, 'user' : username, 'pass' : password, 'real_port' : '502', 'real_ip': '10.5.2.101', 'alias': '192.168.0.34'},
{'ip' : '172.17.0.71', 'port' : 7735, 'user' : username, 'pass' : password, 'real_port' : '503', 'real_ip': '10.5.3.101', 'alias': '192.168.0.35'},
{'ip' : '172.17.0.73', 'port' : 7736, 'user' : username, 'pass' : password, 'real_port' : '504', 'real_ip': '10.5.4.101', 'alias': '192.168.0.36'},
{'ip' : '172.17.0.75', 'port' : 7737, 'user' : username, 'pass' : password, 'real_port' : '505', 'real_ip': '10.5.5.101', 'alias': '192.168.0.37'},
{'ip' : '172.17.0.77', 'port' : 7738, 'user' : username, 'pass' : password, 'real_port' : '506', 'real_ip': '10.5.6.101', 'alias': '192.168.0.38'},
{'ip' : '172.17.0.79', 'port' : 7739, 'user' : username, 'pass' : password, 'real_port' : '507', 'real_ip': '10.5.7.101', 'alias': '192.168.0.39'},
{'ip' : '172.17.0.81', 'port' : 7740, 'user' : username, 'pass' : password, 'real_port' : '508', 'real_ip': '10.5.8.101', 'alias': '192.168.0.40'},

#{'ip' : '10.0.10.26', 'port' : 22611, 'user' : username, 'pass' : password, 'real_port' : '601', 'real_ip': '10.6.1.101', 'alias': '192.168.0.41'},
#{'ip' : '10.0.10.26', 'port' : 22621, 'user' : username, 'pass' : password, 'real_port' : '602', 'real_ip': '10.6.2.101', 'alias': '192.168.0.42'},
#{'ip' : '10.0.10.26', 'port' : 22631, 'user' : username, 'pass' : password, 'real_port' : '603', 'real_ip': '10.6.3.101', 'alias': '192.168.0.43'},
#{'ip' : '10.0.10.26', 'port' : 22641, 'user' : username, 'pass' : password, 'real_port' : '604', 'real_ip': '10.6.4.101', 'alias': '192.168.0.44'},
#{'ip' : '10.0.10.26', 'port' : 22651, 'user' : username, 'pass' : password, 'real_port' : '605', 'real_ip': '10.6.5.101', 'alias': '192.168.0.45'},
#{'ip' : '10.0.10.26', 'port' : 22661, 'user' : username, 'pass' : password, 'real_port' : '606', 'real_ip': '10.6.6.101', 'alias': '192.168.0.46'},
#{'ip' : '10.0.10.26', 'port' : 22671, 'user' : username, 'pass' : password, 'real_port' : '607', 'real_ip': '10.6.7.101', 'alias': '192.168.0.47'},
#{'ip' : '10.0.10.26', 'port' : 22681, 'user' : username, 'pass' : password, 'real_port' : '608', 'real_ip': '10.6.8.101', 'alias': '192.168.0.48'},
#
#{'ip' : '10.0.10.26', 'port' : 22711, 'user' : username, 'pass' : password, 'real_port' : '701', 'real_ip': '10.7.1.101', 'alias': '192.168.0.49'},
#{'ip' : '10.0.10.26', 'port' : 22721, 'user' : username, 'pass' : password, 'real_port' : '702', 'real_ip': '10.7.2.101', 'alias': '192.168.0.50'},
#{'ip' : '10.0.10.26', 'port' : 22731, 'user' : username, 'pass' : password, 'real_port' : '703', 'real_ip': '10.7.3.101', 'alias': '192.168.0.51'},
#{'ip' : '10.0.10.26', 'port' : 22741, 'user' : username, 'pass' : password, 'real_port' : '704', 'real_ip': '10.7.4.101', 'alias': '192.168.0.52'},
#{'ip' : '10.0.10.26', 'port' : 22751, 'user' : username, 'pass' : password, 'real_port' : '705', 'real_ip': '10.7.5.101', 'alias': '192.168.0.53'},
#{'ip' : '10.0.10.26', 'port' : 22761, 'user' : username, 'pass' : password, 'real_port' : '706', 'real_ip': '10.7.6.101', 'alias': '192.168.0.54'},
#{'ip' : '10.0.10.26', 'port' : 22771, 'user' : username, 'pass' : password, 'real_port' : '707', 'real_ip': '10.7.7.101', 'alias': '192.168.0.55'},
#{'ip' : '10.0.10.26', 'port' : 22781, 'user' : username, 'pass' : password, 'real_port' : '708', 'real_ip': '10.7.8.101', 'alias': '192.168.0.56'},
#
#{'ip' : '10.0.10.26', 'port' : 22811, 'user' : username, 'pass' : password, 'real_port' : '801', 'real_ip': '10.8.1.101', 'alias': '192.168.0.57'},
#{'ip' : '10.0.10.26', 'port' : 22821, 'user' : username, 'pass' : password, 'real_port' : '802', 'real_ip': '10.8.2.101', 'alias': '192.168.0.58'},
#{'ip' : '10.0.10.26', 'port' : 22831, 'user' : username, 'pass' : password, 'real_port' : '803', 'real_ip': '10.8.3.101', 'alias': '192.168.0.59'},
#{'ip' : '10.0.10.26', 'port' : 22841, 'user' : username, 'pass' : password, 'real_port' : '804', 'real_ip': '10.8.4.101', 'alias': '192.168.0.60'},
#{'ip' : '10.0.10.26', 'port' : 22851, 'user' : username, 'pass' : password, 'real_port' : '805', 'real_ip': '10.8.5.101', 'alias': '192.168.0.61'},
#{'ip' : '10.0.10.26', 'port' : 22861, 'user' : username, 'pass' : password, 'real_port' : '806', 'real_ip': '10.8.6.101', 'alias': '192.168.0.62'},
#{'ip' : '10.0.10.26', 'port' : 22871, 'user' : username, 'pass' : password, 'real_port' : '807', 'real_ip': '10.8.7.101', 'alias': '192.168.0.63'},
#{'ip' : '10.0.10.26', 'port' : 22881, 'user' : username, 'pass' : password, 'real_port' : '808', 'real_ip': '10.8.8.101', 'alias': '192.168.0.64'}
]



IP_AC = [
{'ip' : '10.0.10.26', 'port' : 22381, 'user' : username, 'pass' : password, 'real_port' : '308'},
{'ip' : '10.0.10.26', 'port' : 22481, 'user' : username, 'pass' : password, 'real_port' : '408'}
]

#IP = IP_AC

class wxee_ipoll64(wxee):

    def __init__(self, Device):
        self.ip = Device['ip']
        self.port = Device['port']
        self.username = Device['user']
        self.password = Device['pass']
        self.lan = None
        self.real_port = Device['real_port']
        wxee.__init__(self, devtype="qualcomm")


    def changed_parameters(self, l):
        l['wireless']['radio'][0]['txpower'] = int(5) 
        #l['wireless']['radio'][0]['channel']['list'] = [5180]
       # l['wireless']['radio'][0]['channel']['select'] = str("all")
      
        l['wireless']['radio'][0]['vap'][0]['ssid2vlan']['enabled'] = bool(False)
        l['wireless']['radio'][0]['vap'][0]['ssid2vlan']['id'] = int(self.real_port)
      #  l['wireless']['radio'][0]['channel']['width'] = int(40)
        #l['wireless']['radio'][0]['channel']['nonstandard'] = bool(True)
      #  l['wireless']['radio'][0]['channel']['autowidth'] = bool(True)
      #  l['wireless']['radio'][0]['vap'][0]['shortgi'] = bool(True)
      #  l['wireless']['radio'][0]['txpower'] = int(10)
      #  l['wireless']['radio'][0]['vap'][0]['wds'] = bool(True)
       # l['wireless']['radio'][0]['vap'][0]['ssid'] = str('ipoll64_ac')
      #  l['wireless']['radio'][0]['vap'][0]['rate']['mcs'] = str('auto')
#        l['wireless']['countrycode'] = str('US')
        l['wireless']['radio'][0]['enabled'] = bool(True)



#        l['wireless']['radio'][0]['vap'][0]['security']['mode'] = str('wpapsk') # open|wpapsk
       
        #### WPA/ENTERPRISE
        #l['wireless']['radio'][0]['vap'][0]['security']['wpaenterprise']['authentication']['eap'] = 'peap'
        #l['wireless']['radio'][0]['vap'][0]['security']['wpaenterprise']['authentication']['password'] = 'tester'
        #l['wireless']['radio'][0]['vap'][0]['security']['wpaenterprise']['authentication']['identity'] = 'tester'
    
        #### WPA/PSK2
#        l['wireless']['radio'][0]['vap'][0]['security']['wpapsk'] = {}
#        l['wireless']['radio'][0]['vap'][0]['security']['wpapsk']['passphrase'] = 'tester123'

        #print l['wireless']['radio'][0]['vap'][0]['security']['wpaenterprise']['authentication']
        #l['network']['topology'] = 'router'

        # AP STA
        #l['wireless']['radio'][0]['vap'][0]['mode'] = "sta" # ap|sta
        
        # wds on/off
        #l['wireless']['radio'][0]['repeater']['wds'] = bool(False)
        #l['wireless']['radio'][0]['wjet']['enabled'] = bool(True)
        return l


    def do(self):
        R = Configer_wxee(self.changed_parameters)

        con = R.connect(ip = self.ip, port = self.port)
        if R.configure(ip = self.ip, port = self.port, con = con): 
            print "     Succesfull %s" % self.port
        else:
            print "     Failed %s" % self.port


    def upgrade(self, args):
        n = self.wx_socket(self.ip, self.port)
        self.wcmd_put(n, '/tmp/fwupdate.bin', args)
        self.wcmd_legacy(n, 'fwupdate 2>&1')

    def upload(self, remote, local):
        n = self.wx_socket(self.ip, self.port)
        self.wcmd_put(n, remote, local)

    def executing(self, cmd):
        n = self.wx_socket(self.ip, self.port)
        cmd += ' 2>&1'
        out = self.wcmd_legacy(n, cmd)
        return out


for i in IP:
#
#    ''' 
#    IP = "10.%s.%s.101" % (str(i['real_port'])[0], str(i['real_port'])[2])
#    GATEWAY = "10.%s.%s.26" % (str(i['real_port'])[0], str(i['real_port'])[2])
#    get_confige(NAME  =  "CPE_%s" % i['real_port'], IP = IP, GATEWAY = GATEWAY, FILE = 'config_11n.json')
#
#    l.upload('/tmp/oem.json', '/data/config.json')
#    l.executing('cp /data/config.json /tmp/config.json; sysconf -w; reboot')
#    '''
#
#    l.executing("ifconfig ath0 down")
#    data = l.executing("cat /var/run/ath0_scan_results.json")
#
#    # Vykdo komanda
#    threading.Thread(target = l.executing, args=["sed -i 's/ipoll64_ac/" + str(i['real_ip']) + "/g' /tmp/config.json; sysconf -w; system_reload"]).start()
#    #threading.Thread(target = l.executing, args=['cp /tmp/config.json /data/bridge.json']).start()
#
    #threading.Thread(target = l.executing, args=['cp /data/config.json /tmp/config.json; sysconf -w; reboot']).start()
    #threading.Thread(target = l.executing, args=['reboot']).start()
#    #time.sleep(2)
    #l.executing('cat /usr/lib/version')
#
  #  threading.Thread(target = l.executing, args=['for i in $(seq 1 1 10); do stats -w; sleep 1; grep -i -A 2 signal /var/run/stats/wireless.json; done']).start()
#    threading.Thread(target = l.executing, args=['iwconfig ath0| grep -i ssid']).start()
#    threading.Thread(target = l.executing, args=['echo "--------------------";ifconfig ath0 | grep -i "HWaddr"| cut -c 39-; ip r | grep proto | cut -c 52-;']).start()
#    #threading.Thread(target = l.executing, args=['ifconfig br0 | grep -i "HWaddr"; ifconfig ath0 | grep -i "HWaddr"; ifconfig eth0 | grep -i "HWaddr"; ifconfig br0 | grep -i \"inet addr\"']).start()
#    # Upgradina
#    threading.Thread(target = l.upgrade ,args=['/tmp/APCPE.QM-1.v7.54-DEVEL.19940.img']).start()
#    threading.Thread(target = l.do).start()
#


#    threading.Thread(target = l.executing, args=['uptime']).start()
    #threading.Thread(target = l.executing, args=['ip a a ' + i['alias'] + '/24 dev br0']).start()
    #threading.Thread(target = l.executing, args=['ip r']).start()
#    threading.Thread(target = l.executing, args=['for j in $(seq 1 1 64); do ping -c 1 -W 1 192.168.0.$j; done']).start()
#    with open('/home/tester/arvydas-AC-testai/scan_rezultatai/' + i['real_ip'] + '.json', 'w') as outfile:
#        json.dump(data, outfile, indent=3)

#for j in ['3']:#, '10', '20']:
#for i in IP:
#    l = ipoll64(i)
#    threading.Thread(target = l.do).start()
   #for i in IP:
   #    threads[i['real_ip']].join()
#tx_power = 30
#for i in IP:
#    l = ipoll64(i)
#    l.executing("iwscan2json ath0")
#    data = l.executing("cat /var/run/ath0_scan_results.json")
#    while data == ([], [u"cat: can't open '/var/run/ath0_scan_results.json': No such file or directory\n"]):
#        data = l.executing("iwscan2json ath0")
#    with open('/home/tester/arvydas-AC-testai/antras_kartas_scan_rezultatai/' + i['real_ip'] + 'tx' + str(tx_power) + '.json', 'w') as outfile:
#        json.dump(data, outfile, indent=3)
#
    l = wxee_ipoll64(i)
    #l.upgrade('/tmp/latest.img')
    threading.Thread(target = l.upgrade ,args=['/tmp/latest.img']).start()


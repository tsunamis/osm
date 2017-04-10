from connection import connection
import paramiko
import time
import threading
from athconfiger import Configer
import scp
from config import *


username = 'admin'
password = 'admin01'
pc = '10.0.10.26'

IP = [
{'ip' : '172.17.0.3 ', 'port' : 22111, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.5 ', 'port' : 22121, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.7 ', 'port' : 22131, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.9 ', 'port' : 22141, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.11', 'port' : 22151, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.13', 'port' : 22161, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.15', 'port' : 22171, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.17', 'port' : 22181, 'user' : username, 'pass' : password, 'real_port' : ''},

{'ip' : '172.17.0.19', 'port' : 22211, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.21', 'port' : 22221, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.23', 'port' : 22231, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.25', 'port' : 22241, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.27', 'port' : 22251, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.29', 'port' : 22261, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.31', 'port' : 22271, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.33', 'port' : 22281, 'user' : username, 'pass' : password, 'real_port' : ''},

{'ip' : '172.17.0.35', 'port' : 22311, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.37', 'port' : 22321, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.39', 'port' : 22331, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.41', 'port' : 22341, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.43', 'port' : 22351, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.45', 'port' : 22361, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.47', 'port' : 22371, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.49', 'port' : 22381, 'user' : username, 'pass' : password, 'real_port' : ''},

{'ip' : '172.17.0.51', 'port' : 22411, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.53', 'port' : 22421, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.55', 'port' : 22431, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.57', 'port' : 22441, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.59', 'port' : 22451, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.61', 'port' : 22461, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.63', 'port' : 22471, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.65', 'port' : 22481, 'user' : username, 'pass' : password, 'real_port' : ''},

{'ip' : '172.17.0.67', 'port' : 22511, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.69', 'port' : 22521, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.71', 'port' : 22531, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.73', 'port' : 22541, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.75', 'port' : 22551, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.77', 'port' : 22561, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.79', 'port' : 22571, 'user' : username, 'pass' : password, 'real_port' : ''},
{'ip' : '172.17.0.81', 'port' : 22581, 'user' : username, 'pass' : password, 'real_port' : ''}
]


class ipoll64(connection):

    def __init__(self, Device):
        connection.__init__(self, Device['ip'], Device['user'], Device['pass'], Device['port'], None)
        self.ip = Device['ip']
        self.port = Device['port']
        self.username = Device['user']
        self.password = Device['pass']
        self.lan = None
        #self.real_port = Device['real_port']
        self.parameters1 = Device['p1']
        self.parameters2 = Device['p2']
        self.parameters3 = Device['p3']


    def changed_parameters(self, l):
        print "%s %s %s" % (self.parameters1, self.parameters2, self.parameters3)
        #l['network']['topology'] = str('bridge')
        #l['network']['topology'] = str('router')
        #l['network']['nat'] = bool(True)

        #l['network']['router']['wan']['mode'] = str('static')
        #l['network']['router']['wan']['static']['ip'][0]['ip'] = str(self.parameters2)
        #l['network']['router']['wan']['static']['gateway'] = str(self.parameters3)
        #l['network']['router']['lan']['ip']['ip'] = str(self.parameters1)

        #l['wireless']['radio'][0]['vap'][0]['ssid2vlan']['enabled'] = bool(False)
        #l['wireless']['radio'][0]['vap'][0]['ssid2vlan']['id'] = int(self.real_port)
        #l['wireless']['radio'][0]['channel']['width'] = int(80)
        l['wireless']['radio'][0]['channel']['nonstandard'] = bool(True)
        #l['wireless']['radio'][0]['channel']['autowidth'] = bool(True)
        #l['wireless']['radio'][0]['vap'][0]['shortgi'] = bool(True)
        l['wireless']['radio'][0]['txpower'] = int(10)
        l['wireless']['radio'][0]['vap'][0]['wds'] = bool(True)
        l['wireless']['radio'][0]['vap'][0]['ssid'] = str('ptmp-ipoll64')
        #l['wireless']['radio'][0]['vap'][0]['rate']['mcs'] = str('auto')
        l['wireless']['countrycode'] = str('US')
        l['wireless']['radio'][0]['wjet']['enabled'] = bool(True)
        l['wireless']['radio'][0]['autorate'] = str("rssi")
        #l['wireless']['radio'][0]['autorate'] = str("per")



        #l['wireless']['radio'][0]['vap'][0]['security']['mode'] = str('wpapsk')
        l['wireless']['radio'][0]['vap'][0]['security']['mode'] = str('open')
       
        #### WPA/ENTERPRISE
        #l['wireless']['radio'][0]['vap'][0]['security']['wpaenterprise']['authentication']['eap'] = 'peap'
        #l['wireless']['radio'][0]['vap'][0]['security']['wpaenterprise']['authentication']['password'] = 'tester'
        #l['wireless']['radio'][0]['vap'][0]['security']['wpaenterprise']['authentication']['identity'] = 'tester'
    
        #### WPA/PSK2
        #l['wireless']['radio'][0]['vap'][0]['security']['wpapsk'] = {}
        #l['wireless']['radio'][0]['vap'][0]['security']['wpapsk']['passphrase'] = 'C1ient2c0r3@DLCO'

        #print l['wireless']['radio'][0]['vap'][0]['security']['wpaenterprise']['authentication']
        #l['network']['topology'] = 'router'








        #PTMP
        #l['log']['forward'] = {}
        #l['log']['forward']['enabled'] = True
        #l['log']['forward']['server1'] = { "address": "172.17.0.18", "port": 514 }
        #l['log']['forward']['server2'] = str('0.0.0.0')

        return l


    def do(self):
        R = Configer(self.changed_parameters)

        if R.configure(ip = self.ip, port = self.port, usr = self.username, psw = self.password, save=True): 
        #if R.configure(ip = self.ip, port = self.port, usr = self.username, psw = self.password, save=False): 
            print "     Succesfull %s" % self.port
        else:
            print "     Failed %s" % self.port


    def upgrade(self, args):
        self.open_con()
        self.open_sftp(args, '/tmp/fwupdate.bin')
        self.execute('fwupdate')

    def upload(self, arg1, arg2):
        self.open_con()
        self.open_sftp(arg1, arg2)

    def executing(self, cmd):
        self.open_con()
        self.execute(cmd)


c = 80
#for i in IP:
for i in range(3, 114, 2):
#for i in range(3, 7, 2):
    c += 1
    CON = {'ip' : '172.17.0.%s' % i, 'port' : 2222, 'user' : 'admin', 'pass' : 'admin01', 'p1' : '192.168.199.%s' % c, 'p2': '192.168.3.%s' % c, 'p3' : '192.168.3.%s' % (c+80)}
    print CON
    l = ipoll64(CON)
    #l.do()

    #IP = "10.%s.%s.101" % (str(i['real_port'])[0], str(i['real_port'])[2])
    #GATEWAY = "10.%s.%s.26" % (str(i['real_port'])[0], str(i['real_port'])[2])

    ##get_confige(NAME  =  "CPE_%s" % i['real_port'], IP = IP, GATEWAY = GATEWAY, FILE = 'config_11n.json')
    #get_confige(NAME  =  "CPE_%s" % i['real_port'], IP = IP, GATEWAY = GATEWAY, FILE = 'config_11ac.json')

    #l.upload('/tmp/oem.json', '/data/config.json')
    #l.executing('cp /data/config.json /tmp/config.json; sysconf -w; reboot')
    #threading.Thread(target = l.executing, args=['iwconfig ath0 txpower 10']).start()
    #l.executing('iwconfig ath0 txpower 13')



    # Vykdo komanda
    #threading.Thread(target = l.executing, args=['iwconfig ath0 | grep "Tx-Power"']).start()
    #threading.Thread(target = l.executing, args=['cp /tmp/config.json /data/mcast.json']).start()
    #threading.Thread(target = l.executing, args=['cp /data/config.json /tmp/config.json; sysconf -w; reboot']).start()

    #l.executing('ifconfig ath0 up')
    #time.sleep(2)

    #threading.Thread(target = l.executing, args=['dmesg | grep -i found | wc -l']).start()
    #threading.Thread(target = l.executing, args=['ifconfig br0 | grep -i "HWaddr"; ifconfig ath0 | grep -i "HWaddr"; ifconfig eth0 | grep -i "HWaddr"; ifconfig br0 | grep -i \"inet addr\"']).start()
    # Upgradina
    threading.Thread(target = l.upgrade ,args=['/tmp/latest.img']).start()
    #threading.Thread(target = l.do).start()

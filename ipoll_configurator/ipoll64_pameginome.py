from connection import connection
import paramiko
import time
import threading
from athconfiger import Configer
import scp

username = 'admin'
password = 'admin01'
pc = '10.0.10.26'

IP = [
{'ip' : '10.0.10.26', 'port' : 22111, 'user' : username, 'pass' : password, 'real_port' : '101'},
{'ip' : '10.0.10.26', 'port' : 22121, 'user' : username, 'pass' : password, 'real_port' : '102'},
{'ip' : '10.0.10.26', 'port' : 22131, 'user' : username, 'pass' : password, 'real_port' : '103'},
{'ip' : '10.0.10.26', 'port' : 22141, 'user' : username, 'pass' : password, 'real_port' : '104'},
{'ip' : '10.0.10.26', 'port' : 22151, 'user' : username, 'pass' : password, 'real_port' : '105'},
{'ip' : '10.0.10.26', 'port' : 22161, 'user' : username, 'pass' : password, 'real_port' : '106'},
{'ip' : '10.0.10.26', 'port' : 22171, 'user' : username, 'pass' : password, 'real_port' : '107'},
{'ip' : '10.0.10.26', 'port' : 22181, 'user' : username, 'pass' : password, 'real_port' : '108'},

{'ip' : '10.0.10.26', 'port' : 22211, 'user' : username, 'pass' : password, 'real_port' : '201'},
{'ip' : '10.0.10.26', 'port' : 22221, 'user' : username, 'pass' : password, 'real_port' : '202'},
{'ip' : '10.0.10.26', 'port' : 22231, 'user' : username, 'pass' : password, 'real_port' : '203'},
{'ip' : '10.0.10.26', 'port' : 22241, 'user' : username, 'pass' : password, 'real_port' : '204'},
{'ip' : '10.0.10.26', 'port' : 22251, 'user' : username, 'pass' : password, 'real_port' : '205'},
{'ip' : '10.0.10.26', 'port' : 22261, 'user' : username, 'pass' : password, 'real_port' : '206'},
{'ip' : '10.0.10.26', 'port' : 22271, 'user' : username, 'pass' : password, 'real_port' : '207'},
{'ip' : '10.0.10.26', 'port' : 22281, 'user' : username, 'pass' : password, 'real_port' : '208'},

#{'ip' : '10.0.10.26', 'port' : 22311, 'user' : username, 'pass' : passwor, 'real_port' : '301'},
#{'ip' : '10.0.10.26', 'port' : 22321, 'user' : username, 'pass' : passwor, 'real_port' : '302'},
#{'ip' : '10.0.10.26', 'port' : 22331, 'user' : username, 'pass' : passwor, 'real_port' : '303'},
#{'ip' : '10.0.10.26', 'port' : 22341, 'user' : username, 'pass' : passwor, 'real_port' : '304'},
#{'ip' : '10.0.10.26', 'port' : 22351, 'user' : username, 'pass' : passwor, 'real_port' : '305'},
#{'ip' : '10.0.10.26', 'port' : 22361, 'user' : username, 'pass' : passwor, 'real_port' : '306'},
#{'ip' : '10.0.10.26', 'port' : 22371, 'user' : username, 'pass' : passwor, 'real_port' : '307'},
#{'ip' : '10.0.10.26', 'port' : 22381, 'user' : username, 'pass' : passwor, 'real_port' : '308'},

#{'ip' : '10.0.10.26', 'port' : 22411, 'user' : username, 'pass' : passwor, 'real_port' : '401'},
#{'ip' : '10.0.10.26', 'port' : 22421, 'user' : username, 'pass' : passwor, 'real_port' : '402'},
#{'ip' : '10.0.10.26', 'port' : 22431, 'user' : username, 'pass' : passwor, 'real_port' : '403'},
#{'ip' : '10.0.10.26', 'port' : 22441, 'user' : username, 'pass' : passwor, 'real_port' : '404'},
#{'ip' : '10.0.10.26', 'port' : 22451, 'user' : username, 'pass' : passwor, 'real_port' : '405'},
#{'ip' : '10.0.10.26', 'port' : 22461, 'user' : username, 'pass' : passwor, 'real_port' : '406'},
#{'ip' : '10.0.10.26', 'port' : 22471, 'user' : username, 'pass' : passwor, 'real_port' : '407'},
#{'ip' : '10.0.10.26', 'port' : 22481, 'user' : username, 'pass' : passwor, 'real_port' : '408'},

{'ip' : '10.0.10.26', 'port' : 22511, 'user' : username, 'pass' : password, 'real_port' : '501'},
{'ip' : '10.0.10.26', 'port' : 22521, 'user' : username, 'pass' : password, 'real_port' : '502'},
{'ip' : '10.0.10.26', 'port' : 22531, 'user' : username, 'pass' : password, 'real_port' : '503'},
{'ip' : '10.0.10.26', 'port' : 22541, 'user' : username, 'pass' : password, 'real_port' : '504'},
{'ip' : '10.0.10.26', 'port' : 22551, 'user' : username, 'pass' : password, 'real_port' : '505'},
{'ip' : '10.0.10.26', 'port' : 22561, 'user' : username, 'pass' : password, 'real_port' : '506'},
{'ip' : '10.0.10.26', 'port' : 22571, 'user' : username, 'pass' : password, 'real_port' : '507'},
{'ip' : '10.0.10.26', 'port' : 22581, 'user' : username, 'pass' : password, 'real_port' : '508'},

{'ip' : '10.0.10.26', 'port' : 22611, 'user' : username, 'pass' : password, 'real_port' : '601'},
{'ip' : '10.0.10.26', 'port' : 22621, 'user' : username, 'pass' : password, 'real_port' : '602'},
{'ip' : '10.0.10.26', 'port' : 22631, 'user' : username, 'pass' : password, 'real_port' : '603'},
{'ip' : '10.0.10.26', 'port' : 22641, 'user' : username, 'pass' : password, 'real_port' : '604'},
{'ip' : '10.0.10.26', 'port' : 22651, 'user' : username, 'pass' : password, 'real_port' : '605'},
{'ip' : '10.0.10.26', 'port' : 22661, 'user' : username, 'pass' : password, 'real_port' : '606'},
{'ip' : '10.0.10.26', 'port' : 22671, 'user' : username, 'pass' : password, 'real_port' : '607'},
{'ip' : '10.0.10.26', 'port' : 22681, 'user' : username, 'pass' : password, 'real_port' : '608'},

{'ip' : '10.0.10.26', 'port' : 22711, 'user' : username, 'pass' : password, 'real_port' : '701'},
{'ip' : '10.0.10.26', 'port' : 22721, 'user' : username, 'pass' : password, 'real_port' : '702'},
{'ip' : '10.0.10.26', 'port' : 22731, 'user' : username, 'pass' : password, 'real_port' : '703'},
{'ip' : '10.0.10.26', 'port' : 22741, 'user' : username, 'pass' : password, 'real_port' : '704'},
{'ip' : '10.0.10.26', 'port' : 22751, 'user' : username, 'pass' : password, 'real_port' : '705'},
{'ip' : '10.0.10.26', 'port' : 22761, 'user' : username, 'pass' : password, 'real_port' : '706'},
{'ip' : '10.0.10.26', 'port' : 22771, 'user' : username, 'pass' : password, 'real_port' : '707'},
{'ip' : '10.0.10.26', 'port' : 22781, 'user' : username, 'pass' : password, 'real_port' : '708'},

{'ip' : '10.0.10.26', 'port' : 22811, 'user' : username, 'pass' : password, 'real_port' : '801'},
{'ip' : '10.0.10.26', 'port' : 22821, 'user' : username, 'pass' : password, 'real_port' : '802'},
{'ip' : '10.0.10.26', 'port' : 22831, 'user' : username, 'pass' : password, 'real_port' : '803'},
{'ip' : '10.0.10.26', 'port' : 22841, 'user' : username, 'pass' : password, 'real_port' : '804'},
{'ip' : '10.0.10.26', 'port' : 22851, 'user' : username, 'pass' : password, 'real_port' : '805'},
{'ip' : '10.0.10.26', 'port' : 22861, 'user' : username, 'pass' : password, 'real_port' : '806'},
{'ip' : '10.0.10.26', 'port' : 22871, 'user' : username, 'pass' : password, 'real_port' : '807'},
{'ip' : '10.0.10.26', 'port' : 22881, 'user' : username, 'pass' : password, 'real_port' : '808'}
]


class ipoll64(connection):

    def __init__(self, Device):
        connection.__init__(self, Device['ip'], Device['user'], Device['pass'], Device['port'], None)
        self.ip = Device['ip']
        self.port = Device['port']
        self.username = Device['user']
        self.password = Device['pass']
        self.lan = None
        self.real_port = Device['real_port']


    def changed_parameters(self, l):
        print self.real_port
        print l['wireless']['radio'][0]['vap'][0]['ssid2vlan']
        #l['wireless']['radio'][0]['channel']['width'] = int(40)
        #l['wireless']['radio'][0]['channel']['nonstandard'] = bool(True)
        #l['wireless']['radio'][0]['channel']['autowidth'] = bool(True)
        #l['wireless']['radio'][0]['vap'][0]['shortgi'] = bool(True)
        #l['wireless']['radio'][0]['txpower'] = int(10)
        #l['wireless']['radio'][0]['vap'][0]['wds'] = bool(True)
        #l['wireless']['radio'][0]['vap'][0]['ssid'] = str('ipoll_64')
        #l['wireless']['radio'][0]['vap'][0]['rate']['mcs'] = str('auto')
        #l['wireless']['countrycode'] = str('CX')


        #l['wireless']['radio'][0]['vap'][0]['security']['mode'] = str('open')
       
        #### WPA/ENTERPRISE
        #l['wireless']['radio'][0]['vap'][0]['security']['wpaenterprise']['authentication']['eap'] = 'peap'
        #l['wireless']['radio'][0]['vap'][0]['security']['wpaenterprise']['authentication']['password'] = 'tester'
        #l['wireless']['radio'][0]['vap'][0]['security']['wpaenterprise']['authentication']['identity'] = 'tester'
    
        #### WPA/PSK2
        #l['wireless']['radio'][0]['vap'][0]['security']['wpapsk'] = {}
        #l['wireless']['radio'][0]['vap'][0]['security']['wpapsk']['passphrase'] = '123456789'

        #print l['wireless']['radio'][0]['vap'][0]['security']['wpaenterprise']['authentication']

        return l


    def do(self):
        R = Configer(self.changed_parameters)

        if R.configure(ip = self.ip, port = self.port, usr = self.username, psw = self.password): 
            print "     Succesfull %s" % self.port
        else:
            print "     Failed %s" % self.port


    def upgrade(self, args):
        self.open_con()
        self.open_sftp(args, '/tmp/fwupdate.bin')
        self.execute('fwupdate')

    def executing(self, cmd):
        self.open_con()
        self.execute(cmd)

for i in IP:
    l = ipoll64(i)

    # Vykdo komanda
    #threading.Thread(target = l.executing, args=['cp /data/bridge.json /tmp/config.json; sysconf -w; reboot']).start()
    #threading.Thread(target = l.executing, args=['cp /tmp/config.json /data/bridge.json']).start()

    #l.executing('ifconfig ath0 up')
    #time.sleep(2)

    #threading.Thread(target = l.executing, args=['dmesg | grep -i found | wc -l']).start()
    #threading.Thread(target = l.executing, args=['ifconfig br0 | grep -i "HWaddr"; ifconfig ath0 | grep -i "HWaddr"; ifconfig eth0 | grep -i "HWaddr"; ifconfig br0 | grep -i \"inet addr\"']).start()
    # Upgradina
    #threading.Thread(target = l.upgrade ,args=['/tmp/APCPE.QM-1.v7.54-DEVEL.17365.img']).start()

    threading.Thread(target = l.do).start()
    #l.do()

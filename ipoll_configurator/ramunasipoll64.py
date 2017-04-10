from connection import connection
import paramiko
import time
import threading
from athconfiger import Configer
import scp
import sys

username = 'admin'
password = 'admin01'
pc = '10.0.10.26'

IP = [
{'ip' : '10.0.10.26', 'port' : 22111, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22121, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22131, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22141, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22151, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22161, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22171, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22181, 'user' : username, 'pass' : password},

{'ip' : '10.0.10.26', 'port' : 22211, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22221, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22231, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22241, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22251, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22261, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22271, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22281, 'user' : username, 'pass' : password},

{'ip' : '10.0.10.26', 'port' : 22311, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22321, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22331, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22341, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22351, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22361, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22371, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22381, 'user' : username, 'pass' : password},

{'ip' : '10.0.10.26', 'port' : 22411, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22421, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22431, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22441, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22451, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22461, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22471, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22481, 'user' : username, 'pass' : password},

{'ip' : '10.0.10.26', 'port' : 22511, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22521, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22531, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22541, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22551, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22561, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22571, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22581, 'user' : username, 'pass' : password},

{'ip' : '10.0.10.26', 'port' : 22611, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22621, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22631, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22641, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22651, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22661, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22671, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22681, 'user' : username, 'pass' : password},

{'ip' : '10.0.10.26', 'port' : 22711, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22721, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22731, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22741, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22751, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22761, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22771, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22781, 'user' : username, 'pass' : password},

#{'ip' : '10.0.10.26', 'port' : 22811, 'user' : username, 'pass' : password},
#{'ip' : '10.0.10.26', 'port' : 22821, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22831, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22841, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22851, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22861, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22871, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.26', 'port' : 22881, 'user' : username, 'pass' : password}
]


class ipoll64(connection):

    def __init__(self, Device):
        connection.__init__(self, Device['ip'], Device['user'], Device['pass'], Device['port'], None)
        self.ip = Device['ip']
        self.port = Device['port']
        self.username = Device['user']
        self.password = Device['pass']
        self.lan = None


    def changed_parameters(self, l):
        #l['wireless']['radio'][0]['channel']['width'] = int(40)
        #l['wireless']['radio'][0]['vap'][0]['shortgi'] = bool(True)
        #l['wireless']['radio'][0]['vap'][0]['ssid'] = 'ipoll_64_1'
        #l['wireless']['radio'][0]['txpower'] = int(10)
        #l['wireless']['radio'][0]['vap'][0]['wds'] = bool(True)
        #l['wireless']['radio'][0]['vap'][0]['rate']['mcs'] = str('auto')
        #l['wireless']['countrycode'] = str('LT')
        #l['services']['discovery'] = bool(True)
        #print l['services']['discovery']

        # Security 


        #l['wireless']['radio'][0]['vap'][0]['security']['mode'] = 'wpapsk'
        ####['mode'] = 'open' \ 'wep' \ 'uam' \ 'wpaenterprise'

        #### WPA/ENTERPRISE
        #l['wireless']['radio'][0]['vap'][0]['security']['wpaenterprise']['authentication']['eap'] = 'peap'
        #l['wireless']['radio'][0]['vap'][0]['security']['wpaenterprise']['authentication']['password'] = 'tester'
        #l['wireless']['radio'][0]['vap'][0]['security']['wpaenterprise']['authentication']['identity'] = 'tester'

        #### WPA/PSK2
        #l['wireless']['radio'][0]['vap'][0]['security']['wpapsk'] = {}
        #l['wireless']['radio'][0]['vap'][0]['security']['wpapsk']['passphrase'] = 'ipoll_64_6'

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
    #print i
    l = ipoll64(i)

    #### Vykdo komanda
    threading.Thread(target = l.executing, args=['ifconfig ath0 down']).start()
    # threading.Thread(target = l.executing, args=['iwpriv wifi0 chan_step 5; iwpriv wifi0 chan_bw 5']).start()
    # threading.Thread(target = l.executing, args=['iwconfig ath0 txpower 5']).start()
    #l.executing('radartool numdetects')
    #threading.Thread(target = l.executing, args=['uptime']).start()
    #### Upgradina
    #threading.Thread(target = l.upgrade ,args=['/tmp/latest.img']).start()
    ### Keicia Konfiga
    #threading.Thread(target = l.do).start()

from connection import connection
import paramiko
import time
import threading
from athconfiger import Configer
import scp
import sys

username = 'admin'
password = 'admin01'

IP = [
#{'ip' : '10.0.10.26', 'port' : 22871, 'user' : username, 'pass' : password},
{'ip' : '10.0.10.19', 'port' : 22, 'user' : username, 'pass' : password}
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
    #threading.Thread(target = l.executing, args=['ifconfig ath0 down']).start()
    # threading.Thread(target = l.executing, args=['iwpriv wifi0 chan_step 5; iwpriv wifi0 chan_bw 5']).start()
    # threading.Thread(target = l.executing, args=['iwconfig ath0 txpower 5']).start()
    #l.executing('radartool numdetects')
    #threading.Thread(target = l.executing, args=['uptime']).start()
    #### Upgradina
    threading.Thread(target = l.upgrade ,args=['/tmp/latest.img']).start()
    ### Keicia Konfiga
    #threading.Thread(target = l.do).start()

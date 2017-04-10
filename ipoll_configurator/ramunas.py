from connection import connection
import paramiko
import time
import threading
from athconfiger import Configer
import scp

username = 'admin'
password = 'admin01'
pc = '10.1.1.1'

IP = [
{'ip' : pc, 'port' : 22, 'user' : username, 'pass' : password}
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
        l['wireless']['radio'][0]['txpower'] = int(24)
        #l['wireless']['radio'][0]['vap'][0]['wds'] = bool(True)
        #l['wireless']['radio'][0]['vap'][0]['rate']['mcs'] = str('auto')
        #l['wireless']['countrycode'] = str('BR')
        
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
    print i
    l = ipoll64(i)
    
    CMD = ''
    for a in range(1, 65, 1):
        CMD += '/sbin/ip l set peer%s txqueuelen 1; ' % a

    print CMD
    #l.executing([CMD])
    #threading.Thread(target = l.executing, args=[CMD ]).start()

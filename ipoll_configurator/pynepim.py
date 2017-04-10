import os
import subprocess
import re
import time
from threading import Thread, Event
import paramiko


class Pynepim:

    def __init__(self, ip='192.168.199.100', client_ip='192.168.51.112', username = 'wili', password = 'sauletekio15'):

        self.ip = ip
        self.client_ip = client_ip
        self.username = username
        self.password = password

        self.duration = 60
        self.direction = '-d'
        self.pckt_size = 1500
        self.burst = '95'

        self.results_file = '/tmp/thr.results'
        self.server_RAW = []
        self.client_RAW = []
        self.reg_avg = re.compile(r'(.*)(avg)(\s*)(\d*)(\s*)(\d*.\d*)(\s*)(\d*.\d*)')
        self.reg_cur = re.compile(r'(.*)(cur)(\s*)(\d*)(\s*)(\d*.\d*)(\s*)(\d*.\d*)')
        self.proccess = 'nepim'
        self.nepim_server_params = []
        self.nepim_client_params = ''



    def prepare(self):
        self.set_nepim_server()
        self.set_nepim_client()


    def set_server_params(self, params):
        self.nepim_server_params = params


    def set_client_params(self, params):
        self.nepim_client_params = params


    def set_nepim_server(self):
        self.nepim_server = []
        self.nepim_server.append(self.proccess)
        for i in self.nepim_server_params:
            self.nepim_server.append(i)


    def set_nepim_client(self):
        self.nepim_client = '%s -c %s -i 1 -a %s %s %s' % (self.proccess, self.ip, self.duration, self.direction, self.nepim_client_params)


    def set_duration(self, duration):
        self.duration = duration


    def set_direction(self, direciton):
        '''
        '-d' - DUPLEX
        '-s' - OUT
        ''   - IN
        '''
        self.direction = direciton


    def set_pckt_size(self, pckt_size):
        self.pckt_size = pckt_size


    def set_burst(self, burst):
        self.burst = burst


    def calculate(self, RAW, skip=-1):
        results = []
        for r in RAW:
            r = r.strip()

            FE = self.reg_cur.search(r)
            ME = self.reg_cur.match(r)

            if ME != None:
                if skip < 0:
                    results.append( ( float(FE.groups()[5]) )/1024 )
                skip -= 1

        return round(sum(results) / float(len(results)), 1)


    def run_server(self):
        print self.nepim_server
        popen = subprocess.Popen(self.nepim_server, stdout=subprocess.PIPE)
        lines_iterator = iter(popen.stdout.readline, b"")
        for line in lines_iterator:
            print line
            self.server_RAW.append(line)


    def kill_server(self):
        command = ['pkill', 'nepim']
        p = subprocess.Popen(command, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        RAW, err = p.communicate() 

    def run_client(self):
        print self.nepim_client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.client_ip, username = self.username, password = self.password)
        stdin, stdout, stderr = ssh.exec_command(self.nepim_client)
        RAW = stdout.readlines()
        ssh.close()
        return RAW

    def start(self, direction = '-d'):
        self.set_direction(direction)

        self.prepare()
        self.server_RAW = []
        self.client_RAW = []


        Thread(target=self.run_server).start()
        time.sleep(1)
        self.client_RAW = self.run_client()
        time.sleep(1)
        self.kill_server()

        if self.direction == '-d':
            return self.calculate(self.server_RAW) + self.calculate(self.client_RAW, skip = -1)

        elif self.direction == '-s':
            return self.calculate(self.server_RAW)

        elif self.direction == '':
            return self.calculate(self.client_RAW) 

'''
results_file = '/tmp/thr.nepim'
os.system('rm %s' % results_file)

# self, ip='192.168.199.100', client_ip='192.168.51.112', username = 'wili', password = 'sauletekio15'
p = Pynepim(ip='192.168.199.100', client_ip='192.168.101.48', username = 'tester', password = 'tester')
p.set_duration(60)

p.set_client_params('')
p.set_server_params([])
DUPLEX = p.start('-d') 
OUT = p.start('') 
IN = p.start('-s') 


p.set_client_params('-u')
p.set_server_params([])
DUPLEX_u = p.start('-d') 
OUT_u = p.start('')
IN_u = p.start('-s')


print "TCP: DUPLEX: %s | AP->STA: %s | STA->AP: %s" % (DUPLEX, OUT, IN)
print "UDP: DUPLEX: %s | AP->STA: %s | STA->AP: %s" % (DUPLEX_u, OUT_u, IN_u)

#for pckt_size in [64, 65, 127, 128, 255, 256, 511, 512, 1023, 1024, 1399, 1400, 1499, 1500]:
for pckt_size in [64, 1500]:
    p.set_client_params('-u -W %s -r 95M' % pckt_size)
    p.set_server_params(['-W', '%s' % pckt_size])


    OUT = p.start('')
    IN = p.start('-s')
    DUPLEX = p.start()
    print "%s |%s %s %s|" % (pckt_size, DUPLEX, IN, OUT)

    fm = open(results_file, 'a')
    fm.writelines("| %s | %s %s %s |\n" % (pckt_size, DUPLEX, IN, OUT))
    fm.close()
'''

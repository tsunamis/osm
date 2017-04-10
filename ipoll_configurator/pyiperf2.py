import os
import subprocess
import re
import time
import threading
#from threading import Thread, Event
import paramiko
import select
from configs import *
import csv
import string
import Queue


class iperf:

    def __init__(self, PC, IP, SERVER = True, ID = 9001, protocol = '', direction = '-d', duration = 60, burst = 100, traffic_type = None):
        self.PC = PC
        self.IP = IP
        self.PID = None
        self.SERVER = SERVER         # 'server', 'client'
        self.stop = False
        self.RAW = []
 
        # Parameters
        self.ID = ID
        self.duration = duration
        self.direction = direction     # '' - Server->Client, '-r' Server->CLient|Client->Server, '-d' - Duplex
        self.burst = burst
        self.protocol = protocol        # '' - TCP, '-u' - UDP

        self.proto = ''           # '' - TCP, '-u -b xM' - UDP

        if self.protocol == '-u':
            self.proto = '%s -b %sM' % (self.protocol, self.burst)

        #QOS
        qos = ''
        if traffic_type != None:
            TOS = { 'tosL' : '0x20', 'tosM' : '0x60', 'tosH' : '0xA0', 'tosU' : '0xE0' }
            tos = TOS[traffic_type]
            qos = '-S %s' % tos

        self.proccess = 'iperf -c %s -i 1 -t %s %s -y c -p %s -P 1  %s %s'     % (self.IP, self.duration, self.direction, self.ID, self.proto, qos)

        if self.SERVER == True:
            self.proccess = 'iperf -s    -i 1          -y c -p %s -B %s %s' % (self.ID, self.IP, self.protocol)


        '''
        UDP Duplex     iperf -c 10.0.94.104 -P 1 -i 1 -f m -t 60 -d -u -b 100M
                       iperf -s -P 1 -i 1 -f m -u 

        TCP Duplex     iperf -c 10.0.85.103 -P 1 -i 1 -f m -t 60 -d
                       iperf -s -P 1 -i 1 -f m

        UDP Simplex    iperf -c 10.0.83.103 -P 1 -i 1 -f m -t 60 -u -b 100M
                       iperf -s -P 1 -i 2 -f m -u
                 
        TCP Simplex    iperf -c 10.0.95.200 -P 1 -i 1 -f m -t 60
                       iperf -s -P 1 -i 1 -p 5001 -f m
        '''
       

    def run_traffic_generator(self):
        host = self.PC['ip']
        port = self.PC['port']
        username = self.PC['user']
        password = self.PC['pass']

        print "%s %s" % (host, self.proccess)

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port = port, username = username, password = password)

        stdin, stdout, stderr = client.exec_command('echo $$; exec ' +  self.proccess)
        self.PID = int(stdout.readline())
        print self.PID

        # Wait for the command to terminate
        while not stdout.channel.exit_status_ready():
            # Only print data if there is data to read in the channel
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                     self.RAW.append(stdout.channel.recv(1024),)

        print "Pabaige matuoti %s" % self.proccess
        self.stop = True
        client.close()


    def kill(self):
        if self.PID != None:
            host = self.PC['ip']
            port = self.PC['port']
            username = self.PC['user']
            password = self.PC['pass']

            print "Kilinu iperf'a"
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, port = port, username = username, password = password)
            stdin, stdout, stderr = client.exec_command('kill -9 %s' % self.PID)
            client.close()       


    def convert_to_csv(self):

        results = []
        zz = string.split(self.RAW, '\n') 
    
        for i in zz:
            for row in csv.reader([i]):
                if len(row) > 0:
                    element = {}
                    # timestamp, server_ip, server_port, client_ip, client_port, tag_id, interval, transferred, bandwidth
                    '''
                    timestap, 
                    server IP, 
                    server port, 
                    client IP, 
                    client port, 
                    iperf process number, 
                    time interval, 
                    amount of data transferred (bytes), 
                    bandwidth (bits per second), 
                    jitter (milliseconds), 
                    number of lost datagrams, 
                    total number of datagrams sent, 
                    percentage loss, 
                    number of datagrams received out of order
                    '''
                    element['timestamp'] = row[0]
                    element['server_ip'] = row[1] 
                    element['server_port'] = int(row[2])
                    element['client_ip'] = row[3] 
                    element['client_port'] = int(row[4])
                    element['tag_id'] = int(row[5])
                    element['interval'] = self.split_interval(row[6])
                    l = [float(i) for i in row[6].split('-')]
                    element['start'] = l[0]
                    element['end'] = l[1]
                    element['transferred'] = int(row[7])
                    element['bandwidth'] = int(row[8])
                    if len(row) > 9:
                        element['jitter'] = row[9]
                        element['lost_datagram'] = row[10]
                        element['total_datagrams'] = row[11]
                        element['percentage_loss'] = row[12]
                        element['datagrams_ofo'] = row[13]

                    results.append(element)
        return results

    def split_interval(self, s):
        i = s.split('-')
        return [float(i[0]), float(i[1])]

    def get_results(self):
        self.RAW = self.beautifier(self.RAW)
        return self.convert_to_csv()

    def beautifier(self, l):
        r = ''
        for i in l:
            r += i
        return r

    def return_stop(self):
        return self.stop

    def return_duration(self):
        return self.duration


class Pyiperf:

    def __init__(self, LPC, RPC):

        self.LPC = LPC
        self.RPC = RPC
        self.IP = RPC['lan']

        self.results_file = '/tmp/thr.results'

    def start(self, q = Queue.Queue(0), protocol = 't', direction = 'd', duration = 60, burst = 100, traffic_type = None, ID = None):
        print "%s %s %s %s %s" % (protocol, direction, duration, burst, traffic_type)
        '''
        protocol = [u - UDP, t - TCP]
        direction = [d - Duplex, r - Simplex]
        '''
        if protocol == 'u':
            protocol = '-u'
        elif protocol == 't':
            protocol = ''
        else:
            protocol = ''

        if direction == 'd':
            direction = '-d'
        elif direction == 'r':
            direction = '-r'
        else:
            direction = '-d'

        if ID == None:
            ID = 5001
        #self.swap_side()

        #__init__(self, PC, IP, MODE = 'server', ID = 9001)
        server = iperf(self.RPC, self.IP, SERVER = True, ID = ID, protocol = protocol, direction = direction, duration = duration, burst = burst)
        client = iperf(self.LPC, self.IP, SERVER = False, ID = ID, protocol = protocol, direction = direction, duration = duration, burst = burst, traffic_type = traffic_type)
 

        threading.Thread(target = server.run_traffic_generator).start()
        threading.Thread(target = client.run_traffic_generator).start()

        c = 0
        while server.return_stop() == False and client.return_stop() == False:
            print ">>>>>>>    Dar nebaige darba [%s] server:[%s] client:[%s] Duration: %s" % (c, server.return_stop(), client.return_stop(), c)
            if c > (duration * 2.2):
                break
            time.sleep(1)
            c +=1

        server.kill()
        client.kill()


        SERVER = []
        for i in server.get_results():
            if i['server_port'] == ID:
                if int(i['end']) - int(i['start']) == 1:
                    SERVER.append(i['bandwidth'])
        
        CLIENT = []
        for i in client.get_results():
            if i['server_port'] == ID:
                if int(i['end']) - int(i['start']) == 1:
                    CLIENT.append(i['bandwidth'])

        ToServer = None
        if len(SERVER) > 0:
            ToServer = round(self.bytesto(sum(SERVER)/len(SERVER), 'm'), 1)

        ToClient = None
        if len(CLIENT) > 0:
            ToClient = round(self.bytesto(sum(CLIENT)/len(CLIENT), 'm'), 1)

        print [traffic_type, ToServer, ToClient]
        q.put([traffic_type, ToServer, ToClient])
        return ToServer, ToClient

    #deg start(self, q = Queue.Queue(0), protocol = 't', direction = 'd', duration = 60, burst = 100, traffic_type = 'tosU', ID = None):
    def start_qos(self, protocol = 'u', direction = 'd', duration = 60, burst = 100):
        threadList = ["tosU", "tosH", "tosM", "tosL"]
        #threadList = ["tosH", "tosH", "tosH", "tosH"]
        #threadList = ["tosU", "tosL"]
        queueLock = threading.Lock()
        workQueue = Queue.Queue(10)
        threads = []


        ID = 5001
        for tName in threadList:
            print tName
            thread = threading.Thread(target = self.start, args = (workQueue, protocol, direction, duration, burst, tName, ID))
            thread.start()
            threads.append(thread)
            ID += 1

         # Wait for all threads to complete
        for t in threads:
            print "!!!!!!!!!!!!!!!!!!!!!!!!! %s" % t
            t.join()
        

        while not workQueue.empty():
            val = workQueue.get()
            print "Outputting: ", val


        #print "!!!!!!!!!!!! Jau pabaigiau darba !!!!!!!!!!!!!!!!!!!!!!!"
        #print workQueue.get()

            #thread = myThread(threadID, tName, workQueue)
            #thread.start()
            #threads.append(thread)
            #threadID += 1

        #queueLock.acquire()
        #queueLock.release()

        '''
        # Create new threads
                                                #protocol = 't', direction = 'd', duration = 60, burst = 100, traffic_type = '0xE0'
        thread1 = threading.Thread(target = self.start, args = (q, 'u', 'd', duration, 20, 'tosU',)).start()
        thread2 = threading.Thread(target = self.start, args = (q, 'u', 'd', duration, 20, 'tosH',)).start()
        thread3 = threading.Thread(target = self.start, args = (q, 'u', 'd', duration, 20, 'tosM',)).start()
        thread4 = threading.Thread(target = self.start, args = (q, 'u', 'd', duration, 20, 'tosL',)).start()

        threads.append(thread1)
        threads.append(thread2)
        threads.append(thread3)
        threads.append(thread4)

        #for t in threads:
        #    print "Joininu %s" % t
        #    t.join()
 
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11111value bandau gauti"
        func_value = q.get()
        print func_value
        '''

    def bytesto(self, bytes, to, bsize=1024):
        """convert bytes to megabytes, etc.
        sample code:
        print('mb= ' + str(bytesto(314575262000000, 'm')))
        sample output:
        mb= 300002347.946
        """
         
        a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
        r = float(bytes)
        for i in range(a[to]):
            r = r / bsize
         
        return(r) 

a = Pyiperf(LPC, RPC)
a.start_qos()

'''
# examples:

i = Pyiperf(LPC, RPC)

age = 10
s = {}
s['UD'] =  i.start(protocol = 'u', direction = 'd', duration = age, burst = 400)
s['US'] = i.start(protocol = 'u', direction = 'r', duration = age, burst = 800)
s['TD'] = i.start(protocol = 't', direction = 'd', duration = age)
s['TS'] = i.start(protocol = 't', direction = 'r', duration = age)

print "UDP Duplex - %s UDP - Simplex%s  TCP - Duplex%s TCP - Simplex %s" % ( s['UD'], s['US'], s['TD'], s['TS'])
'''

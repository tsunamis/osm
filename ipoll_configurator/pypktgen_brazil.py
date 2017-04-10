import os

class pypktgen:

    def __init__(self):
        self.Pc = "/proc/net/pktgen/pgctrl" 
        self.c = 0

    def start(self):
        cmd = "echo \"start\" > %s" % self.Pc
        os.system(cmd)

    def stop(self):
        cmd = "echo \"stop\" > %s" % self.Pc
        os.system(cmd)

    def add_peer(self, l, i):
        self.c += 1
        INDEX = 0
        if self.c > 2:
            INDEX = 1
        IFACE = l['iface']
        MAC = l['mac']
        SRC = l['src']
        DST = l['dst']
        PKT_SIZE = 64
        DELAY = 1
        PACKETS = 0

        Pq = "/proc/net/pktgen/kpktgend_%s" % INDEX
        Pi = "/proc/net/pktgen/%s" % IFACE
        Pc = self.Pc

        print "%s %s %s %s %s %s %s %s" % (Pc, Pq, Pi, INDEX, IFACE, MAC, SRC, DST)

        #os.system("echo \"stop\" > %s" % self.Pc)
        #os.system("echo \"rem_device_all\" > %s" % Pq)
        os.system("echo \"add_device %s\" > %s" % (IFACE, Pq))

        os.system("echo \"clone_skb 0\" > %s" % Pi)
        os.system("echo \"min_pkt_size %s\" > %s" % (PKT_SIZE, Pi))
        os.system("echo \"max_pkt_size %s\" > %s" % (PKT_SIZE, Pi))
        os.system("echo \"dst_min %s\" > %s" % (DST, Pi))
        os.system("echo \"dst_max %s\" > %s" % (DST, Pi))
        os.system("echo \"src_min %s\" > %s" % (SRC, Pi))
        os.system("echo \"src_max %s\" > %s" % (SRC, Pi))
        os.system("echo \"dst_mac %s\" > %s" % (MAC, Pi))
        os.system("echo \"delay %s\" > %s" % (DELAY, Pi))
        os.system("echo \"count %s\" > %s" % (PACKETS, Pi))

    def peers(self, r = 9, p = 9):
        l = []
        '''
        for rack in range(1, r, 1): 
            for pcba in range(1, p, 1):
                e = {}
                e['iface'] = 'virt%s%s' % (rack, pcba)
                e['mac'] = "80:1f:02:00:0%s:0%s" % (rack, pcba)
                if rack > 5:
                    e['mac'] = "68:05:ca:29:0%s:0%s" % (rack, pcba)
                e['src'] = '10.%s.%s.27' % (rack, pcba)
                e['dst'] = '10.%s.%s.26' % (rack, pcba)

                l.append(e)
        '''
        e = {}
        e['iface'] = 'virt41'
        e['mac'] = '80:1f:02:00:04:01'
        e['src'] = '10.4.1.27'
        e['dst'] = '10.4.1.26'
        l.append(e)

        e = {}
        e['iface'] = 'virt42'
        e['mac'] = '80:1f:02:00:04:02'
        e['src'] = '10.4.2.27'
        e['dst'] = '10.4.2.26'
        l.append(e)

        e = {}
        e['iface'] = 'virt43'
        e['mac'] = '80:1f:02:00:04:03'
        e['src'] = '10.4.3.27'
        e['dst'] = '10.4.3.26'
        l.append(e)

        e = {}
        e['iface'] = 'virt44'
        e['mac'] = '80:1f:02:00:04:04'
        e['src'] = '10.4.4.27'
        e['dst'] = '10.4.4.26'
        l.append(e)

        e = {}
        e['iface'] = 'virt45'
        e['mac'] = '80:1f:02:00:04:05'
        e['src'] = '10.4.5.27'
        e['dst'] = '10.4.5.26'
        l.append(e)

        return l

    def run(self):

        os.system("rmmod pktgen")
        os.system("modprobe pktgen")
        #self.stop()

        L = self.peers(r = 9, p = 9)
 
        for p in L:
            print L.index(p) 
            self.add_peer(p, L.index(p))

        #for i in range(10):
        #print i
        self.start()

pktgen = pypktgen()
pktgen.run()
os.system("rmmod pktgen")

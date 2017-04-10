import sys
from pynepim import Pynepim

#results_file = '/tmp/thr.nepim'
#os.system('rm %s' % results_file)

# self, ip='192.168.199.100', client_ip='192.168.51.112', username = 'wili', password = 'sauletekio15'

#print len(sys.argv)
#sys.exit(255)

if len(sys.argv) < 2:
    G = 2
else:
    G = int(sys.argv[1])
    

duration = 60
ip = '192.168.199.1'
ip2G = '172.17.0.5'
ip5G = '172.17.0.4'

rate = int(866.7 * 0.7)

client_ip= ip5G
if G == 2:
    client_ip = ip2G
elif G == 5:
    client_ip = ip5G
else:
    print(" Add value 2 or 5")
    sys.exit(255)



p = Pynepim(ip=ip, client_ip=client_ip, username = 'tester', password = 'tester')
p.set_duration(duration)
p.set_client_params('')
p.set_server_params([])
DUPLEX = p.start('-d')

p = Pynepim(ip=ip, client_ip=client_ip, username = 'tester', password = 'tester')
p.set_duration(duration)
p.set_client_params('')
p.set_server_params([])
OUT = p.start('') 

p = Pynepim(ip=ip, client_ip=client_ip, username = 'tester', password = 'tester')
p.set_duration(duration)
p.set_client_params('')
p.set_server_params([])
IN = p.start('-s') 



#p = Pynepim(ip=ip, client_ip=client_ip, username = 'tester', password = 'tester')
#p.set_duration(duration)
#p.set_client_params('-u -r '+str(rate/2)+'M')
#p.set_server_params([])
#DUPLEX_u = p.start('-d') 
#
#p = Pynepim(ip=ip, client_ip=client_ip, username = 'tester', password = 'tester')
#p.set_duration(duration)
#p.set_client_params('-u -r '+str(rate)+'M')
#p.set_server_params([])
#OUT_u = p.start('')
#
#p = Pynepim(ip=ip, client_ip=client_ip, username = 'tester', password = 'tester')
#p.set_duration(duration)
#p.set_client_params('-u -r '+str(rate)+'M')
#p.set_server_params([])
#IN_u = p.start('-s')



print "TCP: DUPLEX: %s | AP->STA: %s | STA->AP: %s" % (DUPLEX, OUT, IN)
#print "UDP(%s): DUPLEX: %s | AP->STA: %s | STA->AP: %s" % (rate, DUPLEX_u, OUT_u, IN_u)

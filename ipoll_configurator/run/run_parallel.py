try:
    from concurrent.futures import ThreadPoolExecutor
    from concurrent.futures import as_completed as future_completed
except ImportError as e:
    # XXX: die("please run 'pip install --user futures'")
    print "please run 'pip install --user futures'"
import os
import sys
import random
import time
import paramiko

CLI=56
SERVER=2

def run_mcast_nepim(p):
    print '192.168.199.%s' % (80+p)
    #os.system('ssh spc%s "iperf -s -u -B 224.0.55.55 -i 1 > /dev/null 2>&1 &" ' % (p, 80+p))
    os.system('ssh spc%s "iperf -s -u -B 224.0.55.55 -i 1 > /dev/null 2>&1 &" ' % p)

def run_mcast_nepim1(p):
    print '192.168.199.%s' % (80+p)
    #os.system('ssh spc%s "iperf -s -u -B 224.0.55.55 -i 1 > /dev/null 2>&1 &" ' % (p, 80+p))
    os.system('ssh tpc%s "iperf -c 224.0.55.55 -u -b 1M -t 99999999 > /dev/null 2>&1 &" ' % p)

def up(p):
    print '192.168.199.%s' % (80+p)
    os.system('ssh spc%s sshpass -p admin01 ssh admin@192.168.199.%s "/sbin/ifconfig ath0 up" ' % (p, 80+p))

def reboot(p):
    print '192.168.199.%s' % (80+p)
    os.system('ssh spc%s sshpass -p admin01 ssh admin@192.168.199.%s "/sbin/ifconfig ath0 down" ' % (p, 80+p))
    time.sleep(60)
    os.system('ssh spc%s sshpass -p admin01 ssh admin@192.168.199.%s "/sbin/ifconfig ath0 up" ' % (p, 80+p))

def connect(p):
    print '192.168.199.%s' % (80+p)
    os.system('ssh spc%s /home/tester/bin/test_wxee_atheros.py 192.168.199.%s' % (p, 80+p))



L = [range(1, 9, 1), range(9, 17, 1), range(17, 25, 1), range(25, 33, 1), range(33, 41, 1), range(41, 49, 1), range(49, 57, 1)]

with ThreadPoolExecutor(max_workers=64) as executor:

    jobs = []
    #for p in range(1, 57, 1):
    for p in range(1, CLI+1, 1):
        jobs.append(executor.submit(run_mcast_nepim, p))

    for future in future_completed(jobs):
        try:
            data = future.result()
        except Exception as e:
            print "Nepavyko"

time.sleep(5)

with ThreadPoolExecutor(max_workers=64) as executor:

    jobs = []
    #for p in range(1, 57, 1):
    for p in range(1, SERVER+1, 1):
        jobs.append(executor.submit(run_mcast_nepim1, p))

    for future in future_completed(jobs):
        try:
            data = future.result()
        except Exception as e:
            print "Nepavyko"

sys.exit(1)

for i in range(500):
    l = L[random.randrange(len(L))]
    print l

    with ThreadPoolExecutor(max_workers=8) as executor:

        jobs = []
        for p in l:
            jobs.append(executor.submit(reboot, p))

        for future in future_completed(jobs):
            try:
                data = future.result()
            except Exception as e:
                print "Nepavyko"

    print "Einu pamiegoti, kol CPE bootinsis"
    #time.sleep(20)

    #with ThreadPoolExecutor(max_workers=8) as executor:

    #    jobs = []
    #    for p in l:
    #        jobs.append(executor.submit(connect, p))

    #    for future in future_completed(jobs):
    #        try:
    #            data = future.result()
    #        except Exception as e:
    #            print "Nepavyko"

    #time.sleep(1)
    
    COUNT = 0
    STOP = 60
    while COUNT < STOP:
        COUNT += 1
        print "Bandau paziureti kiek CPE prisijunge. [%s]" % COUNT

        con = paramiko.SSHClient()
        con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        con.connect('172.17.0.2', port = 22, username = 'tester', password = 'tester')
        stdin, stdout, stderr = con.exec_command('sshpass -p 10173440 ssh -p 1984 public@192.168.199.254 "wlanconfig ath0 list | wc -l"')
        cpe = int(stdout.readlines()[0])

        print cpe
        if cpe == 79:
            print "Jau prisijunge visi!!!"
            COUNT = STOP


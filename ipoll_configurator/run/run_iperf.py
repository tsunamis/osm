import os

for i in range(1, 8, 1):
    for j in range(1, 9, 1): 
        bind="10.%s.%s.27" % (i, j)
        port = "50%s%s" % (i, j)
        #cmd1 = "iperf -s -i 10 -p %s -B %s &" % (port, bind)
        cmd1 = "iperf -s -i 10 -p %s -B %s -u &" % (port, bind)
        os.system(cmd1)

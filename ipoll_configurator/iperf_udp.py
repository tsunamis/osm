import os

for i in range(1, 9, 1):
    for j in range(1, 9, 1): 
        bind="10.%s.%s.27" % (i, j)
        port = "50%s%s" % (i, j)
        cmd1 = "iperf -s -i 10 -u -p %s -B %s &" % (port, bind)
        os.system(cmd1)

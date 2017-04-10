from connection import connection
import time
import json
import sys

class ptp(connection):

    def __init__(self, Device):
        connection.__init__(self, Device['ip'], Device['user'], Device['pass'], Device['port'], Device['lan'])
        self.Device = Device
        print "ptp"

    def beautifier(self, text):
        a = ''
        for iii in text:
            a = a + iii
        return a

    def change_frequency(self, frequency = 5180):
        self.open_con()
        cfg = self.read_file_to_json('/tmp/config.json')

        print cfg['channel']
        cfg['channel']['list'] = [int(frequency)]                                # Only for PTP
        cfg['channel']['select'] = str('list')                        # Only for PTP
        print cfg['channel']

        self.write_to_json('/tmp/config.json', cfg)
        
        output, error = self.execute('sysconf -w')
        print "%s %s" % (output, error)

        self.close_con()



    def change_width(self, width = '20'):
        extension = 'upper'
        if str(width) == '40-':
           width = '40'
           extension = 'lower'

        if str(width) == '40+':
            width = '40'
            extension = 'upper'

        self.open_con()
        cfg = self.read_file_to_json('/tmp/config.json')

        print cfg['channel']
        cfg['channel']['width'] = int(width)                                    # Only for PTP
        print cfg['channel']

        self.write_to_json('/tmp/config.json', cfg)

        output, error = self.execute('sysconf -w')
        print "%s %s" % (output, error)

        self.close_con()


    def get_wireless_stats(self):
        content = []

        try:
            self.open_con()
            output, error = self.execute('stats -w')
            print "%s %s" % (output, error)
            time.sleep(1)
            output, error = self.execute('cat /var/run/stats/wireless.json')
            print  ">>>> get_stats >>>> %s %s" % (output, error)
            RAW = json.loads(self.beautifier(output))
            tmp_l = {}
            tmp_l['bitrate'] = str(RAW['radios']["dev"]["wifi0"]["bitrate"])
            tmp_l['txRate'] = str(RAW["peers"][0]["txRate"])
            tmp_l['rxRate'] = str(RAW["peers"][0]["rxRate"])
            tmp_l['signal'] = RAW["peers"][0]["signal"]
            content.append(tmp_l)
            self.close_con()
        except:
            pass

        return content

    def get_cac(self):
        content = None

        try:
            self.open_con()

            output, error = self.execute('stats -p')
            print "%s %s" % (output, error)
            time.sleep(1)
            output, error = self.execute('cat /var/run/stats/periodic.json')
            print  ">>>> get_cac >>>> %s %s" % (output, error)
            RAW = json.loads(self.beautifier(output))

            content = int(RAW['wireless'][0]['cacPeriod'])

            self.close_con()
        except:
            pass

        return content


    def get_chan_list(self, bw = 0, country='US', step = 5):
        channel = []
        bw_athtool = '0'
        bw_real = 'ht20'

        if str(bw) == str('5'):
            bw_athtool = '5'
            bw_real = 'ht5'
        elif str(bw) == str('10'):
            bw_athtool = '10'
            bw_real = 'ht10'
        elif str(bw) == str('20'):
            bw_athtool = '20'
            bw_real = 'ht20'
        elif str(bw) == str('40-'):
            bw_athtool = '20'
            bw_real = 'ht40-'
        elif str(bw) == str('40+'):
            bw_athtool = '20'
            bw_real = 'ht40+'
        elif str(bw) == str('80'):
            bw_athtool = '20'
            bw_real = 'vht80'

        print "%s - %s" % (bw, 'athtool -c %s:%s:0:%s -j' % (step, bw_athtool, country))
        try:
            self.open_con()
            output, error = self.execute('athtool -c %s:%s:0:%s -j' % (step, bw_athtool, country) )
            a = self.beautifier(output)
            self.close_con()
            CH = json.loads(a)
            for ch in CH:
                if ch['mode'] == str(bw_real):
                    channel.append(ch['freq'])
        except:
            pass

        return channel

    def reboot(self, type='', command = 'reboot'):
        self.open_con()

        if type == '-f':
            command = "%s -f" % comannd

        output, error = self.execute(command)
        print "%s %s" % (output, error)

        self.close_con()

    def get_real_width(self):
        content = None

        try:
            self.open_con()
            output, error = self.execute('stats -w')
            time.sleep(2)
            output, error = self.execute('cat /var/run/stats/wireless.json')
            print "%s %s" % (output, error)

            text = json.loads(self.beautifier(output))
            print json.dumps(text['radios']['dev']['wifi0'], indent = 4)
            content = str(text['radios']['dev']['wifi0']['channelWidth'])

            self.close_con()

        except:
            print "        >>> Can't parse channel"
            pass

        return content



    def get_real_channel(self):
        content = None

        try:
            self.open_con()
            output, error = self.execute('stats -w')
            time.sleep(2)
            output, error = self.execute('cat /var/run/stats/wireless.json')
            print "%s %s" % (output, error)
 
            text = json.loads(self.beautifier(output))
            print json.dumps(text['radios']['dev']['wifi0'], indent = 4)
            content = int(text['radios']['dev']['wifi0']['frequency'])

            self.close_con()
        except:
            print "        >>> Can't parse channel"
            pass

        return content

    def run_cmd(self, cmd=''):
        self.open_con()
        output, error = self.execute(str(cmd))
        print "%s %s" % (output, error) 
        self.close_con()

    def check_channel_width(self, CH, BW):
        status = False
        CH1 = self.get_real_channel()
        BW1 = self.get_real_width()

        print "KA GAVAU %s %s" % (CH1, BW1)
        print "KA NORIU GAUTI %s %s" % (CH, BW)

        if CH1 and BW1:
            print "%s %s %s %s" % (CH, BW, CH1, BW1)
            if (int(CH) == int(CH1)) and (str(BW) == str(BW1)):
                status = True

        return status


#!/usr/bin/python

import os, sys
import re
import getopt
import string
import paramiko
import socket
from ConfigParser import ConfigParser

PKTGEN_THREAD_FILE = "/proc/net/pktgen/kpktgend_0"
PKTGEN_IFACE_FILE_FMT = "/proc/net/pktgen/%s"
PKTGEN_CONTROL_FILE = "/proc/net/pktgen/pgctrl"

SHORT_ARGS = 'vhb:s:d:t:r'
LONG_ARGS  = ['verbose', 'help', 'burst=', 'size=', 'delay=', 'tries=', 'reverse']

verbosity = 0

LOG_DISABLED = 0
LOG_FATAL = 1
LOG_ERROR = 2
LOG_WARNING = 3
LOG_INFO = 4
LOG_DEBUG = 5

def help():
    print "Command line:"
    print "\t%s [options] [config]" % sys.argv[0]
    print
    print "Options:"
    print "\t-h, --help\t\t Help message"
    print "\t-v, --verbose\t\t Verbosity increase"
    print "\t-b, --burst\t\t Bursting size (default: 100000)"
    print "\t-s, --size\t\t Sending packet size (default: 64B)"
    print "\t-d, --delay\t Packet send delay (default: 0)"
    print "\t-t, --tries\t Bursts count (default: 1)"
    print "\t-r, --reverse\t Reverse measuring direction"
    sys.exit(0)


def die(fmt, *args):
    line = fmt + '\n'
    sys.stderr.write(line % args)
    sys.exit(1)


def debug(fmt, *args):
    if verbosity < LOG_DEBUG:
        return

    line = fmt + '\n'
    sys.stderr.write(line % args)


def info(fmt, *args):
    if verbosity < LOG_INFO:
        return

    line = fmt + '\n'
    sys.stderr.write(line % args)


def error(fmt, *args):
    if verbosity < LOG_ERROR:
        return

    line = fmt + '\n'
    sys.stderr.write(line % args)


def ssh_open(ipaddr, port=22, username="tester", password="tester", timeout=3):
    global strerror

    sshc = paramiko.SSHClient()
    sshc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        sshc.connect(ipaddr, 
                     username=username,
                     password=password, 
                     timeout=timeout)
    except paramiko.BadHostKeyException, e:
        strerror = "Host key error: %s" % e
    except paramiko.AuthenticationException, e:
        strerror = "Authentication error: %s" % e
    except paramiko.SSHException, e:
        strerror = "SSH Error: %s" % e
    except socket.error, e:
        strerror = "Socket error: %s" % e
    else:
        return sshc

    return None


def ssh_close(sshc):
    if sshc == None:
        return
    sshc.close()


def ssh_command(sshc, fmt, *args):
    if sshc == None:
        return

    command = fmt % args
    password = "tester"
    command = "echo -e \"%s\" | sudo -p \"\" -S sh -c '%s'" % (password, command)
    debug("ssh: execute '%s'", command)

    fds = sshc.exec_command(command)
    err = fds[2].read()
    out = fds[1].read()

    debug("ssh stdout len %s: \n%s", len(out), out)
    debug("ssh stderr len %s: \n%s", len(err), err)

    if len(err) > 0:
        return False

    return out


class PacketGen:

    def __init__(self, device, interface):
        self.device = device
        self.ifctrl = PKTGEN_IFACE_FILE_FMT % interface

    def initialize(self, params):

        #if ssh_command(self.device, "modprobe pktgen") == False:
        if ssh_command(ssh_open('172.17.0.1', username='root'), "modprobe pktgen") == False:
            return False

        ssh_command(self.device, "echo stop > %s", PKTGEN_CONTROL_FILE)
        ssh_command(self.device, "echo rem_device_all > %s", PKTGEN_THREAD_FILE)
        ssh_command(self.device, "echo add_device %s > %s", params['dev1-interface'], PKTGEN_THREAD_FILE)

        ssh_command(self.device, "echo clone_skb 0 > %s", self.ifctrl)
        ssh_command(self.device, "echo dst_min 0.0.0.0 > %s", self.ifctrl)
        ssh_command(self.device, "echo dst_max 0.0.0.0 > %s", self.ifctrl)
        ssh_command(self.device, "echo src_min 0.0.0.0 > %s", self.ifctrl)
        ssh_command(self.device, "echo src_max 0.0.0.0 > %s", self.ifctrl)

        ssh_command(self.device, "echo min_pkt_size %s > %s", params['packet-size'], self.ifctrl)
        ssh_command(self.device, "echo max_pkt_size %s > %s", params['packet-size'], self.ifctrl)
        ssh_command(self.device, "echo count %s > %s", params['count'], self.ifctrl)
        ssh_command(self.device, "echo delay %s > %s", params['send-delay'], self.ifctrl)

        ssh_command(self.device, "echo dst_mac %s > %s", params['target-mac'], self.ifctrl)

        return True

    def finalize(self):
        if ssh_command(self.device, "rmmod pktgen") == False:
            return False

        return True

    def run(self):
        ssh_command(self.device, "echo start > %s", PKTGEN_CONTROL_FILE)

    def get_runtime(self):
        rv = ssh_command(self.device, "cat %s", self.ifctrl)
        if not rv:
            error("Cannot cat pktgen results")
            return None

        match = None
        for line in rv.split('\n'):
            match = re.match("^Result: OK: (\d+).*$", line)
            if match:
                break
                             
        if not match:
            error("Failed to get TX runtime")
            return None

        v = string.atoi(match.group(1))
        return v

    def set_delay(self, delay):
        debug("adusting delay: %u", delay)
        ssh_command(self.device, "echo delay %s > %s", delay, self.ifctrl)

def get_rx_counters(sshc, ifname):
    rv = ssh_command(sshc, "ip -s link show dev %s", ifname)
    if not rv:
        error("Failed to receive rx counters from '%s'", ifname)
        return None

    lines = rv.split('\n')
    while True:

        if len(lines) == 0:
            break
        line = lines[0].strip()
        del lines[0]
        if line.startswith('RX'):
            break

    line = lines[0]

    match = re.match("^\s+(\d+)\s+(\d+).*$", line)
    if not match:
        return None

    v1 = string.atoi(match.group(1))
    v2 = string.atoi(match.group(2))

    return v1, v2


def get_mac_address(sshc, ifname):
    rv = ssh_command(sshc, "ip link show dev %s", ifname)
    if not rv:
        error("Failed to receive mac from '%s'", ifname)
        return None

    mac = None
    lines = rv.split('\n')
    for line in lines:

        match = re.match("^\s+link/ether\s+([0-9A-Fa-f\:]+).*$", line)
        if not match:
            continue

        mac = match.group(1)
        break

    return mac


def measure(pktgen, dev1_ssh, dev2_ssh, params):
    dev2_interface = params['dev2-interface']
    packets_count = params['count']
    
    rx1 = get_rx_counters(dev2_ssh, dev2_interface)
    if rx1 == None:
        return None
    
    rv = pktgen.run()

    rx2 = get_rx_counters(dev2_ssh, dev2_interface)
    if rx2 == None:
        return None

    duration = pktgen.get_runtime()

    delta_bytes = rx2[0] - rx1[0]
    delta_packets = rx2[1] - rx1[1]

    debug("delta bytes: %u", delta_bytes)
    debug("delta packets: %u", delta_packets)
    debug("duration: %u us", duration)

    loss = (packets_count - delta_packets) / (1.0 * packets_count)
    bps = delta_bytes / (duration / 1000000.0)
    pps = delta_packets / (duration / 1000000.0)
    
    return bps, pps, loss


if __name__ == '__main__':
    reverse = False
    params = dict()
    config_file = None
    params['count'] = 100000
    params['packet-size'] = 64
    params['send-delay'] = 0
    params['tries'] = 1

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], SHORT_ARGS, LONG_ARGS)
    except getopt.GetoptError, err:
        help()

    for o, a in opts:
        if o in ('-h', '--help'):
            help()

        elif o in ('-v', '--verbose'):
            verbosity += 1

        elif o in ('-b', '--burst'):
            params['count'] = string.atoi(a)

        elif o in ('-s', '--size'):
            params['packet-size'] = string.atoi(a)

        elif o in ('-d', '--delay'):
            params['send-delay'] = string.atoi(a)

        elif o in ('-t', '--tries'):
            params['tries'] = string.atoi(a)

        elif o in ('-r', '--reverse'):
            reverse = True

    if len(args) > 0:
        config_file = args[0]

    if config_file == None:
        config_file = 'link.cfg'

    if not os.path.isfile(config_file):
        die("configuration file '%s' not foung", config_file)

    config = ConfigParser()
    config.readfp(open(config_file))

    params['dev1-interface'] = config.get("master", "target-interface")
    params['dev2-interface'] = config.get("slave", "target-interface")
    params['dev1-ipaddr'] = config.get("master", "connect-ipaddr")
    params['dev2-ipaddr'] = config.get("slave", "connect-ipaddr")

    if reverse:
        tmp_ip = params['dev1-ipaddr']
        tmp_ifname = params['dev1-interface']
        params['dev1-ipaddr'] = params['dev2-ipaddr']
        params['dev1-interface'] = params['dev2-interface']
        params['dev2-ipaddr'] = tmp_ip
        params['dev2-interface'] = tmp_ifname

    dev1_ip = params['dev1-ipaddr']
    dev2_ip = params['dev2-ipaddr']
    dev1_iface = params['dev1-interface']
    dev2_iface = params['dev2-interface']

    info("SSH connect to %s", dev1_ip)
    dev1_ssh = ssh_open(dev1_ip)
    if dev1_ssh == None:
        die("connect to %s failed", dev1_ip)

    info("SSH connect to %s", dev2_ip)
    dev2_ssh = ssh_open(dev2_ip)
    if dev2_ssh == None:
        ssh_close(dev1_ssh)
        die("connect to %s failed", dev2_ip)

    remote_mac = get_mac_address(dev2_ssh, dev2_iface)
    if remote_mac == None:
        ssh_close(dev1_ssh)
        ssh_close(dev2_ssh)
        die("Failed to get remote mac")

    params['target-mac'] = remote_mac

    pktgen = PacketGen(dev1_ssh, dev1_iface)

    info("Initializing pktgen")
    if not pktgen.initialize(params):
        ssh_close(dev1_ssh)
        ssh_close(dev2_ssh)
        die("pktgen init failed")

    result = None

    info("starting measurements")
    counter = 0
    while True:
        rv = measure(pktgen, dev1_ssh, dev2_ssh, params)
        if not rv:
            error("No result?")
            break

        bps, pps, loss = rv
        #print "BPS: %u; PPS: %u; LOSS: %.4f; delay: %u" % (bps, pps, loss, params['send-delay'])
        print "%uMbps; %ukPPS; LOSS: %.4f; delay: %u" % (round(float((bps*8)/2**20),1), round(float(pps)/1000, 1), loss, params['send-delay'])

        counter += 1
        if counter >= params['tries']:
            break

    if not pktgen.finalize():
        error("pktgen finalize failed")

    ssh_close(dev1_ssh)
    ssh_close(dev2_ssh)

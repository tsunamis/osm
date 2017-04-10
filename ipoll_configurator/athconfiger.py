#!/usr/bin/env python

import json
import sys
import paramiko

class Configer:
    def __init__(self, change_function):
        self.changes = change_function

    def die(self):
        sys.exit()

    def open_json(self, cfg_file):
        try:
            cfg = json.load(cfg_file)
        except:
            return False
        return cfg

    def save_json(self, cfg, cfg_file):
        try:
            json.dump(cfg, cfg_file, indent=3)
        except:
            return False
        return True

    def connect(self, ip, port, usr, psw):
        try:
            con = paramiko.SSHClient()
            con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            con.connect(ip, port, usr, psw)
        except:
            return False
        return con

    def disconnect(self, con):
        con.close()

    def update_keys(self, cfg):
        try:
            updated = self.changes(cfg)
        except KeyError:
            print("Invalid keys")
            self.die()
        return updated

    def save_and_reboot(self, con):
        con.exec_command("sysconf -w; reboot")

    def open_config(self, con):
        try:
            sftp = con.open_sftp()
            f = sftp.file('/tmp/config.json', 'r+')
        except IOError:
            print("Invalid config file. Connecting to wrong device?")
            self.die()
        return f

    def configure(self, ip, port, usr, psw, save=False):
        c = self.connect(ip, port, usr, psw)
        if not c:
            return False
        f = self.open_config(c)
        cfg = self.open_json(f)
        if cfg:
            updated = self.update_keys(cfg)
        else:
            f.close()
            self.disconnect(c)
            return False
        f.seek(0)
        if self.save_json(updated, f):
            f.truncate(f.tell())
            f.close()
            if save:
                self.save_and_reboot(c)
            self.disconnect(c)
            return True
        else:
            f.close()
            self.disconnect(c)
            return False

if __name__ == '__main__':

    def CHANGE_FUNCTION(CFG):
        """ DEFINE CONFIG CHANGES HERE 

        HOW TO:
            CFG['X']['Y']['Z'] = NEW_VALUE

        """
        # -------------------------------------------------------------------
        CFG['wireless']['radio'][0]['vap'][0]['rts']['enabled'] = "true"
	#CFG['wireless']['radio'][0]['vap'][0]['ssid'] = "ipoll_64"
        # -------------------------------------------------------------------
        return CFG

    port = 22
    username = 'admin'
    password = 'admin01'

    # DEFINE IP RANGE HERE
    # FORMAT:
    # 10.<min_1>.<min_2>.101 -- 10.<max_1>.<max_2>.101
    min_1 = 1
    max_1 = 8
    min_2 = 1
    max_2 = 8

    # IGNORE THESE IPs:
    ignore = ['10.5.8.101']
    
    # create device IP list
    ip_range = sum([['10.'+str(x)+'.'+str(y)+'.101' for y in range(min_2,max_2+1,1)] for x in range(min_1,max_1+1,1)], [])

    # remove ignored IPs from list
    [ip_range.remove(ign) for ign in ignore if ign in ip_range]

    configer = Configer(CHANGE_FUNCTION)

    for ip in ip_range:
        if configer.configure(ip, port, username, password):
            print("Configured: " + ip)
        else:
            print("Configuration failed: " + ip)

    print("Finished")

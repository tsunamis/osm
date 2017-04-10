#!/usr/bin/env python

import json
import sys
from wxee2 import wxee

class Configer_wxee:
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

    def connect(self, ip, port):
        try:
            con = wxee(devtype="qualcomm")
            self.socket = con.wx_socket(ip, port) 
        except:
            return False
        return con

    def disconnect(self, con):
        con.wx_close(self.socket)

    def update_keys(self, cfg):
        try:
            updated = self.changes(cfg)
        except KeyError:
            print("Invalid keys")
            self.die()
        return updated

    def save_and_reboot(self, con):
        con.wcmd_legacy(self.socket, "sysconf -w; reboot")

    def open_config(self, con, ip):
        try:
            con.wcmd_legacy(self.socket, "sysconf --read config /tmp/config.json")
            con.wcmd_get(self.socket, '/tmp/config.json', '/tmp/tmpfile'+ip)
            f = open('/tmp/tmpfile', 'r+')
        except IOError:
            print("Invalid config file. Connecting to wrong device?")
            self.die()
        return f

    def configure(self, ip, port, con):
        c = self.connect(ip, port)
        if not c:
            return False
        f = self.open_config(c, ip)
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
            con.wcmd_put(self.socket, '/tmp/config.json', '/tmp/tmpfile'+ip)
            self.save_and_reboot(c)
            self.disconnect(c)
            return True
        else:
            f.close()
            self.disconnect(c)
            return False


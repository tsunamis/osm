import paramiko
import time
import json
import scp
import sys

class connection:

    def __init__(self, ip, username, password, port, lan):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        self.lan = lan
        self.con = None
        print "Connection"

    def make_con(self):
        print "%s %s %s %s" % (self.ip, self.port, self.username, self.password)
        i = 0
        while True:
            try:
                self.con = paramiko.SSHClient()
                self.con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.con.connect(self.ip, port = self.port, username = self.username, password = self.password)
                break

            except:
                i += 1
                time.sleep(2)
            if i == 30:
                print "Pasiduodu"
                sys.exit(1)

    def close_con(self):
        self.con.close()

    def open_con(self):
        self.make_con()

    def execute(self, command):
        stdin, stdout, stderr = self.con.exec_command(str(command))
        output = stdout.readlines()
        error = stderr.readlines()
        print ">>>> execute >>>> %s %s" % (output, error)
        return output, error

    def read_file_to_json(self, f):
        sftp = self.con.open_sftp()
        ff = sftp.file(f, 'r')
        cfg = json.load(ff)
        ff.close()
        return cfg

    def write_to_json(self, f, j):
        sftp = self.con.open_sftp()
        ff = sftp.file(f, 'w')
        json.dump(j, ff, indent=4)
        ff.close()

    def open_sftp(self, source, destination):
        pipe = scp.SCPClient(self.con.get_transport())
        pipe.put(source, destination) 

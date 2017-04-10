#!/usr/bin/python

from select import select
from socket import *
from struct import pack
from log import factory

import logging
import time
import os
import sys
import fdpexpect

log = factory("WXEE")
log.setLevel(logging.DEBUG)

class wxee:
    endian="<" #this means little endian

    attr_any                    = 0
    attr_enabled                = 1
    attr_firmware_id            = 2  # string, "FWBD-0200"
    attr_chipset_name           = 3  # string , "RT3052"
    attr_pcb_rev                = 4  # char*,  "0005"
    attr_pcb_prddate            = 5  # time_t, seconds
    attr_pcb_name               = 6  # string,  "FWBD-0120" */
    
    def __init__(self, devtype="ralink"):
        if devtype == "ralink":
            self.attr_tx_calpoints_2ghz      = 7  # Radio TX power calibration points
            self.attr_tx_calpoints_5ghz      = 8
            self.attr_rx_calpoints_2ghz      = 9  # Radio RX signal level measurement calibration points
            self.attr_rx_calpoints_5ghz      = 10
            self.attr_11bg_txpower_delta     = 11 # 11b-11g TX power delta
            self.attr_leds                   = 12 # struct ee_led, array
            self.attr_shiftreg               = 13 # struct ee_shiftreg, array
            self.attr_buttons                = 14 # struct ee_button, array
            self.attr_ethernet               = 15 # struct ee_ethernet*, array
            self.attr_poerelay               = 16 # struct ee_poerelay*, array

            self.attr_atas_enabled           = 17
            self.attr_atas_address           = 18
            self.attr_atas_gateway           = 19
            self.attr_atas_port              = 20

            self.attr_atas_reserved1         = 21
            self.attr_atas_reserved2         = 22
            self.attr_atas_reserved3         = 23
            self.attr_atas_reserved4         = 24

            self.attr_pcb_prlocation         = 25

            self.attr_tx_calpoints_2ghz_3x   = 26
            self.attr_tx_calpoints_5ghz_3x   = 27
            self.attr_rx_calpoints_2ghz_3x   = 28
            self.attr_rx_calpoints_5ghz_3x   = 29
            self.attr_serial_number          = 30
            self.attr_max_vaps               = 31
            self.attr_calibration_mode       = 32

        elif devtype == "qualcomm":
            self.endian=">" #this means big endian

            self.attr_leds                   = 7  # struct ee_led, array
            self.attr_shiftreg               = 8  # struct ee_shiftreg, array
            self.attr_buttons                = 9  # struct ee_button, array
            self.attr_poerelay               = 10 # struct ee_poerelay*, array

            self.attr_atas_enabled           = 11
            self.attr_atas_address           = 12
            self.attr_atas_gateway           = 13
            self.attr_atas_port              = 14

            self.attr_atas_reserved1         = 15
            self.attr_atas_reserved2         = 16
            self.attr_atas_reserved3         = 17
            self.attr_atas_reserved4         = 18
                
            self.attr_pcb_prlocation         = 19
                    
            self.attr_serial_number          = 20
            self.attr_calibration_mode       = 21
            self.attr_pcba_calibrated        = 22
            self.attr_post_production        = 23

    def set_endian(self, endian):
        self.endian = endian

    def endian_pack(self, fmt, *args):
        return pack(self.endian+fmt, *args)
        

    def die(self, s):
        log.error(s)
        sys.exit(1)

    def __wx_socket(self, host, port):
        while True:
            s = None

            try:
                s = create_connection((host, port), 2)
                s.settimeout(0)
            except timeout, msg:
                log.debug('can\'t connect to %s on port %s, %s', host, port, msg)
                continue
            except error, msg:
                log.debug('can\'t connect to %s on port %s, %s', host, port, msg.strerror)
                time.sleep(2)
                continue

            return s

    def wx_socket(self, host, port):
        s = self.__wx_socket(host, port)
        log.debug("connected to %s on port %s", host, port)
        s.settimeout(0)
        return s

    def wx_close(self, s):
        s.close()
        s = None

    def wx_expect_open(self, s, logon=True):
        child = fdpexpect.fdspawn(s.fileno())
        if child == None:
            self.die('could not create expect child')

        if logon:
            child.logfile = sys.stdout

        child.maxread = 5000
        child.timeout = 10
        log.debug("expect child created")

        return child

    def wx_expect_close(self, child):
        child.close()
        child = None
        log.debug('expect child closed')

    def __wx_recv(self, s, size = 8192):
        odata = ''
        s.setblocking(0)
        while True:
            ifd, ofd, xfd = select([s.fileno()], [], [], 0.100)
            if s.fileno() in ifd:
                idata = s.recv(size)
                if len(idata) == 0:
                    break
                odata += idata
                if str(odata).endswith('$END'):
                    odata = odata[0:-4]
                    break

        s.setblocking(1)
        return odata

    def wx_recv(self, s, size = 8192):
        try:
            s.setblocking(0)
            return self.__wx_recv(s, size)
        except error, msg:
            log.error('socket error: %s\n', msg)
            return ''
        finally:
            s.setblocking(1)


    def __wx_send(self, s, data):
        nleft = len(data)
        noff  = 0
        s.setblocking(1)

        while nleft > 0:
            ifd, ofd, xfd = select([], [s.fileno()], [], 0.100)
            if s.fileno() in ofd:
                nsent = s.send(data[noff:])

                if nsent > 0:
                    nleft -= nsent
                    noff  += nsent
                elif nsent < 0:
                    log.error('send failed?')
                    break
                elif nsent == 0:
                    log.debug('send EOF?')
                    break;
            else:
                log.debug('timeout.')

        s.setblocking(0)
        if nleft > 0:
            self.die("too few bytes sent %d/%d.", nleft, len(data))

        return nsent

    def wx_send(self, s, data):
        try:
            s.setblocking(0)
            return self.__wx_send(s, data)
        except error, msg:
            log.error('socket error: %s\n', msg)
            return ''
        finally:
            s.setblocking(1)

    def wcmd_send(self, s, command):
        nsend = 4 + len(command)
        data = self.endian_pack('4sI', 'WCMD', len(command))
        self.wx_send(s, data)
        self.wx_send(s, command)
        nrecv = len(self.wx_recv(s))

        log.debug('sending \'%s\' = %d/%d', command, nsend, nrecv)

    def wcmd_get(self, s, remote, local):
        hlen = 64
        data = self.endian_pack('4sI', 'WGET', hlen)
        self.wx_send(s, data)

        data = self.endian_pack('64s', remote)
        self.wx_send(s, data)

        data = self.wx_recv(s)
        if len(data) > 0:
            fd = os.open(local, os.O_WRONLY|os.O_CREAT|os.O_TRUNC)
            os.write(fd, data)
            os.close(fd)

        log.debug("'%s' saved as '%s'", remote, local)
        return len(data)

    """
        WPUT
        {header length}
        {file name}
        {file size}
        {file data}

        name   - file name, upto 64 bytes length
        length - file content length 4bytes
        data   - file data
    """
    def wcmd_put(self, s, remote, local):
        try:
            fs = os.stat(local)
        except OSError, e:
            log.error(e)
            return

        hlen = 64 + 4
        data = self.endian_pack('4sI', 'WPUT', hlen)
        self.wx_send(s, data)

        data = self.endian_pack('64sI', remote, fs.st_size)
        self.wx_send(s, data)

        try:
            # XXX: Must specify O_BINARY on windows, otherwise reading will be
            # finished on first occurance of '\0'. Linux has no such key thus
            # try-catch block required.
            fd = os.open(local, os.O_RDONLY | os.O_BINARY)
        except AttributeError, e:         # no attribute 'O_BINARY'
            fd = os.open(local, os.O_RDONLY)

        nbytes = 0
        while True:
            data = os.read(fd, 128*1024)
            if len(data) == 0:
                break

            nsent = self.wx_send(s, data)
            if nsent > 0:
                nbytes += nsent
            elif nsent == 0:
                log.debug('EOF ?')
                break
            elif nsent < 0:
                log.error('send')
                break

        os.close(fd)
        self.wx_recv(s)
        return nbytes

    def wxee_send(self, s, atype, adata):
        nsend = 4 + len(adata)
        data = self.endian_pack('4sHH', 'WXEE', nsend, atype)
        self.wx_send(s, data)
        self.wx_send(s, adata)
        nrecv = len(self.wx_recv(s))

        log.debug('sending ATTR(%d,%d) = %d/%d', atype, len(adata), nsend, nrecv)

    def wxda_send(self, s, atype):
        data = self.endian_pack('4sHH', 'WXDA', atype, 0)
        self.wx_send(s, data)
        nrecv = len(self.wx_recv(s))
        log.debug('delete ATTR(%d) %d', atype, nrecv)

    def wxfa_send(self, s, atype):
        data = self.endian_pack('4sHH', 'WXFA', atype, 0)
        self.wx_send(s, data)
        attr = self.wx_recv(s)
        nrecv = len(attr)
        log.debug('wxfa ATTR(%d) %d', atype, nrecv)
        return attr


    def wcmd_legacy(self, s, command):
        nsend = len(command)
        self.wx_send(s, command)
        data = self.wx_recv(s, 8192)
        nrecv = len(data)
        log.debug('sending \'%s\' = %d/%d', command, nsend, nrecv)
        return data

    def wcmd_legacy_expect(self, s, child, command, expect, timeout=5):
        nsend = len(command)
        self.wx_send(s, command)
        status = child.expect(expect, timeout)
        log.debug('sending \'%s\' = %d', command, status)
        return status

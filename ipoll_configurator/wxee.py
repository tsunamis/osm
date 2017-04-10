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

WXEE_ANY                = 0
WXEE_ENABLED            = 1
WXEE_FIRMWARE_ID        = 2  # string, "FWBD-0200"
WXEE_CHIPSET_NAME       = 3  # string , "RT3052"
WXEE_PCB_REV            = 4  # char*,  "0005"
WXEE_PCB_PRDDATE        = 5  # time_t, seconds
WXEE_PCB_NAME           = 6  # string,  "FWBD-0120" */
WXEE_TX_CALPOINTS_2GHZ  = 7  # Radio TX power calibration points
WXEE_TX_CALPOINTS_5GHZ  = 8
WXEE_RX_CALPOINTS_2GHZ  = 9  # Radio RX signal level measurement calibration points
WXEE_RX_CALPOINTS_5GHZ  = 10
WXEE_11BG_TXPOWER_DELTA = 11 # 11b-11g TX power delta
WXEE_LEDS               = 12 # struct ee_led, array
WXEE_SHIFTREG           = 13 # struct ee_shiftreg, array
WXEE_BUTTONS            = 14 # struct ee_button, array
WXEE_ETHERNET           = 15 # struct ee_ethernet*, array
WXEE_POERELAY           = 16 # struct ee_poerelay*, array

WXEE_ATAS_ENABLED       = 17
WXEE_ATAS_ADDRESS       = 18
WXEE_ATAS_GATEWAY       = 19
WXEE_ATAS_PORT          = 20

WXEE_ATAS_RESERVED1     = 21
WXEE_ATAS_RESERVED2     = 22
WXEE_ATAS_RESERVED3     = 23
WXEE_ATAS_RESERVED4     = 24

WXEE_PCB_PRLOCATION     = 25

WXEE_TX_CALPOINTS_2GHZ_3X   = 26
WXEE_TX_CALPOINTS_5GHZ_3X   = 27
WXEE_RX_CALPOINTS_2GHZ_3X   = 28
WXEE_RX_CALPOINTS_5GHZ_3X   = 29
WXEE_SERIAL_NUMBER      = 30
WXEE_MAX_VAPS           = 31
WXEE_CALIBRATION_MODE   = 32

log = factory("WXEE")
log.setLevel(logging.DEBUG)

def die(s):
    log.error(s)
    sys.exit(1)

def __wx_socket(host, port):
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

def wx_socket(host, port):
    s = __wx_socket(host, port)
    log.debug("connected to %s on port %s", host, port)
    s.settimeout(0)
    return s

def wx_close(s):
    s.close()
    s = None

def wx_expect_open(s, logon=True):
    child = fdpexpect.fdspawn(s.fileno())
    if child == None:
        die('could not create expect child')

    if logon:
        child.logfile = sys.stdout

    child.maxread = 5000
    child.timeout = 10
    log.debug("expect child created")

    return child

def wx_expect_close(child):
    child.close()
    child = None
    log.debug('expect child closed')

def __wx_recv(s, size = 8192):
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

def wx_recv(s, size = 8192):
    try:
        s.setblocking(0)
        return __wx_recv(s, size)
    except error, msg:
        log.error('socket error: %s\n', msg)
        return ''
    finally:
        s.setblocking(1)


def __wx_send(s, data):
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
        die("too few bytes sent %d/%d.", nleft, len(data))

    return nsent

def wx_send(s, data):
    try:
        s.setblocking(0)
        return __wx_send(s, data)
    except error, msg:
        log.error('socket error: %s\n', msg)
        return ''
    finally:
        s.setblocking(1)

def wcmd_send(s, command):
    nsend = 4 + len(command)
    data = pack('4sI', 'WCMD', len(command))
    wx_send(s, data)
    wx_send(s, command)
    nrecv = len(wx_recv(s))

    log.debug('sending \'%s\' = %d/%d', command, nsend, nrecv)

def wcmd_get(s, remote, local):
    hlen = 64
    data = pack('4sI', 'WGET', hlen)
    wx_send(s, data)

    data = pack('64s', remote)
    wx_send(s, data)

    data = wx_recv(s)
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
def wcmd_put(s, remote, local):
    try:
        fs = os.stat(local)
    except OSError, e:
        log.error(e)
        return

    hlen = 64 + 4
    data = pack('4sI', 'WPUT', hlen)
    wx_send(s, data)

    data = pack('64sI', remote, fs.st_size)
    wx_send(s, data)

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

        nsent = wx_send(s, data)
        if nsent > 0:
            nbytes += nsent
        elif nsent == 0:
            log.debug('EOF ?')
            break
        elif nsent < 0:
            log.error('send')
            break

    os.close(fd)
    wx_recv(s)
    return nbytes

def wxee_send(s, atype, adata):
    nsend = 4 + len(adata)
    data = pack('4sHH', 'WXEE', nsend, atype)
    wx_send(s, data)
    wx_send(s, adata)
    nrecv = len(wx_recv(s))

    log.debug('sending ATTR(%d,%d) = %d/%d', atype, len(adata), nsend, nrecv)

def wxda_send(s, atype):
    data = pack('4sHH', 'WXDA', atype, 0)
    wx_send(s, data)
    nrecv = len(wx_recv(s))
    log.debug('delete ATTR(%d) %d', atype, nrecv)

def wxfa_send(s, atype):
    data = pack('4sHH', 'WXFA', atype, 0)
    wx_send(s, data)
    attr = wx_recv(s)
    nrecv = len(attr)
    log.debug('wxfa ATTR(%d) %d', atype, nrecv)
    return attr


def wcmd_legacy(s, command):
    nsend = len(command)
    wx_send(s, command)
    data = wx_recv(s, 8192)
    nrecv = len(data)
    log.debug('sending \'%s\' = %d/%d', command, nsend, nrecv)
    return data

def wcmd_legacy_expect(s, child, command, expect, timeout=5):
    nsend = len(command)
    wx_send(s, command)
    status = child.expect(expect, timeout)
    log.debug('sending \'%s\' = %d', command, status)
    return status

import logging
import sys

def factory(logid=None):
    log  = logging.getLogger(logid)

    hdlr = logging.StreamHandler(sys.stderr)
    fmtr = logging.Formatter('%(asctime)s - %(message)s')
    hdlr.setFormatter(fmtr)

    log.addHandler(hdlr)
    log.setLevel(logging.DEBUG);

    return log

#!/bin/bash

wget "http://buildd3.wilibox.com/download.php?branch=master&firmware=APCPE.QA-2&file=latest.img" -O /tmp/latest.img
#wget "http://buildd3.wilibox.com/download.php?branch=DLB/v7.53&firmware=APCPE.QA-2&file=APCPE.QA-2.v7.53.20512.img" -O /tmp/latest.img
case $1 in
wxee)
python fwupdate_ac_wxee.py
;;
normal)
python fwupdate_ac.py
;;
esac
strings /tmp/latest.img | grep -i apcpe

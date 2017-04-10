#!/bin/bash


#wget "http://buildd3.wilibox.com/download.php?branch=master&firmware=APCPE.QM-1&file=latest.img" -O /tmp/latest.img
wget "http://buildd3.wilibox.com/download.php?branch=DLB/v7.53&firmware=APCPE.QM-1&file=latest.img" -O /tmp/latest.img

case $1 in

normal)
python fwupdate_n.py
;;
wxee)
python fwupdate_n_wxee.py
;;
esac
strings /tmp/latest.img | grep -i apcpe

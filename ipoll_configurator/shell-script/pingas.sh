#!/bin/sh

for i in $(seq 1 1 8)
        do
        for j in $(seq 1 1 8)
                do
                        #echo "${i}${j} ->"  $(ping -A -i 0.01 -c 256000 -s 1400  192.168.199.$i$j | grep -i -B 1 "min/avg/max/mdev") &
                        ping 10.$i.$j.26 &
                done
        done

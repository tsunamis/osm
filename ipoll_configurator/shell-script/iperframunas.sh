#!/bin/sh -x

for i in $(seq 1 1 8)
        do   
        for j in $(seq 1 1 8) 
                 do
                        iperf -c 10.${i}.${j}.26 -u -t 100 -p $((50${i}0+${j})) -d -y C >> output.txt& 
                 done 
        done

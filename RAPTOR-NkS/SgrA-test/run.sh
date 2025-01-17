#!/bin/bash
for ((i=234;i<=285;i=i+1))
do
	python3 plot.py  $i
done

# convert -delay 10 -loop 0 *.png ani-1k.gif

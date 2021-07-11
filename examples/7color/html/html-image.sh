#!/bin/bash
./clear.py &
CWD=`pwd`
filename=$1
line1=$2
line2=$3
topRight=$4
image=$5
cp $CWD/$filename $CWD/$filename.copy

awk -v replacement="$line1" '{sub("{line1}",replacement, $0); print }' $CWD/$filename.copy > $CWD/$filename.copy.replaced && mv -f $CWD/$filename.copy.replaced $CWD/$filename.copy
awk -v replacement="$line2" '{sub("{line2}",replacement, $0); print }' $CWD/$filename.copy > $CWD/$filename.copy.replaced && mv -f $CWD/$filename.copy.replaced $CWD/$filename.copy
awk -v replacement="$topRight" '{sub("{topRight}",replacement, $0); print }' $CWD/$filename.copy > $CWD/$filename.copy.replaced && mv -f $CWD/$filename.copy.replaced $CWD/$filename.copy
awk -v replacement="$image" '{sub("{image}",replacement, $0); print }' $CWD/$filename.copy > $CWD/$filename.copy.replaced && mv -f $CWD/$filename.copy.replaced $CWD/$filename.copy

firefox --headless --screenshot --window-size=600,448 file://$CWD/$filename.copy
echo Waiting for clear..
wait
echo Updating now..
./image.py screenshot.png
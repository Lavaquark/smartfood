#!/bin/sh
sudo bluetoothctl
power on
scan on
scan off
connect C5:AC:9A:2E:1C:DF
exit
sudo nuimoctl --discover
sudo nuimoctl --connect C5:AC:9A:2E:1C:DF

python3 raspberrypicode.py
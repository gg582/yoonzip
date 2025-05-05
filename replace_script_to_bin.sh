#!/bin/bash
pip3 install nuitka
python3 -m nuitka --standalone --onefile yoonzip.py 
rm -rf /usr/bin/yoonzip
rm -rf /usr/bin/yoonzip.py
cp yoonzip.bin /usr/bin/yoonzip

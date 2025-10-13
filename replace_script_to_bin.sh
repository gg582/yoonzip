#!/bin/bash
pip3 install nuitka
python3 -m nuitka --standalone --onefile yoonzip.py\
  --include-package=pyzipper
rm -rf /usr/bin/yoonzip
rm -rf /usr/bin/yoonzip.py
pkexec cp yoonzip.bin /usr/bin/yoonzip

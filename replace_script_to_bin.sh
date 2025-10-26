#!/bin/bash
set -e

pip3 install nuitka pyzipper

python3 -m nuitka \
  --standalone \
  --onefile \
  --include-package=pyzipper \
  --include-module=gi \
  yoonzip.py

sudo rm -f /usr/bin/yoonzip /usr/bin/yoonzip.py
sudo cp yoonzip.bin /usr/bin/yoonzip


#!/bin/bash

sudo cp yoonzip.desktop /usr/share/applications

sudo cp yoonzip.py /usr/bin/

sudo ln -s /usr/bin/yoonzip.py /usr/bin/yoonzip

sudo update-mime-database /usr/share/mime

#!/bin/bash

cp yoonzip.desktop /usr/share/applications

cp yoonzip.py /usr/bin/

ln -s /usr/bin/yoonzip.py /usr/bin/yoonzip

update-mime-database /usr/share/mime

#!/bin/bash

pkexec cp yoonzip.desktop /usr/share/applications
pkexec
pkexec cp yoonzip.py /usr/bin/
pkexec
pkexec ln -s /usr/bin/yoonzip.py /usr/bin/yoonzip
pkexec
pkexec update-mime-database /usr/share/mime

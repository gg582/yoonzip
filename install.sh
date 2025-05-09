#!/bin/bash

sudo cp korzip.desktop /usr/share/applications

sudo cp korzip.py /usr/bin/

sudo ln -s /usr/bin/korzip.py /usr/bin/korzip

sudo update-mime-database /usr/share/mime

#!/bin/bash
set -e

pip3 install nuitka pyzipper

python3 -m nuitka \
  --standalone \
  --onefile \
  --include-package=pyzipper \
  --include-module=gi \
  --include-module=gi.repository.GLib \
  --include-module=gi.repository.GObject \
  --include-module=gi.repository.Gio \
  --include-module=gi.repository.GdkPixbuf \
  --include-module=gi.repository.Gtk \
  --include-module=gi.repository.Cairo \
  yoonzip.py

sudo rm -f /usr/bin/yoonzip /usr/bin/yoonzip.py
sudo cp yoonzip.bin /usr/bin/yoonzip


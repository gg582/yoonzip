#!/usr/bin/python3
from importlib import reload
import sys
reload(sys)
import gi
import zipfile
gi.require_version("Gtk","3.0")
from gi.repository import Gtk
ii=0
def unzip(file,path):
	with zipfile.ZipFile(file,'r') as z:
		zipinfo=z.infolist()
		for member in zipinfo:
			member.filename=member.filename.encode('cp437').decode('euc-kr','ignore')
			z.extract(member,path)
def altunzip(file,path):
	with zipfile.ZipFile(file,'r') as z:
		zipinfo=z.infolist()
		for member in zipinfo:
			z.extract(member,path)
if sys.argv[1]=="--gui":
	dialog=Gtk.FileChooserDialog("압축을 풀 폴더 선택",None,Gtk.FileChooserAction.SELECT_FOLDER,(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,"Select",Gtk.ResponseType.OK))
	dialog.set_default_size(800,400)
	response=dialog.run()
	if response == Gtk.ResponseType.OK:
		print("OK")
		folder=dialog.get_current_folder()
		dialog.destroy()
	elif response == Gtk.ResponseType.CANCEL:
		print("Cancelled")
		dialog.destroy()
	dialog0=Gtk.FileChooserDialog("ZIP 파일 선택",None,Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN,Gtk.ResponseType.OK))
	dialog0.set_default_size(800,400)
	file_filter=Gtk.FileFilter()
	file_filter.set_name("ZIP Files")
	file_filter.add_mime_type("application/zip")
	dialog0.add_filter(file_filter)
	response0=dialog0.run()
	if response0== Gtk.ResponseType.OK:
		print("OK")
		filename=dialog.get_filename()
		dialog0.destroy()
	elif response0==Gtk.ResponseType.CANCEL:
		print("Cancelled")
		dialog0.destroy()
		sys.exit()
	if response0==Gtk.ResponseType.OK:
		try:
			unzip(filename,folder)
			sys.exit()
		except UnicodeEncodeError:
			print('not cp949')
			altunzip(filename,folder)
			sys.exit()
	Gtk.main()
else:
	try:
		unzip(sys.argv[1],sys.argv[2])
	except BaseException:
			altunzip(sys.argv[1],sys.argv[2])

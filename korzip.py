#!/usr/bin/python3
import sys
import zipfile
import os
import gi
from importlib import reload
from multiprocessing import Pool
from datetime import datetime

reload(sys)
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def _unzip_single(file_path, extract_path):
    """내부 함수: 단일 ZIP 파일 압축 해제 시도"""
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            for member in zf.infolist():
                try:
                    member.filename = member.filename.encode('cp437').decode('euc-kr', 'ignore')
                    zf.extract(member, extract_path)
                except UnicodeDecodeError:
                    try:
                        member.filename = member.filename.encode('cp437').decode('utf-8', 'ignore')
                        zf.extract(member, extract_path)
                    except UnicodeDecodeError:
                        print(f"경고: '{member.filename}' 파일명 디코딩 실패. 건너뜁니다.")
                except Exception as e:
                    print(f"경고: '{member.filename}' 압축 해제 중 오류 발생: {e}")
    except zipfile.BadZipFile:
        print(f"오류: '{file_path}'은 올바른 ZIP 파일이 아닙니다.")
    except FileNotFoundError:
        print(f"오류: '{file_path}' 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"오류: '{file_path}' 압축 해제 중 예기치 않은 오류 발생: {e}")

def unzip_multiple(file_paths, extract_path, use_multiprocessing=True):
    """여러 ZIP 파일 압축 해제"""
    if use_multiprocessing and len(file_paths) > 1:
        with Pool() as pool:
            tasks = [(file, extract_path) for file in file_paths]
            pool.starmap(_unzip_single, tasks)
    else:
        for file_path in file_paths:
            _unzip_single(file_path, extract_path)

def _zip_single(file_paths, zip_file_path):
    """내부 함수: 여러 파일을 하나의 ZIP 파일로 압축"""
    try:
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in file_paths:
                base_name = os.path.basename(file_path)
                zf.write(file_path, base_name)
        print(f"'{zip_file_path}'으로 압축 완료.")
    except FileNotFoundError:
        print(f"오류: '{file_path}' 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"오류: 압축 중 예기치 않은 오류 발생: {e}")

class UnzipWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="ZIP 압축 해제")
        self.set_border_width(10)
        self.set_default_size(400, 150)

        grid = Gtk.Grid(column_spacing=5, row_spacing=5)
        self.add(grid)

        # 대상 폴더 선택 버튼
        folder_label = Gtk.Label(label="압축 해제할 폴더:")
        grid.attach(folder_label, 0, 0, 1, 1)

        self.folder_entry = Gtk.Entry()
        self.folder_entry.set_editable(False)
        grid.attach(self.folder_entry, 1, 0, 2, 1)

        folder_button = Gtk.Button(label="선택")
        folder_button.connect("clicked", self.on_folder_clicked)
        grid.attach(folder_button, 3, 0, 1, 1)

        # ZIP 파일 선택 버튼
        file_label = Gtk.Label(label="ZIP 파일:")
        grid.attach(file_label, 0, 1, 1, 1)

        self.file_list_store = Gtk.ListStore(str)
        file_tree_view = Gtk.TreeView(model=self.file_list_store)
        file_renderer = Gtk.CellRendererText()
        file_column = Gtk.TreeViewColumn("선택된 ZIP 파일", file_renderer, text=0)
        file_tree_view.append_column(file_column)
        grid.attach(file_tree_view, 1, 1, 2, 1)

        file_button = Gtk.Button(label="추가")
        file_button.connect("clicked", self.on_file_clicked)
        grid.attach(file_button, 3, 1, 1, 1)

        # 압축 해제 버튼
        unzip_button = Gtk.Button(label="압축 해제")
        unzip_button.connect("clicked", self.on_unzip_start)
        grid.attach(unzip_button, 0, 2, 4, 1)

        self.extract_folder = None
        self.zip_files_to_unzip = []

    def on_folder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            "압축을 풀 폴더 선택", self, Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "선택", Gtk.ResponseType.OK)
        )
        dialog.set_default_size(800, 400)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.extract_folder = dialog.get_filename()
            self.folder_entry.set_text(self.extract_folder)
        dialog.destroy()

    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            "ZIP 파일 선택", self, Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        )
        dialog.set_default_size(800, 400)
        file_filter = Gtk.FileFilter()
        file_filter.set_name("ZIP 파일")
        file_filter.add_mime_type("application/zip")
        dialog.add_filter(file_filter)
        dialog.set_select_multiple(True)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            selected_files = dialog.get_filenames()
            for file in selected_files:
                if file not in self.zip_files_to_unzip:
                    self.zip_files_to_unzip.append(file)
                    self.file_list_store.append([file])
        dialog.destroy()

    def on_unzip_start(self, widget):
        if not self.extract_folder:
            self.show_message("오류", "압축을 풀 폴더를 먼저 선택해주세요.")
            return
        if not self.zip_files_to_unzip:
            self.show_message("오류", "압축 해제할 ZIP 파일을 선택해주세요.")
            return

        unzip_multiple(self.zip_files_to_unzip, self.extract_folder)
        self.show_message("완료", f"{len(self.zip_files_to_unzip)}개의 ZIP 파일 압축 해제를 완료했습니다.\n위치: {self.extract_folder}")
        self.file_list_store.clear()
        self.zip_files_to_unzip = []
        self.folder_entry.set_text("")
        self.extract_folder = None

    def show_message(self, title, message):
        dialog = Gtk.MessageDialog(
            self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, message
        )
        dialog.set_title(title)
        dialog.run()
        dialog.destroy()

class ZipWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="ZIP 압축")
        self.set_border_width(10)
        self.set_default_size(400, 200)

        grid = Gtk.Grid(column_spacing=5, row_spacing=5)
        self.add(grid)

        # 압축할 파일/폴더 선택
        file_label = Gtk.Label(label="압축할 파일/폴더:")
        grid.attach(file_label, 0, 0, 1, 1)
        self.file_list_store = Gtk.ListStore(str)
        file_tree_view = Gtk.TreeView(model=self.file_list_store)
        file_renderer = Gtk.CellRendererText()
        file_column = Gtk.TreeViewColumn("선택된 항목", file_renderer, text=0)
        file_tree_view.append_column(file_column)
        grid.attach(file_tree_view, 1, 0, 2, 1)
        add_button = Gtk.Button(label="추가")
        add_button.connect("clicked", self.on_add_clicked)
        grid.attach(add_button, 3, 0, 1, 1)

        # ZIP 파일 저장 위치 선택
        output_label = Gtk.Label(label="ZIP 파일 저장 위치:")
        grid.attach(output_label, 0, 1, 1, 1)
        self.output_entry = Gtk.Entry()
        self.output_entry.set_editable(False)
        grid.attach(self.output_entry, 1, 1, 2, 1)
        output_button = Gtk.Button(label="선택")
        output_button.connect("clicked", self.on_output_clicked)
        grid.attach(output_button, 3, 1, 1, 1)

        # 압축 시작 버튼
        zip_button = Gtk.Button(label="압축 시작")
        zip_button.connect("clicked", self.on_zip_start)
        grid.attach(zip_button, 0, 2, 4, 1)

        self.files_to_zip = []
        self.output_zip_file = None

    def on_add_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            "압축할 파일 또는 폴더 선택", self, Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        )
        dialog.set_default_size(800, 400)
        dialog.set_select_multiple(True)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            selected_items = dialog.get_filenames()
            for item in selected_items:
                if item not in self.files_to_zip:
                    self.files_to_zip.append(item)
                    self.file_list_store.append([item])
        dialog.destroy()

    def on_output_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            "ZIP 파일 저장 위치 선택", self, Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "저장", Gtk.ResponseType.OK)
        )
        dialog.set_default_size(800, 400)
        dialog.set_current_name(f"archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip")
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.output_zip_file = dialog.get_filename()
            self.output_entry.set_text(self.output_zip_file)
        dialog.destroy()

    def on_zip_start(self, widget):
        if not self.output_zip_file:
            self.show_message("오류", "ZIP 파일을 저장할 위치를 선택해주세요.")
            return
        if not self.files_to_zip:
            self.show_message("오류", "압축할 파일 또는 폴더를 선택해주세요.")
            return

        _zip_single(self.files_to_zip, self.output_zip_file)
        self.show_message("완료", f"'{self.output_zip_file}'로 압축을 완료했습니다.")
        self.file_list_store.clear()
        self.files_to_zip = []
        self.output_entry.set_text("")
        self.output_zip_file = None

    def show_message(self, title, message):
        dialog = Gtk.MessageDialog(
            self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, message
        )
        dialog.set_title(title)
        dialog.run()
        dialog.destroy()

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="KorZip")
        self.set_border_width(10)
        self.set_default_size(200, 100)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.add(vbox)

        unzip_button = Gtk.Button(label="압축 해제")
        unzip_button.connect("clicked", self.on_unzip_button_clicked)
        vbox.pack_start(unzip_button, True, True, 0)

        zip_button = Gtk.Button(label="압축")
        zip_button.connect("clicked", self.on_zip_button_clicked)
        vbox.pack_start(zip_button, True, True, 0)

        self.unzip_win = None
        self.zip_win = None

    def on_unzip_button_clicked(self, widget):
        if not self.unzip_win:
            self.unzip_win = UnzipWindow()
            self.unzip_win.connect("destroy", lambda w: setattr(self, 'unzip_win', None))
            self.unzip_win.show_all()
        else:
            self.unzip_win.present()

    def on_zip_button_clicked(self, widget):
        if not self.zip_win:
            self.zip_win = ZipWindow()
            self.zip_win.connect("destroy", lambda w: setattr(self, 'zip_win', None))
            self.zip_win.show_all()
        else:
            self.zip_win.present()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        main_win = MainWindow()
        main_win.connect("destroy", Gtk.main_quit)
        main_win.show_all()
        Gtk.main()
    elif len(sys.argv) >= 3:
        zip_files = sys.argv[1:-1]
        extract_path = sys.argv[-1]
        unzip_multiple(zip_files, extract_path)
    else:
        print("사용법:")
        print("  python script.py --gui             # GUI 모드 실행")
        print("  python script.py <zip_파일1> [<zip_파일2> ...] <대상_폴더> # CLI 모드로 압축 해제")

import math
import os
import subprocess
import sys

from PIL import Image, ImageFilter
from PySide2.QtCore import QEvent
from PySide2.QtGui import QPixmap, Qt, QIcon, QKeySequence
from PySide2.QtWidgets import QMainWindow, QLabel, QFileDialog, QDesktopWidget, QWidget, QStatusBar, QSizePolicy, \
    QGridLayout, QListWidget, QListWidgetItem, QSplitter, QMessageBox, QDialog, QAbstractItemView, QInputDialog


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.start_flag = None
        self.statusbar_view = None
        self.files_view = None
        self.photos = None
        self.labels = None
        self.status = None
        self.main_widget = None
        self.img = None
        self.selected_dir = None
        self.last_selected = None
        self.current_img_path = None
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle("Просмотр изображений")
        self.resize(1280, 720)
        self.setWindowIcon(QIcon("app-icon.png"))
        
        self.main_widget = QWidget()
        layout = QGridLayout()
    
        self.start_flag = False
        self.photos = QListWidget()
        self.photos.currentItemChanged.connect(self.changed_proc)
        self.photos.itemClicked.connect(self.click_on_photo)
        split_form = QSplitter(Qt.Horizontal)
        self.img = QLabel()
        self.img.setScaledContents(True)
        self.img.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.img.setPixmap(QPixmap("null.jpg"))
        bar = self.menuBar()
        file = bar.addMenu('Файл')
        open_file = file.addAction("Открыть")
        open_file.triggered.connect(self.open_proc)
        close_file = file.addAction("Закрыть")
        delete_file = file.addAction("Удалить")
        delete_file.triggered.connect(self.delete_proc)
        close_file.triggered.connect(self.close_proc)
        quit_app = file.addAction("Выйти")
        quit_app.triggered.connect(self.quit_proc)
        photo = bar.addMenu('Изображение')
        edit_photo = photo.addAction("Редактировать")
        edit_photo.triggered.connect(self.edit_proc)
        rotate = photo.addAction("Повернуть")
        rotate.triggered.connect(self.rotate_proc)
        change_size = photo.addAction("Изменить размер")
        change_size.triggered.connect(self.changesize_proc)
        filters = photo.addAction("Наложить фильтр")
        filters.triggered.connect(self.filter_proc)
        
        view = bar.addMenu('Вид')
        moving = bar.addMenu("Переход")
        forward = moving.addAction("Вперед")
        forward.setShortcut(QKeySequence("Right"))
        forward.triggered.connect(self.next_img)
        back = moving.addAction("Назад")
        back.setShortcut(QKeySequence("Left"))
        back.triggered.connect(self.back_img)
        self.statusbar_view = view.addAction("Показать строку состояния")
        self.statusbar_view.setCheckable(True)
        self.statusbar_view.setChecked(True)
        self.statusbar_view.triggered.connect(self.hide_status)
        self.files_view = view.addAction("Показать файлы")
        self.files_view.setCheckable(True)
        self.files_view.setChecked(True)
        self.files_view.triggered.connect(self.hide_files)
        info = bar.addMenu('Справка')
        about_form = info.addAction("О программе")
        about_form.triggered.connect(self.info_proc)
        
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        
        split_form.addWidget(self.photos)
        layout.addWidget(split_form, 0, 0, 8, 2)
        layout.addWidget(self.img, 0, 2, 8, 8)
        
        self.main_widget.setLayout(layout)
        self.setCentralWidget(self.main_widget)
        self.center_to_screen()
        
        self.img.installEventFilter(self)
        self.status.showMessage("Нажмите дважды на превью, чтобы выбрать файл", 15000)
    
    def rotate_proc(self):
    
        image, ext = os.path.splitext(os.path.basename(self.current_img_path))
        
        if not bool(self.current_img_path):
            imgg = Image.open(os.path.join(self.selected_dir, self.current_img_path))
        else:
            imgg = Image.open(self.current_img_path)
        
        text, result = QInputDialog.getText(self, "Повернуть",
                                            "Введите градус поворота: ")
        if result:
            out_img = imgg.rotate(int(text))
            out_img.save(f"output/rotate{int(text)}${image}{ext}")
    
    def changesize_proc(self):
        image, ext = os.path.splitext(os.path.basename(self.current_img_path))
    
        if not bool(self.current_img_path):
            imgg = Image.open(os.path.join(self.selected_dir, self.current_img_path))
        else:
            imgg = Image.open(self.current_img_path)
    
        text, result = QInputDialog.getText(self, "Изменить размер",
                                            "Введите размер в формате '1000x2222': ")
        if result:
            width, height = text.split('x')
            out_img = imgg.resize((int(width)//2, int(height)//2))
            out_img.save(f"output/{width}x{height}${image}{ext}")
    
    def filter_proc(self):
        image, ext = os.path.splitext(os.path.basename(self.current_img_path))
        name = os.path.basename(self.current_img_path)
    
        if not bool(self.current_img_path):
            imgg = Image.open(os.path.join(self.selected_dir, self.current_img_path))
        else:
            imgg = Image.open(self.current_img_path)
    
        text, result = QInputDialog.getText(self, "Применить фильтр",
                                            "Введите фильтр для применения, например: "
                                            "BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, "
                                            "EMBOSS, FIND_EDGES, SHARPEN, SMOOTH, SMOOTH_MORE")
        if result:
            if text == "BLUR":
                output_img = imgg.filter(ImageFilter.BLUR)
                output_img.save(f"output/BLURED${name}{ext}")
            elif text == "CONTOUR":
                output_img = imgg.filter(ImageFilter.CONTOUR)
                output_img.save(f"output/CONTOURED${name}{ext}")
            elif text == "DETAIL":
                output_img = imgg.filter(ImageFilter.DETAIL)
                output_img.save(f"output/DETAILED${name}{ext}")
            elif text == "EDGE_ENHANCE":
                output_img = imgg.filter(ImageFilter.EDGE_ENHANCE)
                output_img.save(f"output/EDGED${name}{ext}")
            elif text == "EMBOSS":
                output_img = imgg.filter(ImageFilter.EMBOSS)
                output_img.save(f"output/EMBOSSED${name}{ext}")
            elif text == "FIND_EDGES":
                output_img = imgg.filter(ImageFilter.FIND_EDGES)
                output_img.save(f"output/FINDED${name}{ext}")
            elif text == "SHARPEN":
                output_img = imgg.filter(ImageFilter.SHARPEN)
                output_img.save(f"output/SHARPENED${name}{ext}")
            elif text == "SMOOTH":
                output_img = imgg.filter(ImageFilter.SMOOTH)
                output_img.save(f"output/SMOOTHED${name}{ext}")
            elif text == "SMOOTH_MORE":
                output_img = imgg.filter(ImageFilter.SMOOTH_MORE)
                output_img.save(f"output/MORE_SMOOTHED${name}{ext}")
    
    def changed_proc(self, item):
        if bool(self.start_flag) and bool(item):
            path_to_image = os.path.join(self.selected_dir, item.text())
            self.current_img_path = path_to_image
            self.img.setPixmap(QPixmap(path_to_image))
        else:
            self.start_flag = True
    
    def next_img(self):
        index = self.photos.moveCursor(QAbstractItemView.MoveUp, Qt.NoModifier)
        if index.isValid():
            self.photos.setCurrentIndex(index)
    
    def back_img(self):
        index = self.photos.moveCursor(QAbstractItemView.MoveDown, Qt.NoModifier)
        if index.isValid():
            self.photos.setCurrentIndex(index)
    
    @staticmethod
    def info_proc():
        info_frame = QDialog()

        info_frame.setWindowTitle("Информация о приложении и авторе")
        info_frame.resize(300, 50)
        info_frame.setWindowIcon(QIcon("app-icon.png"))

        layout = QGridLayout()

        lb1 = QLabel()
        lb1.setPixmap(QPixmap("app-icon.png"))
        lb1.resize(150, 100)

        lb2 = QLabel("<b>PyPicView<b>")
        lb3 = QLabel("v0.1")
        lb4 = QLabel("PyPicView - простая программа для просмотра изображений и базового редактирования")
        lb5 = QLabel("Copyright © 2022 - the Independent developers")
        lb6 = QLabel("Это приложение распространяется без каких-либо гарантий.\n Подробнее в GNU Lesser "
                     "General Public License, версии 2 или позднее")

        for widget in [lb1, lb2, lb3, lb4, lb5, lb6]:
            widget.setAlignment(Qt.AlignCenter)
            layout.addWidget(widget)

        info_frame.setLayout(layout)
        info_frame.exec_()
    
    def hide_status(self):
        if not self.statusbar_view.isChecked():
            self.status.setHidden(True)
        else:
            self.status.setHidden(False)
    
    def hide_files(self):
        if not self.files_view.isChecked():
            self.photos.setHidden(True)
        else:
            self.photos.setHidden(False)
    
    def edit_proc(self):
        if bool(self.current_img_path):
            subprocess.call(["exo-open", self.current_img_path])
    
    def eventFilter(self, obj, event):
        if obj is self.img and event.type() == QEvent.MouseButtonDblClick:
            self.status.clearMessage()
            title = "Открыть фотокарточку"
            directory = os.getcwd()
            filter_file = "Images (*.png *.jpg)"
            file_path = QFileDialog.getOpenFileName(self, title, directory, filter_file)[0]
            if bool(file_path):
                self.img.setPixmap(QPixmap(file_path))
                name = os.path.basename(file_path)
                self.img_proc(file_path)
                self.selected_dir = os.path.abspath(os.path.dirname(file_path))
                self.fill_photos()
                self.status.showMessage(f"Файл {name} открыт", 15000)
                self.current_img_path = os.path.join(self.selected_dir, file_path)
        return super().eventFilter(obj, event)
    
    def open_proc(self):
        self.status.clearMessage()
        name = ""
        title = "Открыть фотокарточку"
        directory = os.getcwd()
        filter_file = "Images (*.png *.jpg)"
        file_path = QFileDialog.getOpenFileName(self, title, directory, filter_file)[0]
        if bool(file_path):
            self.img.setPixmap(QPixmap(file_path))
            self.img_proc(file_path)
            self.selected_dir = os.path.abspath(os.path.dirname(file_path))
            name = os.path.basename(file_path)
            self.fill_photos()
            self.current_img_path = os.path.join(self.selected_dir, file_path)
        self.status.showMessage(f"Файл {name} открыт", 15000)
    
    def close_proc(self):
        self.start_flag = False
        self.img.setPixmap(QPixmap("null.jpg"))
        self.photos.clear()
        self.status.clearMessage()
        self.status.showMessage("Нажмите дважды на превью, чтобы выбрать файл", 15000)
    
    @staticmethod
    def quit_proc():
        sys.exit()
    
    def delete_proc(self):
        if bool(self.current_img_path):
            warning_message = QMessageBox()
            warning_message.resize(300, 50)
            warning_message.setWindowTitle("Удаление файла")
            warning_message.setText(f"Вы уверены, что хотите \nудалить {self.current_img_path} ?")
            if warning_message.exec_() == QDialog.Accepted:
                removed_file = os.path.join(self.selected_dir, self.current_img_path)
                os.remove(removed_file)
                self.status.showMessage(f"Файл {self.current_img_path} был успешно удалён", 15000)
    
    def click_on_photo(self, item):
        self.last_selected = item.text()
        self.current_img_path = self.last_selected
        self.img.setPixmap(QPixmap(os.path.join(self.selected_dir, item.text())))
        self.img_proc(os.path.join(self.selected_dir, item.text()))
    
    def fill_photos(self):
        self.photos.clear()
        
        if bool(self.selected_dir):
            for image in os.listdir(self.selected_dir):
                filename, ext = os.path.splitext(image)
                if ext == ".png" or ext == ".jpg":
                    image_path = os.path.join(self.selected_dir, image)
                    pixmap = QPixmap(image_path)
    
                    name = os.path.basename(image_path)
                    item = QListWidgetItem()
                    item.setIcon(QIcon(pixmap))
                    item.setText(name)
                    self.photos.addItem(item)
    
    def img_proc(self, path_to_img):
        image = Image.open(path_to_img)

        name = os.path.basename(image.filename)
        image_size = f"{image.width} x {image.height}"
        image_bytesize = f"{math.ceil(os.stat(path_to_img).st_size / 1024)} КиБ"

        self.img.setToolTip(f"{name}  {image_size}  {image_bytesize}")

    def center_to_screen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))
from PySide6.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    DEFAULT_W = 800
    DEFAULT_H = 600
    DEFAULT_SCREEN_SIZE = (DEFAULT_W, DEFAULT_H)
    DEFAULT_ICON_PATH = 'icons/app-icon.png'
    MIN_W = 480
    MIN_H = 320
    MIN_SCREEN_SIZE = (MIN_W, MIN_H)
    DEFAULT_ICON_SIZE = 32
    
    def __init__(self):
        super().__init__()
        from edit import Edit
        from path_list import PathList
        from PySide6.QtWidgets import QLabel
        
        self.list_obj = PathList()
        self.edit_obj = Edit()
        self.picture = QLabel()
        self.flag = True
        self.init_gui()
        
    def init_gui(self):
        from PySide6.QtGui import Qt, QIcon, QKeySequence, QAction
        from PySide6.QtWidgets import QToolBar, QSizePolicy, QHBoxLayout
        from PySide6.QtCore import QSize
        from screen import Screen
        
        self.setWindowTitle('Просмотр изображений')
        self.resize(self.DEFAULT_W, self.DEFAULT_H)
        self.setWindowIcon(QIcon(self.DEFAULT_ICON_PATH))

        self.main_tools = QToolBar()
        self.main_tools.setIconSize(QSize(self.DEFAULT_ICON_SIZE, \
                    self.DEFAULT_ICON_SIZE))
        self.main_tools.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.main_tools)
        upload = QAction(QIcon('icons/upload_file.png'), \
                    'Открыть картинку', self)
        effect = QAction(QIcon('icons/effect.png'), \
                    'Выбрать фильтр для картинки', self)
        resize = QAction(QIcon('icons/resize.png'), \
                    'Изменить размер картинки', self)
        down = QAction(QIcon('icons/arrow_down.png'), \
                    'Предыдущая картинка', self)
        up = QAction(QIcon('icons/arrow_up.png'), \
                    'Следующая картинка', self)
        save_image = QAction(QIcon('icons/save_file.png'), \
                    'Сохранить изменения', self)
        rotate_left = QAction(QIcon('icons/rotate_right.png'), \
                    'Повернуть против часовой стрелки', self)
        rotate_right = QAction(QIcon('icons/rotate_left.png'), \
                    'Повернуть по часовой стрелке', self)
        close = QAction(QIcon('icons/close_image.png'), \
                    'Закрыть картинку', self)
        delete = QAction(QIcon('icons/trash.png'), 'Удалить картинку', self)
        image_info = QAction(QIcon('icons/image_info.png'), \
                    'Показать информацию о картинке', self)
        self.main_tools.addActions([upload, effect, image_info, close, resize, delete, up, down, \
                    save_image, rotate_left, rotate_right])
        upload.triggered.connect(self.open_proc)
        down.triggered.connect(self.prev_proc)
        up.triggered.connect(self.next_proc)
        save_image.triggered.connect(self.save_proc)
        rotate_left.triggered.connect(self.rotate_l)
        rotate_right.triggered.connect(self.rotate_r)
        close.triggered.connect(self.close_proc)
        delete.triggered.connect(self.delete_proc)
        resize.triggered.connect(self.resize_proc)
        effect.triggered.connect(self.effect_proc)
        image_info.triggered.connect(self.image_proc)
        bar = self.menuBar()
        file = bar.addMenu('Файл')
        open_file = file.addAction('Открыть')
        open_file.triggered.connect(self.open_proc)
        close_image = file.addAction('Закрыть')
        save_img = file.addAction('Сохранить')
        save_img.triggered.connect(self.save_proc)
        delete_file = file.addAction('Удалить')
        close_image.triggered.connect(self.close_proc)
        photo = bar.addMenu('Изображение')
        view = bar.addMenu('Вид')
        self.toolbar_view = view.addAction('Показать панель инструментов')
        self.toolbar_view.setCheckable(True)
        move = bar.addMenu('Переход')
        move_next = move.addAction('Перейти к следующей картинке')
        move_next.setShortcut(QKeySequence('Right'))
        move_prev = move.addAction('Перейти к предыдущей картинке')
        move_prev.setShortcut(QKeySequence('Left'))
        about_photo = photo.addAction('Посмотреть информацию о картинке')
        resize_photo = photo.addAction('Изменить размер картинки')
        filter_photo = photo.addAction('Выбрать фильтр для картинки')
        rotate_intime = photo.addAction('Повернуть картинку по часовой')
        rotate_antitime = photo.addAction('Повернуть картинку против часовой')
        delete_file.triggered.connect(self.delete_proc)
        rotate_intime.triggered.connect(self.rotate_l)
        rotate_antitime.triggered.connect(self.rotate_r)
        move_next.triggered.connect(self.next_proc)
        move_prev.triggered.connect(self.prev_proc)
        resize_photo.triggered.connect(self.resize_proc)
        filter_photo.triggered.connect(self.effect_proc)
        self.toolbar_view.triggered.connect(self.toolbar_proc)
        info = bar.addMenu('Справка')
        about_form = info.addAction('О программе')
        about_form.triggered.connect(self.info_proc)
        about_photo.triggered.connect(self.image_proc)

        self.picture.setMinimumSize(self.MIN_W, self.MIN_H)
        self.picture.setSizePolicy(QSizePolicy.Policy.Ignored, \
                    QSizePolicy.Policy.Ignored)
        self.picture.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout = QHBoxLayout()
        layout.addWidget(self.picture)
        self.setCentralWidget(self.picture)
        self.setLayout(layout)
        Screen.center(self)
        self.main_tools.hide()
    
    def image_proc(self):
        from PySide6.QtWidgets import QMessageBox
        from os.path import basename
        from os import stat
        
        if self.list_obj.exists:
            size = f'{self.edit_obj.obj.width} x {self.edit_obj.obj.height}'
            rounded_size = round(((stat(self.edit_obj.path).st_size)/1024), 1)
            bytesize = f'{rounded_size} КиБ'
            name = basename(self.edit_obj.obj.filename)
            format = self.edit_obj.obj.format
            mode = self.edit_obj.obj.mode
            
            result = QMessageBox.warning(
                self,
                'Информация о картинке',
                (f'Размер: {size}\n'
                f'Размер в байтах: {bytesize}\n'
                f'Название: {name}\n'
                f'Формат: {format}\n'
                f'Режим: {mode}'),
                buttons=QMessageBox.StandardButton.Close,
                defaultButton=QMessageBox.StandardButton.Close
            )
    
    def toolbar_proc(self):
        self.main_tools.setHidden(not self.toolbar_view.isChecked())
    
    def effect_proc(self):
        from PySide6.QtWidgets import QInputDialog
        
        if self.list_obj.exists:
            text, ok = QInputDialog.getText(
                self,
                'Выбрать эффект',
                ('Введите название эффекта: \n' 
                '(BLUR,\n' 
                'CONTOUR,\n'
                'DETAIL,\n'
                'EDGE_ENHANCE,\n'
                'EMBOSS,\n'
                'FIND_EDGES,\n'
                'SHARPEN,\n' 
                'SMOOTH,\n'
                'SMOOTH_MORE)')
            )
        
            if ok and text:
                self.edit_obj.filter(text)
                self.display_proc(self.edit_obj.qtimage)
    
    def resize_proc(self):
        from PySide6.QtWidgets import QInputDialog
        
        if self.list_obj.exists:
            text, ok = QInputDialog.getText(
                self,
                'Изменить размер',
                'Введите размер в формате: 300x300'
            )
        
            if ok and text:
                tuple = text.split('x')
                self.edit_obj.resize((int(tuple[0]), int(tuple[1])))
                self.display_proc(self.edit_obj.qtimage)
    
    def close_proc(self):
        if self.list_obj.exists:
            self.list_obj.clear()
            self.edit_obj.clear()
            self.picture.clear()
    
    def delete_proc(self):
        from PySide6.QtWidgets import QMessageBox
        from os import remove
        
        if self.list_obj.exists:
            result = QMessageBox.warning(
                self,
                'Удаление картинки',
                'Удалить картинку? Её нельзя будет восстановить.',
                buttons=QMessageBox.StandardButton.No |
                    QMessageBox.StandardButton.Yes,
                defaultButton=QMessageBox.StandardButton.Yes
            )
            
            if result == QMessageBox.StandardButton.Yes:
                remove(self.edit_obj.path)
                self.prev_proc()
                self.list_obj.clear()
                self.fill_proc()
            
    
    def rotate_l(self):
        if self.list_obj.exists:
            self.edit_obj.rotate(90)
            self.display_proc(self.edit_obj.qtimage)
            
    def rotate_r(self):
        if self.list_obj.exists:
            self.edit_obj.rotate(-90)
            self.display_proc(self.edit_obj.qtimage)
    
    def scale_proc(self, qtimage):
        from PySide6.QtGui import QPixmap, Qt
        
        pixmap = QPixmap.fromImage(qtimage).scaled(self.picture.size(), \
                    aspectMode=Qt.KeepAspectRatio)
        self.picture.setPixmap(pixmap)
        self.picture.repaint()
    
    def prev_proc(self):
        if self.list_obj.exists:
            self.edit_obj.open(self.list_obj.prev())
            self.scale_proc(self.edit_obj.qtimage)
                
    def next_proc(self):
        if self.list_obj.exists:
            self.edit_obj.open(self.list_obj.next())
            self.scale_proc(self.edit_obj.qtimage)
    
    def save_proc(self):
        if self.list_obj.exists:
            self.edit_obj.obj.save(self.edit_obj.path)
      
    def info_proc(self):
        from info import InfoDialog
        
        dlg = InfoDialog()
        dlg.exec()
    
    def display_proc(self, qtimage):
        self.scale_proc(qtimage)
        self.fill_proc()
        # self.img_proc()
    
    def open_proc(self):
        from PySide6.QtWidgets import QFileDialog
        from os import getcwd
        
        path = QFileDialog.getOpenFileName(self, 'Открыть фотокарточку', \
                    getcwd(), 'Images (*.png *.jpg)')[0]
        self.edit_obj.open(path)
        self.display_proc(self.edit_obj.qtimage)
    
    def resizeEvent(self, event):
        if self.list_obj.exists:
            self.scale_proc(self.edit_obj.qtimage)
    
    def fill_proc(self):
        from os import path, listdir
        
        dir = path.abspath(path.dirname(self.edit_obj.path))
        for image in listdir(dir):
            name, ext = path.splitext(image)
            if ext == '.png' or ext == '.jpg':
                image_path = path.join(dir, \
                            image)
                self.list_obj.add(image_path)

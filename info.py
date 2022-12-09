from PySide6.QtWidgets import QDialog

class InfoDialog(QDialog):
        DEFAULT_W = 150
        DEFAULT_H = 50
        DEFAULT_ICON_PATH = 'icons/app-icon.png'
        DEFAULT_IMG_W = 256
        DEFAULT_IMG_H = 256
    
        def __init__(self):
            from screen import Screen
            
            super().__init__()
            self.init_gui()
            Screen.center(self)

        def init_gui(self):
                from PySide6.QtWidgets import QVBoxLayout, QLabel, QGroupBox
                from PySide6.QtGui import QIcon, QPixmap, Qt

                self.setWindowTitle('О программе')
                self.resize(self.DEFAULT_W, self.DEFAULT_H)
                self.setWindowIcon(QIcon(self.DEFAULT_ICON_PATH))

                layout = QVBoxLayout()

                vbox:QVBoxLayout = QVBoxLayout()
                box = QGroupBox()
                image = QLabel()
                image.resize(self.DEFAULT_IMG_W, self.DEFAULT_IMG_H)
                label_size = image.size()
                pixmap = QPixmap(self.DEFAULT_ICON_PATH).scaled(label_size, \
                                    aspectMode=Qt.KeepAspectRatio)
                image.setPixmap(pixmap)
                image.repaint()
                lb2 = QLabel('<b>pyPicView<b>')
                lb3 = QLabel('<i>v0.2<i>')
                lb4 = QLabel('PyPicView - простая программа для '
                            'просмотра изображений и базового редактирования.')
                lb5 = QLabel('Copyright © 2022 - the Independent developers.')
                lb6 = QLabel('Это приложение распространяется без каких-либо гарантий.')
                lb7 = QLabel('Подробнее в GNU Lesser General Public License, версии 2 или позднее.')

                for el in [lb2, lb3, lb4, lb5, lb6, lb7]:
                    vbox.addWidget(el)
                    el.setAlignment(Qt.AlignmentFlag().AlignCenter)
                box.setLayout(vbox)

                layout.addWidget(image)
                image.setAlignment(Qt.AlignmentFlag().AlignCenter)
                layout.addWidget(box)
                
                self.setLayout(layout)
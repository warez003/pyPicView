class Screen:
    
    @staticmethod
    def center(win):
        from PySide6.QtGui import QScreen
        from PySide6.QtWidgets import QApplication

        primary = QApplication.primaryScreen()
        center = QScreen.availableGeometry(primary).center()
        win.frameGeometry().moveCenter(center)
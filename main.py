def main():
    from PySide6.QtWidgets import QApplication
    from form import MainWindow
    from sys import exit, argv
    
    app = QApplication(argv)
    form = MainWindow()
    form.show()
    exit(app.exec())

if __name__ == '__main__':
    main()
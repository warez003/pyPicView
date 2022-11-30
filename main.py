from PySide2.QtWidgets import QApplication

import view
import sys

def main():
    app = QApplication(sys.argv)
    main_form = view.Window()
    main_form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
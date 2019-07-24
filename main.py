import sys
from PyQt5.QtWidgets import QApplication
from view.window import AppWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AppWindow()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QMenu
from PyQt5.QtGui import QIcon
from view.widget import MainWidget
from controller.save_results import CsvSaver, TxtSaver, PdfSaver


class AppWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.init_ui()
        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)
        self.setWindowIcon(QIcon("img/python.png"))

    def init_ui(self):
        save_menu = QMenu("&Save results as...", self)

        csv_saver = CsvSaver()
        save_csv_act = QAction(".&csv (data)", self)
        save_csv_act.setShortcut('Ctrl+S')
        save_csv_act.setStatusTip("Save results to CSV file")
        save_csv_act.triggered.connect(lambda: csv_saver.choose_filename())
        save_menu.addAction(save_csv_act)

        txt_saver = TxtSaver()
        save_txt_act = QAction(".&txt (data)", self)
        save_txt_act.setStatusTip("Save results to TXT file")
        save_txt_act.triggered.connect(lambda: txt_saver.choose_filename())
        save_menu.addAction(save_txt_act)

        pdf_saver = PdfSaver()
        save_pdf_act = QAction(".&pdf (plot)", self)
        save_pdf_act.setStatusTip("Save plot to PDF file")
        save_pdf_act.triggered.connect(lambda: pdf_saver.choose_filename())
        save_menu.addAction(save_pdf_act)

        exit_act = QAction(QIcon('exit.png'), '&Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&Menu')
        file_menu.addMenu(save_menu)
        file_menu.addAction(exit_act)

        self.setGeometry(300, 200, 1225, 740)
        self.setWindowTitle("Python & Cython Speed Tester")
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AppWindow()
    sys.exit(app.exec_())

from PyQt5.QtWidgets import QWidget, QCheckBox, QPushButton, QFileDialog, QLineEdit, QTableWidget, QTableView, \
    QTableWidgetItem, QHBoxLayout, QVBoxLayout, QHeaderView, QMessageBox, QLabel
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from controller.mediator import Mediator
from controller.get_modules import get_modules
from model.plot import PlotCanvas
from model.already_tested_error import AlreadyTestedError
# import numpy as np


class MainWidget(QWidget):
    """
    Design Pattern: Singleton.
    """

    __instance = None

    def __init__(self):
        """
        Creates Main Widget.
        """
        if type(self).__instance is None:
            super().__init__()
            self._mediator = Mediator()
            self._interface()
            type(self).__instance = self
        else:
            self.get_instance()

    @staticmethod
    def get_instance():
        if MainWidget.__instance is not None:
            return MainWidget.__instance
        else:
            MainWidget.__instance = MainWidget()
            return MainWidget.__instance

    def _interface(self):
        self.layout = QHBoxLayout()
        self.layout.setSpacing(20)
        py_path_layout = QHBoxLayout()
        cy_path_layout = QHBoxLayout()
        samples_layout = QHBoxLayout()
        left_layout = QVBoxLayout()

        py_checkbox = QCheckBox("Run Python", self)
        py_checkbox.stateChanged.connect(self.checkbox_action)
        self._mediator.checks[py_checkbox.text()] = py_checkbox
        py_path_layout.addWidget(py_checkbox)

        self.py_path = QLineEdit(self)
        self.py_path.resize(460, 25)
        self.py_path.setReadOnly(True)
        self.py_path.setEnabled(False)
        py_path_layout.addWidget(self.py_path)

        py_button = QPushButton("Browse (.py)", self)
        py_button.setToolTip("Browse for Python File")
        py_button.clicked.connect(lambda: self.open_file_dialog("py"))
        py_button.setEnabled(False)
        self._mediator.buttons[py_button.text()] = py_button, self.py_path
        py_path_layout.addWidget(py_button)

        left_layout.addLayout(py_path_layout)

        cy_checkbox = QCheckBox("Run Cython", self)
        cy_checkbox.move(20, 60)
        cy_checkbox.stateChanged.connect(self.checkbox_action)
        self._mediator.checks[cy_checkbox.text()] = cy_checkbox
        cy_path_layout.addWidget(cy_checkbox)

        self.cy_path = QLineEdit(self)
        self.cy_path.move(150, 60)
        self.cy_path.resize(460, 25)
        self.cy_path.setReadOnly(True)
        self.cy_path.setEnabled(False)
        cy_path_layout.addWidget(self.cy_path)

        cy_button = QPushButton("Browse (.pyd)", self)
        cy_button.setToolTip("Browse for Cython Extension Module")
        cy_button.move(630, 60)
        cy_button.clicked.connect(lambda: self.open_file_dialog("cy"))
        cy_button.setEnabled(False)
        self._mediator.buttons[cy_button.text()] = cy_button, self.cy_path
        cy_path_layout.addWidget(cy_button)

        left_layout.addLayout(cy_path_layout)

        both_checkbox = QCheckBox("Run Both", self)
        both_checkbox.move(20, 100)
        both_checkbox.stateChanged.connect(self.checkbox_action)
        self._mediator.checks[both_checkbox.text()] = both_checkbox
        left_layout.addWidget(both_checkbox)

        samples_label = QLabel("Samples:")
        self.samples_line = QLineEdit(self)
        validator = QRegExpValidator(QRegExp("([0-9]+,)+"))
        self.samples_line.setValidator(validator)
        # samples = np.geomspace(3, 10000, 20, dtype=int)
        # samples = np.array2string(samples, separator=",")[1:-1].replace(" ", "").replace("\n", "")
        samples = "10, 20, 30, 40, 50, 60, 70, 80, 90, 100"
        self.samples_line.setText(samples)
        samples_increase = QPushButton("*10", self)
        samples_increase.clicked.connect(self.increase_samples)
        samples_decrease = QPushButton("/10", self)
        samples_decrease.clicked.connect(self.decrease_samples)
        samples_layout.addWidget(samples_label)
        samples_layout.addWidget(self.samples_line)
        samples_layout.addWidget(samples_increase)
        samples_layout.addWidget(samples_decrease)
        left_layout.addLayout(samples_layout)

        run_button = QPushButton("Run", self)
        run_button.setToolTip("Run selected tests")
        run_button.move(20, 140)
        run_button.clicked.connect(self.run_action)
        left_layout.addWidget(run_button)

        self.plot = PlotCanvas(self)
        self.plot.move(20, 200)
        left_layout.addWidget(self.plot)

        left_layout.setContentsMargins(5, 5, 5, 5)
        self.layout.addLayout(left_layout)

        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Python", "Cython"])
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)

        self.layout.addWidget(self.table_widget)

        self.setLayout(self.layout)

        self.show()

    def checkbox_action(self, state):
        self._mediator.update(self.sender().text(), state)

    def run_action(self):
        if self.samples_line.text()[-1] == ",":
            self.samples_line.setText(self.samples_line.text()[:-1])
        try:
            get_modules(self.samples_line.text(),
                        self.py_path.text() if self._mediator.checks["Run Python"].isChecked() else "",
                        self.cy_path.text() if self._mediator.checks["Run Cython"].isChecked() else "")
        except AlreadyTestedError as e:
            msg = QMessageBox.question(self, "Message", str(e),
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if msg == QMessageBox.Yes:
                self.plot.clear_plot()
                self.run_action()
            else:
                pass
        except AttributeError as e:
            QMessageBox.warning(self, "Message", str(e), QMessageBox.Ok, QMessageBox.Ok)
            return

        if self.py_path.text() == "":
            self._mediator.checks["Run Python"].setChecked(False)
        if self.cy_path.text() == "":
            self._mediator.checks["Run Cython"].setChecked(False)

        loops, py_data, cy_data = None, None, None
        if len(self.plot.ax.lines) == 2:
            loops = self.plot.ax.lines[0].get_xdata()
            if self._mediator.checks["Run Python"].isChecked() and self.py_path.text() != "":
                py_data = self.plot.ax.lines[0].get_ydata()
            elif self._mediator.checks["Run Cython"].isChecked() and self.cy_path.text() != "":
                cy_data = self.plot.ax.lines[0].get_ydata()
        else:
            loops = self.plot.ax.lines[0].get_xdata()
            py_data = self.plot.ax.lines[0].get_ydata()
            cy_data = self.plot.ax.lines[2].get_ydata()

        if loops is not None:
            self.table_widget.setRowCount(loops.shape[0])
            self.table_widget.setVerticalHeaderLabels(loops.astype('str'))
        if py_data is not None:
            for i in range(loops.shape[0]):
                self.table_widget.setItem(i, 0, QTableWidgetItem(str(round(py_data[i], 5)) + " s"))
        if cy_data is not None:
            for i in range(loops.shape[0]):
                self.table_widget.setItem(i, 1, QTableWidgetItem(str(round(cy_data[i], 5)) + " s"))

    def open_file_dialog(self, version):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        if version == "py":
            file_name, _ = QFileDialog.getOpenFileName(self, "Select File", "",
                                                       "Python Files (*.py)",
                                                       options=options)
            self.py_path.setText(file_name)

        if version == "cy":
            file_name, _ = QFileDialog.getOpenFileName(self, "Select File", "",
                                                       "Cython Files (*.pyd)",
                                                       options=options)
            self.cy_path.setText(file_name)

    def increase_samples(self):
        samples = self.samples_line.text()
        samples = samples.split(",")
        if samples[-1] == '':
            del samples[-1]
        samples = [str(int(x)*10) for x in samples]
        samples = ", ".join(samples)
        self.samples_line.setText(samples)

    def decrease_samples(self):
        samples = self.samples_line.text()
        samples = samples.split(",")
        if samples[-1] == '':
            del samples[-1]
        if any([x < 10 for x in list(map(int, samples))]):
            return
        else:
            samples = [str(int(x) // 10) for x in samples]
            samples = ", ".join(samples)
            self.samples_line.setText(samples)
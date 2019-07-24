from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMessageBox
from model.plot import PlotCanvas
from view.widget import MainWidget
import numpy as np
from datetime import datetime
from abc import ABC, abstractmethod


class ResultsSaver(ABC):
    """
    Design Pattern: Template Method
    """
    def choose_filename(self):
        widget = MainWidget.get_instance()
        now = datetime.now()
        allowed_file_name = False
        not_allowed_chars = {'/', '\\', ':', '*', '?', '"', '<', '>', '|'}
        while not allowed_file_name:
            file_name, ok_pressed = QInputDialog.getText(widget, "Save results", "File Name:", QLineEdit.Normal,
                                                         "test-" + now.strftime("%Y-%m-%d_%H-%M-%S"))
            if not ok_pressed:
                break
            if set(file_name).intersection(not_allowed_chars) != set():
                QMessageBox.warning(widget, "Error", "Wrong file name")
            else:
                allowed_file_name = True
        if ok_pressed and file_name != '':
            plot = PlotCanvas.get_instance()

            if widget._mediator.checks["Run Python"].isChecked():
                lines = plot.ax.lines[0].get_xdata()
                py_data = plot.ax.lines[0].get_ydata()
                if widget._mediator.checks["Run Cython"].isChecked():
                    cy_data = plot.ax.lines[2].get_ydata()
                else:
                    cy_data = np.full(len(lines), None)
            elif widget._mediator.checks["Run Cython"].isChecked():
                lines = plot.ax.lines[0].get_xdata()
                py_data = np.full(len(lines), None)
                cy_data = plot.ax.lines[0].get_ydata()
            else:
                lines = np.array(None)
                py_data = np.array(None)
                cy_data = np.array(None)
            
            self.save_results(file_name, [lines, py_data, cy_data])

    @abstractmethod
    def save_results(self, file_name, data):
        pass


class CsvSaver(ResultsSaver):
    def save_results(self, file_name, data): 
        np.savetxt(file_name + ".csv", np.column_stack(data),
                   delimiter=",", fmt='%s', header="arg, python, cython")


class TxtSaver(ResultsSaver):
    def save_results(self, file_name, data):
        np.savetxt(file_name + ".txt", np.column_stack(data),
                   delimiter=";", fmt='%s', header="arg, python, cython")


class PdfSaver(ResultsSaver):
    def save_results(self, file_name, data):
        widget = MainWidget.get_instance()
        widget.plot.figure.savefig(file_name + ".pdf", format="pdf")
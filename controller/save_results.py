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

            data = [plot.ax.lines[0].get_xdata()]

            for i in range(len(plot.ax.lines) // 2):
                data.append([])
                data[i+1] = plot.ax.lines[2*i].get_ydata()

            labels_list = plot.ax.get_legend_handles_labels()[1]
            labels = "sample size;" + ";".join(labels_list)
            
            self.save_results(file_name, [d for d in data], labels)

    @abstractmethod
    def save_results(self, file_name, data, labels):
        pass


class CsvSaver(ResultsSaver):
    def save_results(self, file_name, data, labels): 
        np.savetxt(file_name + ".csv", np.column_stack(data),
                   delimiter=",", fmt='%s', header=labels)


class TxtSaver(ResultsSaver):
    def save_results(self, file_name, data, labels):
        np.savetxt(file_name + ".txt", np.column_stack(data),
                   delimiter=";", fmt='%s', header=labels)


class PdfSaver(ResultsSaver):
    def save_results(self, file_name, data):
        widget = MainWidget.get_instance()
        widget.plot.figure.savefig(file_name + ".pdf", format="pdf")
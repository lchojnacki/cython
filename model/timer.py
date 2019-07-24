from PyQt5.QtWidgets import QApplication
from timeit import default_timer as timer
from model.plot import PlotCanvas
from model.already_tested_error import AlreadyTestedError
from view.progbar import ProgressBar
import os
import sys


class Timer:
    """
    Design Pattern: Decorator
    """
    def __init__(self, module, spec):
        self.spec = spec
        self.module = module

    def __call__(self, samples):
        plot = PlotCanvas.get_instance()
        name = self.module.__name__
        if name in plot.ax.get_legend_handles_labels()[1]:
            raise AlreadyTestedError("At least one of the functions has already been tested. Test again?")
        times = []
        loops = 100
        for n in samples:
            s = 0
            pb = ProgressBar("Timing module " + name + " (" + str(n) + ")")
            for i in range(loops):
                start = timer()
                self.module.test(n)
                end = timer()
                s += end - start
                pb.setValue(i)
                QApplication.processEvents()
            times.append(s / loops)
            pb.close()
        plot.update_plot(samples, times, name)

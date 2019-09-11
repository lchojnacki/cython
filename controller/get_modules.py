from importlib.util import spec_from_file_location, module_from_spec
from model.timer import Timer
import sys


def get_modules(samples, path_py, path_cy, ignore_error=False):

    samples = samples.split(",")
    samples = list(map(int, samples))
    samples.sort()

    if path_py != "":
        module_name_py = path_py.split("/")[-1].replace(".py", "")
        module_path_py = "//".join(path_py.split("/")[:-1])
        spec_py = spec_from_file_location(module_name_py, path_py)
        module_py = module_from_spec(spec_py)
        sys.path.insert(0, module_path_py)
        spec_py.loader.exec_module(module_py)
        timer_py = Timer(module_py, spec_py)
        timer_py(samples, ignore_error)

    if path_cy != "":
        module_name_cy = path_cy.split("/")[-1].replace(".cp36-win_amd64.pyd", "")
        module_path_cy = "//".join(path_cy.split("/")[:-1])
        spec_cy = spec_from_file_location(module_name_cy, path_cy)
        module_cy = module_from_spec(spec_cy)
        sys.path.insert(0, module_path_cy)
        spec_cy.loader.exec_module(module_cy)
        timer_cy = Timer(module_cy, spec_cy)
        timer_cy(samples, ignore_error)

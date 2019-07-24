from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import Cython.Compiler.Options
import numpy

Cython.Compiler.Options.annotate = True

ext_modules = [
    Extension("for_loop", ["for_loop.pyx"],
              include_dirs=[numpy.get_include()], define_macros=[('CYTHON_TRACE', '1')]),
    Extension("convex_hull_numpy", ["convex_hull_numpy.pyx"],
              include_dirs=[numpy.get_include()], define_macros=[('CYTHON_TRACE', '1')])
]

setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules,
    script_args=['build_ext'],
    options={'build_ext': {'inplace': True, 'force': True}}
)

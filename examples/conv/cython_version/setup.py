from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import Cython.Compiler.Options
import numpy


Cython.Compiler.Options.annotate = True

ext_modules = [
    #Extension("figures.point", ["figures/point.pyx"]),
    #Extension("algorithms.convex_hull_objects", ["algorithms/convex_hull_objects.pyx"],
    #          define_macros=[('CYTHON_TRACE', '1')]),
    #Extension("algorithms.convex_hull_objects_py", ["algorithms/convex_hull_objects_py.pyx"],
    #          define_macros=[('CYTHON_TRACE', '1')]),
    #Extension("algorithms.convex_hull_structs", ["algorithms/convex_hull_structs.pyx"],
    #          define_macros=[('CYTHON_TRACE', '1')]),
    #Extension("algorithms.convex_hull_numpy", ["algorithms/convex_hull_numpy.pyx"],
    #          include_dirs=[numpy.get_include()], define_macros=[('CYTHON_TRACE', '1')]),
    Extension("algorithms.convex_hull_memoryview", ["algorithms/convex_hull_memoryview.pyx"],
              include_dirs=[numpy.get_include()], define_macros=[('CYTHON_TRACE', '1')])
]

setup(
    name='geometry',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules,
    script_args=['build_ext'],
    options={'build_ext': {'inplace': True, 'force': True}}
)

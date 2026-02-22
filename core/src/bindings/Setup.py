from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

setup(
    name = 'callback',
    ext_modules=cythonize([
        Extension("molaccescy", ["molacces_python_wrapper.pyx", "molacces_python.c"]),
    ]),
)

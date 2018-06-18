import os
import sys
from cx_Freeze import setup, Executable

#to run this (on Windows) > `python setup.py build`
#after building will need to copy `distances_json` directory into /build/exe.win32-3.6 manually.
#to run click `/build/exe.win32-3.6/main`


os.environ['TCL_LIBRARY'] = 'C:/Users/paul/AppData/Local/Programs/Python/Python36-32/tcl/tcl8.6'
os.environ['TK_LIBRARY'] = 'C:/Users/paul/AppData/Local/Programs/Python/Python36-32/tcl/tk8.6'

buildOptions = dict(
    packages=[],
    excludes=[],
    include_files=[
        'C:/Users/paul/AppData/Local/Programs/Python/Python36-32/DLLs/tcl86t.dll',
        'C:/Users/paul/AppData/Local/Programs/Python/Python36-32/DLLs/tk86t.dll']
    )

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable('main.py', base=base)
    ]

setup(name='distancesbetweenworldports',
        version='1.0',
        description='',
        options = dict(build_exe = buildOptions),
        executables = executables)


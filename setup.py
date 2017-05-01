# coding=utf-8
from distutils.core import setup
import py2exe

includes = ['sip']
data_files = ['main.py']
options = {
    "py2exe":
        {
            "includes": includes,
            "compressed": 1,
            "optimize": 2,
            "ascii": 0,
            "bundle_files": 1,
            "dll_excludes": ["MSVCP90.dll", "numpy-atlas.dll"]

        }
}

setup(version="1.0",
      description="Niubility Word",
      name='NiubilityWord',
      options=options,
      windows=data_files)

if __name__ == '__main__':
    # cmd :python setup.py py2exe
    pass

# coding=utf-8
from distutils.core import setup
import py2exe  # 必须要有，不然命令行编译不过

includes = []
data_files = ['main.py']
options = {
    "py2exe":
        {
            "includes": includes,
            "compressed": 1,
            "optimize": 2,
            "ascii": 0,
            # "bundle_files": 1, 64 位系统会有问题
            "dll_excludes": ["MSVCP90.dll", "numpy-atlas.dll", "w9xpopen.exe"]

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

from distutils.core import setup
import py2exe

setup(
    name='hogge',
    version='0.3',
    package_dir={'': 'src'},
    url='https://github.com/itghisi/hogge',
    license='LGPL v3.0',
    author='Igor Ghisi',
    author_email='igor.ghisi@gmail.com',
    description='',
    console=[{
        "dest_base": "hogge",
        "script": "hogge/main.py",
    }],
    zipfile = None,
    options={
        "py2exe": {"optimize": 2,
                   "compressed": True,
                   "excludes": "Tkinter",
                   "bundle_files": 0,
        }
    },
)

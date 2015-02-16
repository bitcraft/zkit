"""
Bitcraft's pyweek skellington setup.py


usage: python setup.py command

sdist - build a source dist
py2exe - build a windows exe
py2app - build an os x app

"""
try:
    import py2exe
except ImportError:
    pass

import sys
import glob
import os
import shutil


APP_NAME = 'zkit'
DESCRIPTION = open('README.txt').read()
CHANGES = open('CHANGES.txt').read()
TODO = open('TODO.txt').read()

METADATA = {
    'name': APP_NAME,
    'version': '0.0.1',
    'license': 'BSD License',
    'description': 'Zort the Explorer',
    'author': 'bitcraft, wkmanire, AlecksG',
    'url': 'https://github.com/bitcraft/pyweek19',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: pygame',
    ],

    'py2exe.target': '',
    # 'py2exe.icon':'icon.ico', #64x64
    'py2exe.binary': APP_NAME,

    'py2app.target': APP_NAME,
    #'py2app.icon': 'icon.icns',  # 128x128

    'cx_freeze.cmd': 'cxfreeze',
    'cx_freeze.target': APP_NAME,
    'cx_freeze.binary': APP_NAME,
}

files_to_remove = ['tk84.dll',
                   '_ssl.pyd',
                   'tcl84.dll',
                   os.path.join('numpy', 'core', '_dotblas.pyd'),
                   os.path.join('numpy', 'linalg', 'lapack_lite.pyd')]

directories_to_remove = [os.path.join('numpy', 'distutils'),
                         'distutils',
                         'tcl']

cmdclass = dict()
PACKAGEDATA = {
    'cmdclass': cmdclass,
    'package_dir': {'zkit': 'zkit'},
    'packages': ['zkit'],
    'scripts': ['scripts/zkit'],
}

PACKAGEDATA.update(METADATA)

try:
    cmd = sys.argv[1]
except IndexError:
    print('Usage: setup.py install|py2exe|py2app')
    raise SystemExit


# utility for adding subdirectories
def add_files(dest, generator):
    for dirpath, dirnames, filenames in generator:
        for name in 'CVS', '.svn':
            if name in dirnames:
                dirnames.remove(name)

        for name in filenames:
            if '~' in name: continue
            suffix = os.path.splitext(name)[1]
            if suffix in ('.pyc', '.pyo'): continue
            if name[0] == '.': continue
            filename = os.path.join(dirpath, name)
            dest.append(filename)

# define what is our data
_DATA_DIR = os.path.join('zkit', 'data')
data = list()
data_dirs = [os.path.join(f2.replace(_DATA_DIR, 'data'), '*') for f2 in data]
# PACKAGEDATA['package_data'] = {'zkit': data_dirs}
PACKAGEDATA['package_data'] = dict()

data.extend(glob.glob('*.txt'))
# data.append('MANIFEST.in')
# define what is our source
src = list()
add_files(src, os.walk('zkit'))
src.extend(glob.glob('*.py'))

# build the sdist target
if cmd not in "py2exe py2app cx_freeze".split():
    with open("MANIFEST.in", "w") as fh:
        for l in data:
            fh.write("include " + l + "\n")
        for l in src:
            fh.write("include " + l + "\n")
    setup(**PACKAGEDATA)

# build the py2exe target
if cmd == 'py2exe':
    from distutils.core import setup, Extension
    import numpy  # hack

    dist_dir = os.path.join('dist', METADATA['py2exe.target'])
    data_dir = dist_dir
    src = 'run_game.py'
    dest = METADATA['py2exe.binary'] + '.py'
    shutil.copy(src, dest)
    setup(
        options={'py2exe': {
            'dist_dir': dist_dir,
            'dll_excludes': ['_dotblas.pyd', '_numpy.pyd',
                             'numpy.linalg.lapack_lite.pyd',
                             'numpy.core._dotblas.pyd'] + files_to_remove,
            'excludes': ['matplotlib', 'tcl', 'OpenGL'],
            'ignores': ['matplotlib', 'tcl', 'OpenGL'],
            'bundle_files': 1,
            'optimize': 2,
            'compressed': True,
        }},
        console=[{
            'script': dest,
        }],
    )

# build windows cx_freeze
if cmd == 'cx_freeze':
    from cx_Freeze import setup, Executable

    exe = Executable(
        script="file.py",
        base="Win32Gui",
        icon="Icon.ico"
    )
    includefiles = list()
    includes = []
    excludes = ['matplotlib', 'tcl', 'OpenGL']
    packages = []
    setup(
        version="0.0",
        description="No Description",
        author="Name",
        name="App name",
        options={'build_exe': {
            'excludes': excludes,
            'include_files': includefiles
        }},
        executables=[exe]
    )

# build the py2app target
if cmd == 'py2app':
    from distutils.core import setup, Extension

    dist_dir = os.path.join('dist', METADATA['py2app.target'] + '.app')
    data_dir = os.path.join(dist_dir, 'Contents', 'Resources')
    from setuptools import setup

    src = 'run_game.py'
    dest = METADATA['py2app.target'] + '.py'
    shutil.copy(src, dest)

    APP = [dest]
    DATA_FILES = list()
    OPTIONS = {'argv_emulation': True,
               # 'iconfile':METADATA['py2app.icon']
    }

    setup(
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'])


# recursively make a bunch of folders
def make_dirs(dname_):
    parts = list(os.path.split(dname_))
    dname = None
    while len(parts):
        if dname is None:
            dname = parts.pop(0)
        else:
            dname = os.path.join(dname, parts.pop(0))
        if not os.path.isdir(dname):
            os.mkdir(dname)

# copy data into the binaries
if cmd in ('py2exe', 'py2app', 'cxfreeze'):
    dest = data_dir
    for fname in data:
        dname = os.path.join(dest, os.path.dirname(fname))
        make_dirs(dname)
        if not os.path.isdir(fname):
            shutil.copy(fname, dname)

# remove files from the zip.
if 0 and cmd == 'py2exe':
    os.system("unzip dist/library.zip -d dist\library")

    for fn in files_to_remove:
        os.remove(os.path.join('dist', 'library', fn))

    for d in directories_to_remove:
        if os.path.exists(os.path.join('dist', 'library', d)):
            shutil.rmtree(os.path.join('dist', 'library', d))

    os.remove(os.path.join('dist', 'library.zip'))
    os.chdir("dist")
    os.chdir("library")
    os.system("zip -r -9 ..\library.zip .")
    os.chdir("..")
    os.chdir("..")

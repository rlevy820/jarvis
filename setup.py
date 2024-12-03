from setuptools import setup

APP = ['jarvis.py']
DATA_FILES = []
OPTIONS = {
 'iconfile':'jarvisIconV3.icns',
 'argv_emulation': True,
 'packages': ['certifi'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
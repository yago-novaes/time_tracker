from setuptools import setup

APP = ['time_tracker_gui.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False, 
    'iconfile': 'app_icon.icns',  
    'includes': ['sip', 'PyQt5', 'cmath'],  
    'packages': ['pandas'],  
    'excludes': ['PyInstaller'], 
    'plist': {
        'CFBundleName': 'Time Tracker',
        'CFBundleDisplayName': 'Time Tracker',
        'CFBundleGetInfoString': 'Aplicativo de Rastreamento de Tempo',
        'CFBundleIdentifier': 'com.seuusuario.timetracker',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
    },
}

setup(
    app=APP,
    name='Time Tracker',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

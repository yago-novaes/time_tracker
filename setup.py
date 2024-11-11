from setuptools import setup

APP = ['time_tracker_gui.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,  # Desativar argv_emulation
    'iconfile': 'app_icon.icns',  # Opcional: adicionar um ícone personalizado se necessário
    'includes': ['sip', 'PyQt5', 'cmath'],  # Inclua apenas PyQt5 e SIP
    'packages': ['pandas'],  # Inclua apenas pandas como dependência essencial
    'excludes': ['PyInstaller'],  # Exclui o PyInstaller
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
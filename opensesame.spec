import glob
import os

block_cipher = None

# Función para expandir patrones de comodines
def expand_glob(pattern):
    files = []
    for file in glob.glob(pattern, recursive=True):
        # Asegúrate de que sea un archivo
        if os.path.isfile(file):
            # Mantén la estructura de directorios
            folder = os.path.dirname(file)
            files.append((file, folder))
        elif os.path.isdir(file):
            # Si es un directorio, también incluirlo (si es necesario)
            files.append((file, file))  # Incluye la carpeta en sí misma
    return files

binaries=[
    ('/usr/lib/x86_64-linux-gnu/libpython3.10.so', '_internal/libpython3.10.so'),
],

# Incluyendo las carpetas y archivos de manera adecuada
datas = [
    ('libqtopensesame/resources/theme/default/Faba/index.theme', 'libqtopensesame/resources/theme/default/Faba'),
    *expand_glob('libqtopensesame/resources/theme/default/Faba/*.png'),
    *expand_glob('libqtopensesame/resources/theme/default/Faba/**/*.png'),
    *expand_glob('openexp/resources/widgets/gray/*.png'),
    *expand_glob('openexp/resources/widgets/*.ogg'),
    ('libqtopensesame/resources/theme/default/MokaSesame/index.theme', 'libqtopensesame/resources/theme/default/MokaSesame'),
    *expand_glob('libqtopensesame/resources/theme/default/*.css'),
    *expand_glob('libqtopensesame/resources/theme/default/*.qss'),
    *expand_glob('libqtopensesame/resources/theme/default/*.csv'),
    *expand_glob('libqtopensesame/resources/theme/default/*.py'),
    *expand_glob('libqtopensesame/resources/theme/default/MokaSesame/*.png'),
    *expand_glob('libqtopensesame/resources/theme/*.png'),
    *expand_glob('libqtopensesame/resources/theme/default/MokaSesame/**/*.png'),
    *expand_glob('libqtopensesame/resources/theme/default/MokaSesame/**/*.svg'),
    *expand_glob('mime/*.svg'),
    *expand_glob('mime/*.desktop'),
    *expand_glob('libqtopensesame/*.gif'),
    *expand_glob('libqtopensesame/*.wav'),
    *expand_glob('libqtopensesame/widgets/*.wav'),
    *expand_glob('opensesame_extensions/core/get_started/*.wav'),
    *expand_glob('opensesame_extensions/core/get_started/*.gif'),
    *expand_glob('libqtopensesame/translations/*.qm'),
    *expand_glob('libqtopensesame/resources/ui/**/*.ui'),
]

hiddenimports = [
    'libqtopensesame.__main__',
    'libqtopensesame',
    'openexp',
    'libopensesame',
    'libqtopensesame',
    'opensesame_extensions',
    'opensesame_plugins',
    'qtpy',
    'pyqt5',
    'PyQt5-tools',
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
    'setuptools',
    'psutil',
    'qtawesome',
    'webcolors',
    'datamatrix',
    'qtconsole',
    'pyqode.core',
    'python-qnotifications',
    'pyqode.python',
    'qdatamatrix',
    'fastnumbers',
    'markdown',
    'pillow',
    'PyQtWebEngine'
]

a = Analysis(
    ['opensesame.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='opensesame',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='opensesame',
)

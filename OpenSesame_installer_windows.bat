@echo off

echo Instalando dependencias necesarias...

:: Verificar si Python y Git están instalados
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python no está instalado. Por favor, instala Python y vuelve a intentarlo.
    exit /b
)

where git >nul 2>&1
if %errorlevel% neq 0 (
    echo Git no está instalado. Por favor, instala Git y vuelve a intentarlo.
    exit /b
)

:: Crear un entorno virtual
python -m venv opensesame_env
call opensesame_env\Scripts\activate

:: Instalar las dependencias de Python
pip install ^
    libqtopensesame ^
    openexp ^
    libopensesame ^
    libqtopensesame ^
    opensesame_extensions ^
    opensesame_plugins ^
    qtpy ^
    pyqt5 ^
    PyQt5-tools ^
    PyQt5.QtCore ^
    PyQt5.QtGui ^
    PyQt5.QtWidgets ^
    setuptools ^
    psutil ^
    qtawesome ^
    webcolors ^
    datamatrix ^
    qtconsole ^
    pyqode.core ^
    python-qnotifications ^
    pyqode.python ^
    qdatamatrix ^
    fastnumbers ^
    markdown ^
    pillow ^
    PyQtWebEngine

echo Clonando el repositorio de OpenSesame...
:: Clonar el repositorio
git clone https://github.com/camilahinojosa26/OpenSesame/
cd OpenSesame || exit /b

:: Cambiar a la rama específica
git checkout Puzzle

echo Ejecutando OpenSesame...
:: Ejecutar el programa
set PYTHONPATH=opensesame.py
python opensesame.py

:: Desactivar el entorno virtual al finalizar
deactivate

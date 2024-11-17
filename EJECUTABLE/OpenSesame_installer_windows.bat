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

pip install qtpy PyQt5 PyQt5-sip PyYAML PyQt5-tools setuptools pseudorandom psutil qtawesome webcolors datamatrix qtconsole pyqode.core python-qnotifications pyqode.python qdatamatrix fastnumbers markdown pillow PyQtWebEngine

:: Verificar si hubo errores en la instalación de las dependencias
if %errorlevel% neq 0 (
    echo Error al instalar las dependencias.
    exit /b
)

echo Descargando OpenSesame...
:: Clonar el repositorio
git clone --branch cinematography https://github.com/camilahinojosa26/OpenSesame/

cd OpenSesame || (
    echo Error al acceder al descargar OpenSesame.
    exit /b
)

echo Ejecutando OpenSesame...
python opensesame.py

pause

echo Proceso completado.

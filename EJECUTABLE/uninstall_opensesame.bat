@echo off

echo Desinstalando OpenSesame y sus dependencias...

:: Verificar si el repositorio de OpenSesame existe y eliminarlo
if exist "OpenSesame" (
    echo Eliminando la carpeta de OpenSesame...
    rmdir /s /q OpenSesame
) else (
    echo No se encontró la carpeta de OpenSesame.
)

pip uninstall qtpy PyQt5 PyQt5-sip PyYAML PyQt5-tools setuptools psutil qtawesome webcolors datamatrix qtconsole pyqode.core python-qnotifications pyqode.python qdatamatrix fastnumbers PyQtWebEngine

:: Verificar si hubo errores en la desinstalacion de las dependencias
if %errorlevel% neq 0 (
    echo Error al desinstalar las dependencias.
    exit /b
)

echo OpenSesame y sus dependencias han sido desinstalados.

pause

#!/bin/bash

echo "Desinstalando OpenSesame y sus dependencias..."

# Desactivar entorno virtual si está activado
deactivate 2>/dev/null

# Eliminar el entorno virtual si existe
if [ -d "opensesame_env" ]; then
    echo "Eliminando el entorno virtual..."
    rm -rf opensesame_env
else
    echo "No se encontró el entorno virtual opensesame_env."
fi

# Eliminar el repositorio de OpenSesame si existe
if [ -d "OpenSesame" ]; then
    echo "Eliminando la carpeta del repositorio OpenSesame..."
    rm -rf OpenSesame
else
    echo "No se encontró la carpeta del repositorio OpenSesame."
fi

# Desinstalar las dependencias globales de Python
echo "Desinstalando dependencias de Python..."
pip uninstall -y qtawesome webcolors datamatrix qtconsole pyqode.core python-qnotifications pyqode.python qdatamatrix fastnumbers markdown pillow PyQtWebEngine

echo "OpenSesame y sus dependencias han sido desinstalados."

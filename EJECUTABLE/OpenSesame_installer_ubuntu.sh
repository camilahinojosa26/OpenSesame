#!/bin/bash

echo "Instalando dependencias necesarias..."

# Actualizar e instalar pip y git si no están presentes
sudo apt update
sudo apt install -y python3-pip git

# Crear y activar un entorno virtual
python3 -m venv opensesame_env
source opensesame_env/bin/activate

# Instalar dependencias de Python
pip install \
    libqtopensesame \
    openexp \
    libopensesame \
    libqtopensesame \
    opensesame_extensions \
    opensesame_plugins \
    qtpy \
    pyqt5 \
    PyQt5-tools \
    PyQt5.QtCore \
    PyQt5.QtGui \
    PyQt5.QtWidgets \
    setuptools \
    psutil \
    qtawesome \
    webcolors \
    datamatrix \
    qtconsole \
    pyqode.core \
    python-qnotifications \
    pyqode.python \
    qdatamatrix \
    fastnumbers \
    markdown \
    pillow \
    PyQtWebEngine

echo "Clonando el repositorio de OpenSesame..."
# Clonar el repositorio
git clone https://github.com/camilahinojosa26/OpenSesame/
cd OpenSesame || exit

# Cambiar a la rama específica
git checkout Puzzle

echo "Ejecutando OpenSesame..."
# Ejecutar el programa
PYTHONPATH=opensesame.py python3 opensesame.py

# Desactivar el entorno virtual al finalizar
deactivate

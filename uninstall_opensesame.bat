@echo off

echo Desinstalando OpenSesame y sus dependencias...

:: Verificar si el entorno virtual existe y eliminarlo
if exist "opensesame_env" (
    echo Eliminando el entorno virtual...
    rmdir /s /q opensesame_env
) else (
    echo No se encontró el entorno virtual opensesame_env.
)

:: Verificar si el repositorio de OpenSesame existe y eliminarlo
if exist "OpenSesame" (
    echo Eliminando la carpeta del repositorio OpenSesame...
    rmdir /s /q OpenSesame
) else (
    echo No se encontró la carpeta del repositorio OpenSesame.
)

echo OpenSesame y sus dependencias han sido desinstalados.

:: Pausar para que el usuario vea el mensaje final antes de cerrar
pause

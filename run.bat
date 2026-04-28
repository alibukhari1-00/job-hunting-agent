@echo off
set QGIS_ROOT=C:\Program Files\QGIS 3.34.3
set PYTHONHOME=%QGIS_ROOT%\apps\Python39
set PYTHONPATH=%QGIS_ROOT%\apps\Python39\Lib;%QGIS_ROOT%\apps\Python39\Lib\site-packages
set PATH=%QGIS_ROOT%\apps\Python39;%QGIS_ROOT%\apps\qt5\bin;%QGIS_ROOT%\bin;%PATH%
cd /d "%~dp0"
"%QGIS_ROOT%\apps\Python39\python.exe" validate.py

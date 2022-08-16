@echo off
pyinstaller main.py --onefile -w --icon=icons\icon.ico
cd ./dist
move ./*.exe ../
cd ..
rd /s /q __pycache__
rd /s /q build
rd /s /q dist
del /q main.spec
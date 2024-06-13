@echo off
set /p lib=Enter the library name to remove: 
pip uninstall -y %lib%
pip freeze > requirements.txt
echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
echo %lib% has been removed and requirements.txt has been updated.
echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

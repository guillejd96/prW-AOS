@echo off
:: Compile code
cd /d C:\Users\Guillermo\Desktop\Py_Folder\2025\oPA

:: Add Python Scripts directory to PATH (if not already in PATH)
set PATH=%PATH%;C:\Users\Guillermo\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts\

REM Run PyInstaller to create a standalone executable
pyinstaller opa.py --onefile --icon=icos\brand_warhammer_icon_158628.ico

REM Notify the user that the process is complete
echo Executable has been generated.

:: Create executable
:: C:\Users\Guillermo\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts\pyinstaller.exe --onefile oPA.py

:: cd C:\Users\Guillermo\Desktop\Py_Folder\2025\oPA\dist\

:: Create lnk in Desktop
SET TARGET_PATH=C:\Users\Guillermo\Desktop\Py_Folder\2025\oPA\dist\opA.exe
SET SHORTCUT_PATH=%USERPROFILE%\Desktop\oPA.lnk
powershell -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%SHORTCUT_PATH%'); $s.TargetPath='%TARGET_PATH%'; $s.Save()"
echo El valor de TARGET_PATH es: %TARGET_PATH%
echo El valor de SHORTCUT_PATH es: %SHORTCUT_PATH%

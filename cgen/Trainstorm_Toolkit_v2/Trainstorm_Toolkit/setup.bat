@echo off
title Trainstorm Toolkit - One-Time Setup
color 1F
setlocal

echo.
echo  =====================================================
echo   Trainstorm Toolkit - One-Time Setup
echo  =====================================================
echo.
echo  This will create a private Python environment inside
echo  this folder (called "venv") and install all required
echo  packages into it.
echo.
echo  Nothing outside this folder is changed. You only need
echo  to run this once.
echo.
pause

:: -------------------------------------------------------
:: Find a Python interpreter to bootstrap with.
:: The "py" launcher is the most reliable way to find the
:: real Python on Windows, even on machines with several
:: installs. We fall back to "python" only if py is absent.
:: -------------------------------------------------------
echo.
echo  Looking for Python...
echo.

set "BOOT_PY="

py -3 --version >nul 2>&1
if not errorlevel 1 (
    set "BOOT_PY=py -3"
    goto :found_python
)

python --version >nul 2>&1
if not errorlevel 1 (
    set "BOOT_PY=python"
    goto :found_python
)

echo  [ERROR] Python was not found on this machine.
echo.
echo  Please install Python from:
echo    https://www.python.org/downloads/
echo.
echo  IMPORTANT: During installation, check the box that
echo  says "Add Python to PATH" before clicking Install.
echo.
echo  After installing, close this window and run setup again.
echo.
pause
exit /b 1

:found_python
echo  Found Python. Checking version:
%BOOT_PY% --version
echo.

:: -------------------------------------------------------
:: Create the local venv (private environment).
:: After this step we NEVER use the system Python again --
:: every tool in this kit runs venv\Scripts\python.exe by
:: its full path, so messy machine setups can't break it.
:: -------------------------------------------------------
set "VENV_DIR=%~dp0venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"

if exist "%VENV_PY%" (
    echo  A private environment already exists. Reusing it.
    echo.
    goto :install_packages
)

echo  Creating private environment...
echo.
echo  Running: %BOOT_PY% -m venv "%VENV_DIR%"
echo.
%BOOT_PY% -m venv "%VENV_DIR%"

if not exist "%VENV_PY%" (
    echo.
    echo  [ERROR] The private environment was not created.
    echo  Check the messages above. Contact Jake if this continues.
    echo.
    pause
    exit /b 1
)

:install_packages
echo  Installing required packages into the private environment...
echo  (This may take a minute or two -- please wait)
echo.
echo  Running: venv\Scripts\python.exe -m pip install [packages]
echo.

"%VENV_PY%" -m pip install --quiet --disable-pip-version-check --upgrade pip

"%VENV_PY%" -m pip install --quiet --disable-pip-version-check ^
    python-pptx ^
    python-docx ^
    openpyxl ^
    pdfplumber ^
    pdf2image ^
    pytesseract ^
    lxml

if errorlevel 1 (
    echo.
    echo  [WARNING] One or more packages may not have installed correctly.
    echo.
    echo  If you are on a corporate network, a proxy may be blocking
    echo  the Python package index. Contact Jake.
    echo.
    pause
    exit /b 1
)

:: -------------------------------------------------------
:: Verify the environment actually works.
:: -------------------------------------------------------
echo  Verifying the environment...
echo.
"%VENV_PY%" -c "import pptx, docx, openpyxl, pdfplumber, lxml; print('  All core packages: OK')"
if errorlevel 1 (
    echo.
    echo  [ERROR] Verification failed. Contact Jake.
    echo.
    pause
    exit /b 1
)

echo.
echo  Checking for Tesseract OCR...
where tesseract >nul 2>&1
if errorlevel 1 (
    echo  Tesseract not found -- this is OK.
    echo  It is only needed for scanned PDFs.
) else (
    echo  Tesseract OCR: Found
)

echo.
echo  =====================================================
echo   Setup complete!
echo.
echo   This toolkit now has its own private Python in the
echo   "venv" folder. Every tool here uses it automatically.
echo.
echo   You can now double-click any of the tool .bat files:
echo     cgen_build.bat       - build a project context file
echo     matrix_extract.bat   - pull a translation matrix to Excel
echo     matrix_reinject.bat  - put translations back into Word
echo  =====================================================
echo.
pause

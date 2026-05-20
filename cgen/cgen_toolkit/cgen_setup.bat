@echo off
title Trainstorm CGEN - One-Time Setup
color 1F

echo.
echo  =====================================================
echo   Trainstorm CGEN Toolkit - One-Time Setup
echo  =====================================================
echo.
echo  This will check your Python installation and install
echo  all required packages. This only needs to run once.
echo.
pause

:: -------------------------------------------------------
:: Check Python
:: -------------------------------------------------------
echo.
echo  Checking for Python...
echo.

python --version
if errorlevel 1 (
    echo.
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
)

echo.
echo  Python found. Installing required packages...
echo  (This may take a minute or two -- please wait)
echo.

:: -------------------------------------------------------
:: Install packages via python -m pip (safer on managed machines)
:: -------------------------------------------------------
python -m pip install --quiet --disable-pip-version-check ^
    python-pptx ^
    python-docx ^
    openpyxl ^
    pdfplumber ^
    pdf2image ^
    pytesseract

if errorlevel 1 (
    echo.
    echo  [WARNING] One or more packages may not have installed correctly.
    echo.
    echo  If you saw a permissions error, try right-clicking cgen_setup.bat
    echo  and selecting "Run as administrator", then run it again.
    echo.
    echo  If that doesn't work, contact Jake.
    echo.
    pause
    exit /b 1
)

echo.
echo  Checking for Tesseract OCR...
where tesseract >nul 2>&1
if errorlevel 1 (
    echo  Tesseract not found -- this is OK.
    echo  Tesseract is only needed for scanned PDFs.
    echo  Regular Word docs, PowerPoints, Excel and PDFs work without it.
) else (
    echo  Tesseract OCR: Found
)

echo.
echo  =====================================================
echo   Setup complete!
echo.
echo   You can now double-click cgen_build.bat to run the
echo   pipeline whenever you need it.
echo  =====================================================
echo.
pause

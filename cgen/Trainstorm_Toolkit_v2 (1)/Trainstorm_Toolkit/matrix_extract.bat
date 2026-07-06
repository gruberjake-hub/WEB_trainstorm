@echo off
title Trainstorm Toolkit - Matrix Extract
color 1F
setlocal

echo.
echo  =====================================================
echo   Trainstorm Toolkit - Translation Matrix Extract
echo   (Storyline matrix .docx  -^>  translation job folder)
echo  =====================================================
echo.

set "VENV_PY=%~dp0venv\Scripts\python.exe"
set "SCRIPTS_DIR=%~dp0scripts"
set "TMPFILE=%TEMP%\trainstorm_pick_%RANDOM%.txt"

if not exist "%VENV_PY%" (
    echo  [ERROR] The private Python environment was not found.
    echo.
    echo  Please run setup.bat first. You only need to do it once.
    echo.
    pause
    exit /b 1
)

if not exist "%SCRIPTS_DIR%\matrix_extract.py" (
    echo  [ERROR] scripts\matrix_extract.py was not found.
    echo  Contact Jake.
    echo.
    pause
    exit /b 1
)

:: -------------------------------------------------------
:: Pick the Storyline translation matrix (.docx)
:: Write result to a temp file to avoid for/f quoting issues
:: -------------------------------------------------------
echo  Step 1: choose the Storyline translation matrix (.docx)
echo          exactly as exported from Storyline.
echo.

"%VENV_PY%" "%SCRIPTS_DIR%\pick_file.py" "Select the Storyline translation matrix (.docx)" "docx" > "%TMPFILE%" 2>&1
set /p MATRIX_PATH=<"%TMPFILE%"
del "%TMPFILE%" 2>nul

if /i "%MATRIX_PATH%"=="CANCELLED" (
    echo  No file selected. Exiting.
    echo.
    pause
    exit /b 0
)

if not defined MATRIX_PATH (
    echo  [ERROR] File picker returned no path.
    echo  Contact Jake.
    echo.
    pause
    exit /b 1
)

if not exist "%MATRIX_PATH%" (
    echo  [ERROR] The selected file does not exist:
    echo    %MATRIX_PATH%
    echo.
    pause
    exit /b 1
)

echo  Selected matrix:
echo    %MATRIX_PATH%
echo.

:: -------------------------------------------------------
:: Ask for the target language
:: -------------------------------------------------------
set "TARGET_LANG="
set /p TARGET_LANG= Step 2: type the target language (e.g. Japanese): 

if not defined TARGET_LANG (
    echo  [ERROR] No language entered. Exiting.
    echo.
    pause
    exit /b 1
)

echo.

:: -------------------------------------------------------
:: Run the extractor
:: -------------------------------------------------------
echo  Running: venv\Scripts\python.exe scripts\matrix_extract.py
echo           --input "%MATRIX_PATH%"
echo           --language "%TARGET_LANG%"
echo.

"%VENV_PY%" "%SCRIPTS_DIR%\matrix_extract.py" ^
    --input "%MATRIX_PATH%" ^
    --language "%TARGET_LANG%"

if errorlevel 1 (
    echo.
    echo  [ERROR] Extraction failed. Check the messages above.
    echo  If a structure_report.txt was created, send it to Jake.
    echo.
    pause
    exit /b 1
)

echo.
echo  A translation job folder was created next to the matrix.
echo  Open INSTRUCTIONS.txt inside it and follow the steps.
echo.
pause

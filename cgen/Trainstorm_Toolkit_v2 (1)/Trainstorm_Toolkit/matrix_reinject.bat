@echo off
title Trainstorm Toolkit - Matrix Reinject
color 1F
setlocal

echo.
echo  =====================================================
echo   Trainstorm Toolkit - Translation Matrix Reinject
echo   (translation job  -^>  new translated matrix .docx)
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

if not exist "%SCRIPTS_DIR%\matrix_reinject.py" (
    echo  [ERROR] scripts\matrix_reinject.py was not found.
    echo  Contact Jake.
    echo.
    pause
    exit /b 1
)

:: -------------------------------------------------------
:: Pick the ORIGINAL matrix docx
:: -------------------------------------------------------
echo  Step 1: choose the ORIGINAL Storyline matrix (.docx) --
echo          the exact file you ran Matrix Extract on.
echo.

"%VENV_PY%" "%SCRIPTS_DIR%\pick_file.py" "Select the ORIGINAL Storyline matrix (.docx)" "docx" > "%TMPFILE%" 2>&1
set /p MATRIX_PATH=<"%TMPFILE%"
del "%TMPFILE%" 2>nul

if /i "%MATRIX_PATH%"=="CANCELLED" (
    echo  No file selected. Exiting.
    echo.
    pause
    exit /b 0
)

if not defined MATRIX_PATH (
    echo  [ERROR] File picker returned no path. Contact Jake.
    echo.
    pause
    exit /b 1
)

echo  Original matrix:
echo    %MATRIX_PATH%
echo.

:: -------------------------------------------------------
:: Pick the translation job folder
:: -------------------------------------------------------
echo  Step 2: choose the translation job folder (the folder
echo          Matrix Extract created, with your AI answers
echo          saved in its "2_translated" subfolder).
echo.

set "TMPFILE2=%TEMP%\trainstorm_pick_%RANDOM%.txt"
"%VENV_PY%" "%SCRIPTS_DIR%\pick_folder.py" "Select the translation job folder" > "%TMPFILE2%" 2>&1
set /p JOB_PATH=<"%TMPFILE2%"
del "%TMPFILE2%" 2>nul

if /i "%JOB_PATH%"=="CANCELLED" (
    echo  No folder selected. Exiting.
    echo.
    pause
    exit /b 0
)

if not defined JOB_PATH (
    echo  [ERROR] Folder picker returned no path. Contact Jake.
    echo.
    pause
    exit /b 1
)

echo  Job folder:
echo    %JOB_PATH%
echo.

:: -------------------------------------------------------
:: Validate + inject
:: -------------------------------------------------------
echo  Running: venv\Scripts\python.exe scripts\matrix_reinject.py
echo           --matrix "%MATRIX_PATH%"
echo           --job "%JOB_PATH%"
echo.

"%VENV_PY%" "%SCRIPTS_DIR%\matrix_reinject.py" ^
    --matrix "%MATRIX_PATH%" ^
    --job "%JOB_PATH%"

if errorlevel 2 goto :incomplete
if errorlevel 1 (
    echo.
    echo  [ERROR] Reinjection failed. Check the messages above.
    echo  Contact Jake if this continues.
    echo.
    pause
    exit /b 1
)

echo.
echo  Done. A new translated copy of the matrix was saved next
echo  to the original. The original was not modified. Import the
echo  new copy into Storyline.
echo.
pause
exit /b 0

:incomplete
echo.
echo  Some segments are missing or invalid (see coverage_report.txt
echo  in the job folder). The normal fix: re-run the affected packets
echo  in Copilot, save the answers into "2_translated", and run this
echo  tool again.
echo.
set /p PARTIAL= Write a PARTIAL copy anyway (untranslated text stays English)? (Y/N): 
if /i not "%PARTIAL%"=="Y" (
    echo.
    echo  Nothing was written. Re-run when the gaps are filled.
    echo.
    pause
    exit /b 0
)

echo.
echo  Running: venv\Scripts\python.exe scripts\matrix_reinject.py
echo           --matrix "%MATRIX_PATH%"
echo           --job "%JOB_PATH%"
echo           --allow-partial
echo.

"%VENV_PY%" "%SCRIPTS_DIR%\matrix_reinject.py" ^
    --matrix "%MATRIX_PATH%" ^
    --job "%JOB_PATH%" ^
    --allow-partial

echo.
pause

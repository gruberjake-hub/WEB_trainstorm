@echo off
title CGEN - Build Pipeline [DEBUG MODE]
color 4F

echo.
echo  =====================================================
echo   CGEN Context Builder - DEBUG MODE
echo   Window will pause after every step.
echo   Screenshot or copy any errors you see.
echo  =====================================================
echo.
pause

:: -------------------------------------------------------
:: STEP D1: Show where this bat file is running from
:: -------------------------------------------------------
echo.
echo  [D1] Bat file location:
echo    %~dp0
echo.
echo  [D1] Scripts directory will be:
echo    %~dp0scripts
echo.
pause

:: -------------------------------------------------------
:: STEP D2: Check scripts folder exists
:: -------------------------------------------------------
set "SCRIPTS_DIR=%~dp0scripts"

echo  [D2] Checking for scripts folder...
if exist "%SCRIPTS_DIR%" (
    echo   OK: scripts folder found
) else (
    echo   FAIL: scripts folder not found at:
    echo     %SCRIPTS_DIR%
)
echo.
pause

:: -------------------------------------------------------
:: STEP D3: Check each expected script file
:: -------------------------------------------------------
echo  [D3] Checking for individual script files...
echo.

if exist "%SCRIPTS_DIR%\file_to_structured_all_md.py" (
    echo   OK: file_to_structured_all_md.py
) else (
    echo   MISSING: file_to_structured_all_md.py
)

if exist "%SCRIPTS_DIR%\merge_project_context_hardened.py" (
    echo   OK: merge_project_context_hardened.py
) else (
    echo   MISSING: merge_project_context_hardened.py
)

if exist "%SCRIPTS_DIR%\pick_folder.py" (
    echo   OK: pick_folder.py
) else (
    echo   MISSING: pick_folder.py
)

if exist "%SCRIPTS_DIR%\find_latest_dir.py" (
    echo   OK: find_latest_dir.py
) else (
    echo   MISSING: find_latest_dir.py
)

echo.
pause

:: -------------------------------------------------------
:: STEP D4: Check Python
:: -------------------------------------------------------
echo  [D4] Checking Python...
echo.

where python
echo.
python --version
echo.

if errorlevel 1 (
    echo   FAIL: Python not found or returned an error.
    echo   This is likely the problem on this machine.
    echo   See notes below.
    echo.
    echo   On developer machines, Python is often managed by
    echo   conda, pyenv, or a virtual environment and is NOT
    echo   on the system PATH for bat files.
    echo.
    echo   Try running this from your IDE terminal instead,
    echo   or contact Jake with a screenshot of this screen.
) else (
    echo   OK: Python found
)
echo.
pause

:: -------------------------------------------------------
:: STEP D5: Check pip
:: -------------------------------------------------------
echo  [D5] Checking pip (via python -m pip)...
echo.
python -m pip --version
echo.
if errorlevel 1 (
    echo   FAIL: pip not available under this Python.
) else (
    echo   OK: pip found
)
echo.
pause

:: -------------------------------------------------------
:: STEP D6: Check key packages are importable
:: -------------------------------------------------------
echo  [D6] Checking required packages...
echo.

python -c "import pptx; print('  OK: python-pptx')"
python -c "import docx; print('  OK: python-docx')"
python -c "import openpyxl; print('  OK: openpyxl')"
python -c "import pdfplumber; print('  OK: pdfplumber')"
python -c "import tkinter; print('  OK: tkinter')"

echo.
pause

:: -------------------------------------------------------
:: STEP D7: Open folder picker
:: -------------------------------------------------------
echo  [D7] Launching folder picker (pick_folder.py)...
echo.

set "TEMP_PATH_FILE=%TEMP%\cgen_selected_path.txt"

python "%SCRIPTS_DIR%\pick_folder.py" > "%TEMP_PATH_FILE%" 2>&1
set "PICKER_EXIT=%ERRORLEVEL%"
set /p PROJECT_PATH=<"%TEMP_PATH_FILE%"

echo  Picker exit code: %PICKER_EXIT%
echo  Raw value returned: %PROJECT_PATH%
echo.

if "%PROJECT_PATH%"=="CANCELLED" (
    echo  No folder selected. Exiting.
    pause
    exit /b 0
)

if not defined PROJECT_PATH (
    echo  FAIL: No path returned from picker.
    pause
    exit /b 1
)

if not exist "%PROJECT_PATH%" (
    echo  FAIL: Returned path does not exist on disk:
    echo    %PROJECT_PATH%
    pause
    exit /b 1
)

echo  OK: Project folder selected and verified:
echo    %PROJECT_PATH%
echo.
pause

:: -------------------------------------------------------
:: STEP D8: Run converter (Step 1)
:: -------------------------------------------------------
echo  [D8] Running file_to_structured_all_md.py...
echo.

set "OUTPUT_BASE=%PROJECT_PATH%\output"

python "%SCRIPTS_DIR%\file_to_structured_all_md.py" ^
    --input "%PROJECT_PATH%" ^
    --output "%OUTPUT_BASE%"

echo.
echo  Converter exit code: %ERRORLEVEL%
echo.

if errorlevel 1 (
    echo  FAIL: Converter returned an error. See output above.
) else (
    echo  OK: Converter finished.
)
echo.
pause

:: -------------------------------------------------------
:: STEP D9: Find timestamped output folder
:: -------------------------------------------------------
echo  [D9] Locating timestamped output folder...
echo.

set "TEMP_DIR_FILE=%TEMP%\cgen_output_dir.txt"

python "%SCRIPTS_DIR%\find_latest_dir.py" "%OUTPUT_BASE%" > "%TEMP_DIR_FILE%" 2>&1
set /p TIMESTAMP_DIR=<"%TEMP_DIR_FILE%"
del "%TEMP_DIR_FILE%" 2>nul

echo  find_latest_dir.py returned: %TIMESTAMP_DIR%
echo.

if "%TIMESTAMP_DIR%"=="NOT_FOUND" (
    echo  FAIL: No output subfolders found. Converter may have
    echo  found no supported files in the selected folder.
    pause
    exit /b 1
)

if not defined TIMESTAMP_DIR (
    echo  FAIL: TIMESTAMP_DIR is empty.
    pause
    exit /b 1
)

echo  OK: Timestamped folder located:
echo    %TIMESTAMP_DIR%
echo.
pause

:: -------------------------------------------------------
:: STEP D10: Run merge (Step 2)
:: -------------------------------------------------------
echo  [D10] Running merge_project_context_hardened.py...
echo.

python "%SCRIPTS_DIR%\merge_project_context_hardened.py" ^
    --input "%TIMESTAMP_DIR%" ^
    --output "%TIMESTAMP_DIR%" ^
    --no-timestamp

echo.
echo  Merge exit code: %ERRORLEVEL%
echo.

if errorlevel 1 (
    echo  FAIL: Merge returned an error. See output above.
) else (
    echo  OK: Merge finished.
)
echo.
pause

:: -------------------------------------------------------
:: Done
:: -------------------------------------------------------
echo.
echo  =====================================================
echo   DEBUG RUN COMPLETE
echo.
echo   Output folder:
echo     %TIMESTAMP_DIR%
echo.
echo   File to use:
echo     project_context.md
echo  =====================================================
echo.

set /p OPEN_FOLDER= Open output folder in Explorer? (Y/N): 
if /i "%OPEN_FOLDER%"=="Y" start explorer "%TIMESTAMP_DIR%"

echo.
pause

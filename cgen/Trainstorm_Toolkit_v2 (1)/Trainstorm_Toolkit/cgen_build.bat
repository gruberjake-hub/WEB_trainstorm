@echo off
title Trainstorm Toolkit - Context Builder
color 1F
setlocal

echo.
echo  =====================================================
echo   Trainstorm Toolkit - Context Builder
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

if not exist "%SCRIPTS_DIR%\file_to_structured_all_md.py" (
    echo  [ERROR] Cannot find the scripts folder.
    echo.
    pause
    exit /b 1
)

:: -------------------------------------------------------
:: Open folder picker - write result to temp file
:: -------------------------------------------------------
echo  Opening folder selector...
echo  Please choose your project folder in the dialog that appears.
echo.

"%VENV_PY%" "%SCRIPTS_DIR%\pick_folder.py" > "%TMPFILE%" 2>&1
set /p PROJECT_PATH=<"%TMPFILE%"
del "%TMPFILE%" 2>nul

if /i "%PROJECT_PATH%"=="CANCELLED" (
    echo  No folder selected. Exiting.
    echo.
    pause
    exit /b 0
)

if not defined PROJECT_PATH (
    echo  [ERROR] Folder picker returned no path.
    echo.
    pause
    exit /b 1
)

if not exist "%PROJECT_PATH%" (
    echo  [ERROR] The selected path does not exist:
    echo    %PROJECT_PATH%
    echo.
    pause
    exit /b 1
)

echo  Selected folder:
echo    %PROJECT_PATH%
echo.

:: -------------------------------------------------------
:: Step 1: Convert files to structured Markdown
:: -------------------------------------------------------
set "OUTPUT_BASE=%PROJECT_PATH%\output"

echo  -------------------------------------------------------
echo  Step 1 of 2: Converting files to structured Markdown...
echo  -------------------------------------------------------
echo.
echo  Running: venv\Scripts\python.exe scripts\file_to_structured_all_md.py
echo           --input "%PROJECT_PATH%"
echo           --output "%OUTPUT_BASE%"
echo.

"%VENV_PY%" "%SCRIPTS_DIR%\file_to_structured_all_md.py" ^
    --input "%PROJECT_PATH%" ^
    --output "%OUTPUT_BASE%"

if errorlevel 1 (
    echo.
    echo  [ERROR] Step 1 failed.
    echo  Check the messages above. Contact Jake if this continues.
    echo.
    pause
    exit /b 1
)

:: -------------------------------------------------------
:: Find the timestamped subfolder Step 1 just created
:: -------------------------------------------------------
set "TMPFILE2=%TEMP%\trainstorm_latest_%RANDOM%.txt"
"%VENV_PY%" "%SCRIPTS_DIR%\latest_subdir.py" "%OUTPUT_BASE%" > "%TMPFILE2%" 2>&1
set /p TIMESTAMP_DIR=<"%TMPFILE2%"
del "%TMPFILE2%" 2>nul

if not defined TIMESTAMP_DIR (
    echo.
    echo  [ERROR] Could not find the output folder from Step 1.
    echo  Step 1 may have found no supported files in your project folder.
    echo.
    echo  Supported file types: .pptx  .docx  .xlsx  .xlsm  .pdf  .txt  .md
    echo.
    pause
    exit /b 1
)

echo.
echo  Conversion output folder:
echo    %TIMESTAMP_DIR%
echo.

:: -------------------------------------------------------
:: Step 2: Merge into project_context.md
:: -------------------------------------------------------
echo  -------------------------------------------------------
echo  Step 2 of 2: Merging into project_context.md...
echo  -------------------------------------------------------
echo.
echo  Running: venv\Scripts\python.exe scripts\merge_project_context_hardened.py
echo           --input "%TIMESTAMP_DIR%"
echo           --output "%TIMESTAMP_DIR%"
echo           --no-timestamp
echo.

"%VENV_PY%" "%SCRIPTS_DIR%\merge_project_context_hardened.py" ^
    --input "%TIMESTAMP_DIR%" ^
    --output "%TIMESTAMP_DIR%" ^
    --no-timestamp

if errorlevel 1 (
    echo.
    echo  [ERROR] Step 2 failed.
    echo  Check the messages above. Contact Jake if this continues.
    echo.
    pause
    exit /b 1
)

:: -------------------------------------------------------
:: Done
:: -------------------------------------------------------
echo.
echo  =====================================================
echo   Done! Your context file is ready.
echo.
echo   Folder:
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

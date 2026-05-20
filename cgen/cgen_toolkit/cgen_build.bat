@echo off
title Trainstorm CGEN - Build Pipeline
color 1F

echo.
echo  =====================================================
echo   Trainstorm CGEN - Context Builder
echo  =====================================================
echo.

:: -------------------------------------------------------
:: Locate scripts relative to this bat file
:: %~dp0 always gives the folder this bat file lives in
:: -------------------------------------------------------
set "SCRIPTS_DIR=%~dp0scripts"

if not exist "%SCRIPTS_DIR%\file_to_structured_all_md.py" (
    echo  [ERROR] Cannot find the CGEN scripts folder.
    echo.
    echo  Make sure this bat file is in the same folder as
    echo  the "scripts" subfolder containing the Python files.
    echo.
    echo  Expected location:
    echo    %SCRIPTS_DIR%\file_to_structured_all_md.py
    echo.
    pause
    exit /b 1
)

:: -------------------------------------------------------
:: Check Python
:: -------------------------------------------------------
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found.
    echo  Please run cgen_setup.bat first.
    echo.
    pause
    exit /b 1
)

:: -------------------------------------------------------
:: Open folder picker
:: Output is written to a temp file to avoid for/f quoting
:: issues with spaces in paths
:: -------------------------------------------------------
echo  Opening folder selector...
echo  Please choose your project folder in the dialog that appears.
echo.

set "TEMP_PATH_FILE=%TEMP%\cgen_selected_path.txt"

python "%SCRIPTS_DIR%\pick_folder.py" > "%TEMP_PATH_FILE%" 2>&1
set /p PROJECT_PATH=<"%TEMP_PATH_FILE%"
del "%TEMP_PATH_FILE%" 2>nul

if "%PROJECT_PATH%"=="CANCELLED" (
    echo  No folder selected. Exiting.
    echo.
    pause
    exit /b 0
)

if not defined PROJECT_PATH (
    echo  [ERROR] Folder picker did not return a path.
    echo  Contact Jake if this continues.
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

python "%SCRIPTS_DIR%\file_to_structured_all_md.py" ^
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
:: Again using a temp file to avoid for/f quoting issues
:: -------------------------------------------------------
set "TEMP_DIR_FILE=%TEMP%\cgen_output_dir.txt"

python "%SCRIPTS_DIR%\find_latest_dir.py" "%OUTPUT_BASE%" > "%TEMP_DIR_FILE%" 2>&1
set /p TIMESTAMP_DIR=<"%TEMP_DIR_FILE%"
del "%TEMP_DIR_FILE%" 2>nul

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

if "%TIMESTAMP_DIR%"=="NOT_FOUND" (
    echo.
    echo  [ERROR] No output subfolders found after Step 1.
    echo  Your project folder may contain no supported files.
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

python "%SCRIPTS_DIR%\merge_project_context_hardened.py" ^
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

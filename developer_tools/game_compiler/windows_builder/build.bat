@echo off
setlocal


:: === Dynamically find project root by looking for main.py ===
set ROOT_DIR=%CD%
:search_root
if exist "%ROOT_DIR%\main.py" (
    echo [INFO] Project root found at: %ROOT_DIR%
    goto :root_found
)
cd ..
set ROOT_DIR=%CD%
if "%ROOT_DIR%"=="%SystemDrive%\" (
    echo [ERROR] Could not find main.py. Make sure the script is within the project tree.
    pause
    exit /b 1
)
goto search_root

:root_found
set MAIN_SCRIPT=%ROOT_DIR%\main.py
set ASSETS_FOLDER=%ROOT_DIR%\assets
set OUTPUT_NAME=BASILISK_PROTOCOL

echo.
echo [BASILISK_BUILD] Running from inside 'dist\'...
echo.

REM === Find PyInstaller ===
echo [INFO] Searching for PyInstaller...

REM Try common locations
set PYINSTALLER_EXE=
where pyinstaller >nul 2>&1
if %errorlevel%==0 (
    set PYINSTALLER_EXE=pyinstaller
    echo [INFO] Found PyInstaller in system PATH
    goto :found_pyinstaller
)

REM Check Windows Store Python location
set STORE_PATH=%LocalAppData%\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts\pyinstaller.exe
if exist "%STORE_PATH%" (
    set PYINSTALLER_EXE=%STORE_PATH%
    echo [INFO] Found PyInstaller in Windows Store Python location
    goto :found_pyinstaller
)

REM Check regular Python installation
set REGULAR_PATH=%LocalAppData%\Programs\Python\Python311\Scripts\pyinstaller.exe
if exist "%REGULAR_PATH%" (
    set PYINSTALLER_EXE=%REGULAR_PATH%
    echo [INFO] Found PyInstaller in regular Python installation
    goto :found_pyinstaller
)

REM Check if it's in Scripts folder in PATH
set SCRIPTS_PATH=%USERPROFILE%\AppData\Local\Programs\Python\Python311\Scripts\pyinstaller.exe
if exist "%SCRIPTS_PATH%" (
    set PYINSTALLER_EXE=%SCRIPTS_PATH%
    echo [INFO] Found PyInstaller in user Scripts folder
    goto :found_pyinstaller
)

REM PyInstaller not found
echo [ERROR] PyInstaller not found in any common locations.
echo.
echo Please install PyInstaller using one of these methods:
echo   pip install pyinstaller
echo   python -m pip install pyinstaller
echo.
echo Or make sure it's accessible in your PATH.
pause
exit /b 1

:found_pyinstaller

REM === Check if main script exists ===
if not exist "%MAIN_SCRIPT%" (
    echo [ERROR] Main script not found: %MAIN_SCRIPT%
    echo Make sure you're running this from the 'dist' folder with main.py in the parent directory.
    pause
    exit /b 1
)

REM === Clean previous output ===
echo [INFO] Cleaning previous build output...
if exist "..\build" rmdir /s /q "..\build" >nul 2>&1
if exist "..\%OUTPUT_NAME%.spec" del /q "..\%OUTPUT_NAME%.spec" >nul 2>&1
if exist "%OUTPUT_NAME%.spec" del /q "%OUTPUT_NAME%.spec" >nul 2>&1
if exist "%OUTPUT_NAME%.exe" del /q "%OUTPUT_NAME%.exe" >nul 2>&1

REM === Build with PyInstaller ===
echo [INFO] Building "%OUTPUT_NAME%.exe" into current directory...
if exist "%ASSETS_FOLDER%" (
    echo [INFO] Including assets folder: %ASSETS_FOLDER%
    "%PYINSTALLER_EXE%" --onefile --noconsole --name "%OUTPUT_NAME%" ^
        --distpath . ^
        --workpath ..\build ^
        --add-data "%ASSETS_FOLDER%;assets" ^
        "%MAIN_SCRIPT%"
) else (
    echo [INFO] No assets folder found, building without assets
    "%PYINSTALLER_EXE%" --onefile --noconsole --name "%OUTPUT_NAME%" ^
        --distpath . ^
        --workpath ..\build ^
        "%MAIN_SCRIPT%"
)

if %errorlevel% neq 0 (
    echo [ERROR] PyInstaller build failed!
    pause
    exit /b 1
)

REM === Post-Build Cleanup ===
echo [INFO] Cleaning temporary files...
if exist "..\build" rmdir /s /q "..\build" >nul 2>&1
if exist "..\%OUTPUT_NAME%.spec" del /q "..\%OUTPUT_NAME%.spec" >nul 2>&1
if exist "%OUTPUT_NAME%.spec" del /q "%OUTPUT_NAME%.spec" >nul 2>&1

echo.
if exist "%OUTPUT_NAME%.exe" (
    echo [SUCCESS] Build complete! "%OUTPUT_NAME%.exe" created successfully.
) else (
    echo [ERROR] Build may have failed - executable not found.
)
echo.
pause
# SPYHVER-17: HARVESTING

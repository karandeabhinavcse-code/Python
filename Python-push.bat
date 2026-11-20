
@echo off
setlocal

cd /d "D:\Python Under Gaurav Sir"

if errorlevel 1 (
    echo ERROR: Python folder not found!
    pause
    exit /b 1
)

echo.
echo ===== PYTHON PRACTICE =====
echo.

:: Automatically trust this repository if not already trusted
git config --global --get-all safe.directory | findstr /I /X /C:"%CD%" >nul
if errorlevel 1 (
    git config --global --add safe.directory "%CD%"
    if errorlevel 1 goto error
)

:: Check Git repository
git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
    echo ERROR: This folder is not a Git repository!
    echo Make sure Git is initialized in this folder.
    pause
    exit /b 1
)

:: Stage all changes
git add .
if errorlevel 1 goto error

:: Check for changes
git diff --cached --quiet
set "DIFF_RESULT=%ERRORLEVEL%"

if "%DIFF_RESULT%"=="0" (
    echo No changes to push.
    pause
    exit /b 0
)

if not "%DIFF_RESULT%"=="1" goto error

:: Commit and push
git commit -m "Daily Python practice"
if errorlevel 1 goto error

git push
if errorlevel 1 goto error

echo.
echo ===== PYTHON PUSH COMPLETE =====
pause
exit /b 0

:error
echo.
echo ===== ERROR: PYTHON PUSH FAILED =====
echo Please check the Git error above.
pause
exit /b 1

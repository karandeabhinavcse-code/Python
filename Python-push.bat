
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

:: Check Git repository
git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
    echo ERROR: This is not a Git repository!
    pause
    exit /b 1
)

:: Ensure correct GitHub remote
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    git remote add origin https://github.com/karandeabhinavcse-code/Python.git
) else (
    git remote set-url origin https://github.com/karandeabhinavcse-code/Python.git
)
if errorlevel 1 goto error

:: Ensure main branch
git branch -M main
if errorlevel 1 goto error

:: Stage changes
git add .
if errorlevel 1 goto error

:: Check for changes
git diff --cached --quiet
set "DIFF_RESULT=%ERRORLEVEL%"

if "%DIFF_RESULT%"=="1" goto commit_changes
if not "%DIFF_RESULT%"=="0" goto error

goto sync_github

:commit_changes
git commit -m "Daily Python practice"
if errorlevel 1 goto error

:sync_github
:: Synchronize with GitHub
git pull --rebase origin main
if errorlevel 1 goto error

:: Push to GitHub
git push -u origin main
if errorlevel 1 goto error

echo.
echo ===== PYTHON PUSH COMPLETE =====
echo.
pause
exit /b 0

:error
echo.
echo ===== ERROR: PYTHON PUSH FAILED =====
echo Please check the Git error above.
pause
exit /b 1

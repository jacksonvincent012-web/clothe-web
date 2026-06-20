@echo off
title SHINNERS - Fashion Store
cd /d "%~dp0"

echo ===========================================
echo     SHINNERS - Premium Fashion Platform
echo ===========================================
echo.

echo [1/3] Installing Python dependencies...
cd backend-python
pip install -r requirements.txt > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    pip install flask flask-cors requests > nul 2>&1
)
cd ..
echo   Done!

echo [2/3] Starting Java Cart Service...
start "Java Cart Service" cmd /c "cd backend-java && javac CartServer.java -d . 2>nul && java CartServer"
echo   Java Cart Service starting on port 8081...

echo [3/3] Starting Python Backend...
start "Python Backend" cmd /c "cd backend-python && python app.py"
echo   Python backend starting on port 5000...

echo.
echo ===========================================
echo  All services starting!
echo  Frontend: file:///%~dp0frontend/index.html
echo  Python API: http://localhost:5000
echo  Java Cart: http://localhost:8081
echo ===========================================
echo.
echo  NOTE: Open the frontend/index.html in your browser
echo  Make sure Java JDK and Python 3 are installed
echo.
pause

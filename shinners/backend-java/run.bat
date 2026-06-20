@echo off
cd /d "%~dp0"
echo Compiling Java Cart Service...
javac CartServer.java -d .
if %ERRORLEVEL% NEQ 0 (
    echo Failed to compile. Make sure Java JDK is installed.
    pause
    exit /b 1
)
echo Starting Java Cart Service on port 8081...
java CartServer
pause

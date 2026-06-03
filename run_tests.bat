@echo off

call venv\Scripts\activate

python -m pytest

if %ERRORLEVEL% EQU 0 (
    exit /b 0
) else (
    exit /b 1
)
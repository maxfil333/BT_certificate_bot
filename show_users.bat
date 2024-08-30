@echo off

REM Проверка наличия папки .venv
if exist .venv (
    call .venv\Scripts\activate
) else (
    call venv\Scripts\activate
)

REM running script
python -m src.sql_queries

REM user enter
echo.
echo press any button to close this window
pause >nul

@echo off

REM Переход в корневую директорию репозитория
cd ..

REM Проверка наличия папки .venv
if exist .venv (
    call .venv\Scripts\activate
) else (
    call venv\Scripts\activate
)

REM running script
python -m scripts.show_users

REM user enter
echo.
echo press any button to close this window
pause >nul

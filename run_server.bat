@echo off
cd /d "%~dp0"

set logFile=C:\Users\Filipp\Desktop\BT_certificate_bot\logfile.log
echo Запуск скрипта >> %logFile%
echo Текущая дата и время: %date% %time% >> %logFile%

REM Проверка наличия папки .venv
if exist .venv (
    call .venv\Scripts\activate
) else (
    call venv\Scripts\activate
)

python main.py --production >> %logFile% 2>&1

echo Скрипт завершён >> %logFile%

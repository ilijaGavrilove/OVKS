@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

cd /d "%~dp0"

:: Проверка прав администратора
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка: Скрипт должен быть запущен от имени администратора.
    pause
    exit /b 1
)

set "INSTALLED_ANY=0"

:: 1. Проверка / установка Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python не найден. Начинаем установку...
    set "INSTALLED_ANY=1"

    :: Попытка использовать winget
    where winget >nul 2>&1
    if !errorlevel! equ 0 (
        echo Устанавливаем Python через winget...
        winget install Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements --override "/quiet InstallAllUsers=1 PrependPath=1"
        if !errorlevel! neq 0 (
            echo Ошибка winget, пробуем скачать установщик вручную...
            call :DownloadPython
        )
    ) else (
        call :DownloadPython
    )

    :: Обновляем PATH из реестра
    call :RefreshPath

    :: Проверяем, появился ли python
    where python >nul 2>&1
    if !errorlevel! neq 0 (
        echo Python всё ещё не обнаружен, ищем папку установки...
        for /f "delims=" %%i in ('dir /b /ad "%ProgramFiles%\Python*" 2^>nul') do (
            set "PYTHON_ROOT=%ProgramFiles%\%%i\"
            set "PATH=!PYTHON_ROOT!;!PYTHON_ROOT!Scripts;!PATH!"
        )
        where python >nul 2>&1
        if !errorlevel! neq 0 (
            echo Не удалось обнаружить Python. Перезагрузите компьютер и попробуйте снова.
            pause
            exit /b 1
        )
    )
) else (
    echo Python уже установлен.
    for /f "delims=" %%i in ('where python') do set "PYTHON_ROOT=%%~dpi"
)

:: 2. Проверка / установка Poetry
where poetry >nul 2>&1
if %errorlevel% neq 0 (
    echo Poetry не найден. Устанавливаем...
    if not defined PYTHON_ROOT (
        for /f "delims=" %%i in ('where python') do set "PYTHON_ROOT=%%~dpi"
    )
    python -m pip install --upgrade pip
    python -m pip install poetry
    if !errorlevel! neq 0 (
        echo Ошибка установки Poetry. Установите его вручную: https://python-poetry.org/docs/
        pause
        exit /b 1
    )
    call :RefreshPath
    where poetry >nul 2>&1
    if !errorlevel! neq 0 (
        set "PATH=!PYTHON_ROOT!Scripts;!PATH!"
        where poetry >nul 2>&1
        if !errorlevel! neq 0 (
            echo Poetry всё ещё не найден. Перезагрузите компьютер и повторите попытку.
            pause
            exit /b 1
        )
    )
    set "INSTALLED_ANY=1"
) else (
    echo Poetry уже установлен.
)

:: 3. Завершение
if %INSTALLED_ANY% equ 1 (
    echo Установка завершена. Для полного применения изменений рекомендуется перезагрузка и повторный запуск инсталлятора.
    set /p "REBOOT=Перезагрузить компьютер сейчас? (y/n): "
    if /i "!REBOOT!"=="y" (
        shutdown /r /t 0
    ) else (
        echo Перезагрузка отменена. Пожалуйста, перезагрузите компьютер позже.
    )
) else (
    echo Все необходимые компоненты установлены.
    echo Импорт библиотек...
    poetry install
)

pause
exit /b 0

:: === Вспомогательные функции ===

:RefreshPath
    for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH 2^>nul ^| findstr /i "PATH"') do set "MACHINE_PATH=%%b"
    for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v PATH 2^>nul ^| findstr /i "PATH"') do set "USER_PATH=%%b"
    set "PATH=%MACHINE_PATH%;%USER_PATH%"
exit /b

:DownloadPython
    echo Скачиваем установщик Python...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe' -OutFile '%TEMP%\python-installer.exe'"
    if exist "%TEMP%\python-installer.exe" (
        "%TEMP%\python-installer.exe" /quiet InstallAllUsers=1 PrependPath=1
        del "%TEMP%\python-installer.exe"
    ) else (
        echo Не удалось скачать установщик. Скачайте Python вручную с https://python.org
        pause
        exit /b 1
    )
exit /b
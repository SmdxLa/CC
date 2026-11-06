
@echo off
setlocal EnableExtensions
chcp 65001 >nul
title Git Push Auto Retry

REM 切换到脚本所在目录
cd /d "%~dp0"

REM 查找真正的 git.exe
set "GIT_EXE="
for /f "delims=" %%G in ('where.exe git.exe 2^>nul') do (
    if not defined GIT_EXE set "GIT_EXE=%%G"
)

if not defined GIT_EXE (
    echo [ERROR] 找不到 git.exe，请检查 Git 是否安装。
    pause
    exit /b 1
)

echo Git: %GIT_EXE%
echo ==================================

:retry
echo.
echo [%date% %time%] 正在尝试 git push...

"%GIT_EXE%" push
set "RESULT=%errorlevel%"

if "%RESULT%"=="0" (
    echo.
    echo [SUCCESS] 推送成功！
    pause
    exit /b 0
)

echo.
echo [FAILED] Git 返回错误码：%RESULT%
echo 10 秒后再次尝试...
timeout /t 10 /nobreak >nul

goto retry

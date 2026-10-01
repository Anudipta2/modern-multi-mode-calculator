@echo off
title Installing Modern Multi-Mode Calculator...
echo ==========================================================
echo    Installing Modern Multi-Mode Calculator for Windows
echo ==========================================================
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0install.ps1"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Installation encountered an issue.
    pause
)

@echo off
title Uninstalling Modern Multi-Mode Calculator...
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0uninstall.ps1"
pause

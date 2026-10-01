# Uninstaller for Modern Multi-Mode Calculator

$AppName = "Modern Multi-Mode Calculator"
$AppId = "ModernCalculator"
$InstallDir = "$env:LOCALAPPDATA\Programs\$AppId"

Write-Host "==========================================================" -ForegroundColor Yellow
Write-Host "   Uninstalling $AppName" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Yellow

# 1. Terminate running instances
Get-Process -Name "ModernCalculator" -ErrorAction SilentlyContinue | Stop-Process -Force

# 2. Remove Shortcuts
$StartMenuShortcut = "$([Environment]::GetFolderPath('Programs'))\$AppName.lnk"
if (Test-Path $StartMenuShortcut) {
    Remove-Item -Path $StartMenuShortcut -Force -ErrorAction SilentlyContinue
    Write-Host "Removed Start Menu shortcut." -ForegroundColor Gray
}

$DesktopShortcut = "$([Environment]::GetFolderPath('Desktop'))\$AppName.lnk"
if (Test-Path $DesktopShortcut) {
    Remove-Item -Path $DesktopShortcut -Force -ErrorAction SilentlyContinue
    Write-Host "Removed Desktop shortcut." -ForegroundColor Gray
}

# 3. Remove Registry Entry
$RegKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\$AppId"
if (Test-Path $RegKey) {
    Remove-Item -Path $RegKey -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Removed Windows Settings / Registry entry." -ForegroundColor Gray
}

# 4. Schedule directory removal after process exit
Start-Process cmd.exe -ArgumentList "/c timeout /t 2 /nobreak > NUL & rmdir /s /q `"$InstallDir`"" -WindowStyle Hidden

Write-Host "Modern Multi-Mode Calculator has been successfully uninstalled." -ForegroundColor Green

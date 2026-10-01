# Windows PowerShell Installer for Modern Multi-Mode Calculator
# Installs application for the current user (No Administrator privileges required)

param(
    [switch]$Silent = $false
)

$ErrorActionPreference = "Stop"

$AppName = "Modern Multi-Mode Calculator"
$AppId = "ModernCalculator"
$Version = "1.0.0"
$Publisher = "Antigravity Solutions"

$InstallDir = "$env:LOCALAPPDATA\Programs\$AppId"
$ExeName = "ModernCalculator.exe"

# Resolve source executable path
$SourceExe = "$PSScriptRoot\..\dist\$ExeName"
if (-not (Test-Path $SourceExe)) {
    $SourceExe = "$PSScriptRoot\$ExeName"
}

if (-not (Test-Path $SourceExe)) {
    Write-Host "[ERROR] Compiled executable '$ExeName' was not found in 'dist\' or script directory." -ForegroundColor Red
    Write-Host "Please build the executable first using PyInstaller." -ForegroundColor Yellow
    exit 1
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   Installing $AppName (v$Version)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Terminate running instances if any
Get-Process -Name "ModernCalculator" -ErrorAction SilentlyContinue | Stop-Process -Force

# 2. Create Target Directory
Write-Host "[1/5] Creating application directory: $InstallDir" -ForegroundColor Gray
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
New-Item -ItemType Directory -Force -Path "$InstallDir\assets" | Out-Null

# 3. Copy Application Files
Write-Host "[2/5] Copying application files..." -ForegroundColor Gray
Copy-Item -Path $SourceExe -Destination "$InstallDir\$ExeName" -Force

$SourceAssets = "$PSScriptRoot\..\assets"
if (Test-Path "$SourceAssets\icon.ico") {
    Copy-Item -Path "$SourceAssets\icon.ico" -Destination "$InstallDir\assets\icon.ico" -Force
}
if (Test-Path "$SourceAssets\icon.png") {
    Copy-Item -Path "$SourceAssets\icon.png" -Destination "$InstallDir\assets\icon.png" -Force
}

# 4. Copy Uninstaller script
$UninstallScript = "$InstallDir\uninstall.ps1"
Copy-Item -Path "$PSScriptRoot\uninstall.ps1" -Destination $UninstallScript -Force -ErrorAction SilentlyContinue
Copy-Item -Path "$PSScriptRoot\uninstall.bat" -Destination "$InstallDir\uninstall.bat" -Force -ErrorAction SilentlyContinue

# 5. Create Shortcuts (Desktop & Start Menu)
Write-Host "[3/5] Creating Windows Start Menu and Desktop shortcuts..." -ForegroundColor Gray
$WshShell = New-Object -ComObject WScript.Shell

# Start Menu Shortcut
$StartMenuDir = [Environment]::GetFolderPath("Programs")
$StartMenuShortcut = $WshShell.CreateShortcut("$StartMenuDir\$AppName.lnk")
$StartMenuShortcut.TargetPath = "$InstallDir\$ExeName"
$StartMenuShortcut.WorkingDirectory = $InstallDir
$StartMenuShortcut.Description = "Modern Apple-inspired Multi-Mode Calculator"
if (Test-Path "$InstallDir\assets\icon.ico") {
    $StartMenuShortcut.IconLocation = "$InstallDir\assets\icon.ico,0"
}
$StartMenuShortcut.Save()

# Desktop Shortcut
$DesktopDir = [Environment]::GetFolderPath("Desktop")
$DesktopShortcut = $WshShell.CreateShortcut("$DesktopDir\$AppName.lnk")
$DesktopShortcut.TargetPath = "$InstallDir\$ExeName"
$DesktopShortcut.WorkingDirectory = $InstallDir
$DesktopShortcut.Description = "Modern Apple-inspired Multi-Mode Calculator"
if (Test-Path "$InstallDir\assets\icon.ico") {
    $DesktopShortcut.IconLocation = "$InstallDir\assets\icon.ico,0"
}
$DesktopShortcut.Save()

# 6. Register in Windows Add/Remove Programs (Settings > Apps)
Write-Host "[4/5] Registering in Windows Settings (Add or Remove Programs)..." -ForegroundColor Gray
$RegKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\$AppId"
New-Item -Path $RegKey -Force | Out-Null

$ExeSize = (Get-Item "$InstallDir\$ExeName").Length / 1KB

Set-ItemProperty -Path $RegKey -Name "DisplayName" -Value $AppName
Set-ItemProperty -Path $RegKey -Name "DisplayVersion" -Value $Version
Set-ItemProperty -Path $RegKey -Name "Publisher" -Value $Publisher
Set-ItemProperty -Path $RegKey -Name "DisplayIcon" -Value "$InstallDir\$ExeName,0"
Set-ItemProperty -Path $RegKey -Name "InstallLocation" -Value $InstallDir
Set-ItemProperty -Path $RegKey -Name "UninstallString" -Value "powershell.exe -ExecutionPolicy Bypass -File `"$InstallDir\uninstall.ps1`""
Set-ItemProperty -Path $RegKey -Name "EstimatedSize" -Value ([int]$ExeSize)
Set-ItemProperty -Path $RegKey -Name "NoModify" -Value 1
Set-ItemProperty -Path $RegKey -Name "NoRepair" -Value 1

Write-Host "[5/5] Installation Completed Successfully!" -ForegroundColor Green
Write-Host "----------------------------------------------------------" -ForegroundColor Cyan
Write-Host "You can now launch the app from:" -ForegroundColor White
Write-Host "  * Windows Start Menu: Search for '$AppName'" -ForegroundColor Yellow
Write-Host "  * Desktop Shortcut: '$AppName'" -ForegroundColor Yellow
Write-Host "  * File Path: '$InstallDir\$ExeName'" -ForegroundColor Yellow
Write-Host "----------------------------------------------------------" -ForegroundColor Cyan

if (-not $Silent) {
    # Ask or launch immediately
    Write-Host "Starting Modern Calculator now..." -ForegroundColor Green
    Start-Process "$InstallDir\$ExeName"
}

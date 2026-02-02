# Part A: Install Qt 5.15.2 with Qt WebEngine
# This script downloads the Qt Online Installer (if needed) and launches it with install path C:\Qt.
# You must complete the steps in the installer GUI: sign in, select Qt 5.15.2 + MSVC + Qt WebEngine, then Install.

param(
    [string]$InstallRoot = "C:\Qt"
)

$InstallerUrl = "https://download.qt.io/official_releases/online_installers/qt-online-installer-windows-x64-online.exe"
$InstallerPath = "$env:TEMP\qt-online-installer-windows-x64-online.exe"

Write-Host "=== Part A: Qt 5.15.2 + Qt WebEngine ===" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path $InstallerPath) -or (Get-Item $InstallerPath).Length -lt 50MB) {
    Write-Host "Downloading Qt Online Installer..." -ForegroundColor Yellow
    try {
        Invoke-WebRequest -Uri $InstallerUrl -OutFile $InstallerPath -UseBasicParsing
    } catch {
        Write-Host "Download failed. Open this URL in your browser and run the installer manually:" -ForegroundColor Red
        Write-Host "  $InstallerUrl" -ForegroundColor White
        exit 1
    }
    Write-Host "Download complete." -ForegroundColor Green
} else {
    Write-Host "Qt Online Installer already present." -ForegroundColor Green
}

Write-Host ""
Write-Host "Starting Qt Online Installer with install path: $InstallRoot" -ForegroundColor Cyan
Write-Host ""
Write-Host "In the installer window, do the following:" -ForegroundColor Yellow
Write-Host "  1. Sign in (or create) your Qt account."
Write-Host "  2. Accept the license if prompted."
Write-Host "  3. Installation folder: leave as $InstallRoot (or change if you prefer)."
Write-Host "  4. Under Qt, expand and check: Qt 5.15.2"
Write-Host "  5. Under Qt 5.15.2, check ONE of:"
Write-Host "       - MSVC 2019 64-bit  (if you use Visual Studio 2019)"
Write-Host "       - MSVC 2022 64-bit (if you use Visual Studio 2022)"
Write-Host "  6. Under Qt 5.15.2, expand 'Additional Libraries' and check: Qt WebEngine"
Write-Host "  7. Click Next, then Install. Wait for the download/install to finish."
Write-Host ""
Write-Host "After install, your Qt5_DIR will be:" -ForegroundColor Cyan
Write-Host "  VS 2019: $InstallRoot/5.15.2/msvc2019_64/lib/cmake/Qt5" -ForegroundColor White
Write-Host "  VS 2022: $InstallRoot/5.15.2/msvc2022_64/lib/cmake/Qt5" -ForegroundColor White
Write-Host ""

Start-Process -FilePath $InstallerPath -ArgumentList "--root", $InstallRoot -Wait

Write-Host "Installer closed. If you completed the steps above, Part A is done." -ForegroundColor Green

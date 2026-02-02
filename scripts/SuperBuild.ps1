# AutoSegmentSlicer SuperBuild script (Windows)
# Run this AFTER installing: Qt 5.15.2 (with WebEngine), CMake, Visual Studio (C++ workload)
# Usage: .\SuperBuild.ps1 [-Qt5Dir "C:/Qt/5.15.2/msvc2019_64/lib/cmake/Qt5"] [-BuildDir "M:\ASS-Build"] [-ConfigureOnly] [-BuildOnly]
#
# IMPORTANT: Use a SHORT build path to avoid MSB8066 (VTK/ExternalProject install step fails on long paths).
# Recommended: -BuildDir "M:\ASS-Build" or -BuildDir "C:\ASS-Build" (max ~60 chars total for build dir).

param(
    [string]$Qt5Dir = "",
    [string]$BuildDir = "",
    [switch]$ConfigureOnly,
    [switch]$BuildOnly
)

$ErrorActionPreference = "Stop"
$SourceDir = "M:\RKDrive\rk\AutoSegmentSlicer\AutoSegmentSlicer"
# Default to a short path to avoid MSB8066 (VTK install step fails when path is too long)
if (-not $BuildDir) {
    $BuildDir = "M:\ASS-Build"
}

# Try common Qt 5.15.2 locations if not provided
if (-not $Qt5Dir) {
    $candidates = @(
        "C:\Qt\5.15.2\msvc2022_64\lib\cmake\Qt5",
        "C:\Qt\5.15.2\msvc2019_64\lib\cmake\Qt5",
        "C:\Qt\5.15.2\msvc2017_64\lib\cmake\Qt5"
    )
    foreach ($c in $candidates) {
        if (Test-Path $c) {
            $Qt5Dir = $c -replace "\\", "/"
            Write-Host "Using Qt5_DIR: $Qt5Dir"
            break
        }
    }
}

if (-not $Qt5Dir) {
    Write-Host "ERROR: Qt5_DIR not set and no Qt 5.15.2 found in common locations."
    Write-Host "Install Qt 5.15.2 (with Qt WebEngine) and run:"
    Write-Host '  .\SuperBuild.ps1 -Qt5Dir "C:/Qt/5.15.2/msvc2019_64/lib/cmake/Qt5"'
    exit 1
}

# Prefer VS 2022; fallback to VS 2019
$Generator = "Visual Studio 17 2022"
$vsWhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
if (Test-Path $vsWhere) {
    $vsPath = & $vsWhere -latest -products * -requires Microsoft.Component.MSBuild -property installationPath 2>$null
    if (-not $vsPath) {
        $Generator = "Visual Studio 16 2019"
    }
} else {
    $Generator = "Visual Studio 16 2019"
}

if (-not (Test-Path $SourceDir)) {
    Write-Host "ERROR: Source directory not found: $SourceDir"
    exit 1
}

# Warn if build path is long (VTK/ExternalProject install can fail with MSB8066)
if ($BuildDir.Length -gt 55) {
    Write-Host "WARNING: Build path is long ($($BuildDir.Length) chars). VTK install may fail with MSB8066."
    Write-Host "         Use a short path, e.g: .\SuperBuild.ps1 -BuildDir `"M:\ASS-Build`""
}

if (-not $BuildOnly) {
    if (-not (Test-Path $BuildDir)) {
        New-Item -ItemType Directory -Path $BuildDir -Force | Out-Null
        Write-Host "Created build directory: $BuildDir"
    }
    Write-Host "Configuring in $BuildDir ..."
    Push-Location $BuildDir
    try {
        # ITK_SKIP_PATH_LENGTH_CHECKS=ON avoids "ITK source path length too long (59 > 50)" on Windows
        & cmake -G $Generator -A x64 -DQt5_DIR:PATH="$Qt5Dir" -DITK_SKIP_PATH_LENGTH_CHECKS=ON $SourceDir
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    } finally {
        Pop-Location
    }
    Write-Host "Configure done. You can open the solution in Visual Studio or run this script again with -BuildOnly."
    if ($ConfigureOnly) { exit 0 }
}

Write-Host "Building Release (this can take 1-3 hours on first run)..."
Push-Location $BuildDir
try {
    & cmake --build . --config Release -- /maxcpucount:4
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
    Pop-Location
}
Write-Host "Build finished. Run the app: $BuildDir\Slicer-build\AutoSegmentSlicer.exe"

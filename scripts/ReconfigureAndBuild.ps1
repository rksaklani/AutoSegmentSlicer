# Reconfigure and build AutoSegmentSlicer.
# Close Cursor/VS/other apps that might lock _deps\slicersources-src before running.
# Usage: .\ReconfigureAndBuild.ps1

$ErrorActionPreference = "Stop"
$BuildDir = "M:\RKDrive\rk\AutoSegmentSlicer\AutoSegmentSlicer-Build"
$SrcDir   = "$BuildDir\_deps\slicersources-src"

Write-Host "Removing slicersources cache (so patch step runs with run_apply.bat)..."
cmd /c "rd /s /q `"$SrcDir`" 2>nul"
if (Test-Path $SrcDir) {
    Write-Host "WARNING: Could not remove $SrcDir (file in use?). Close Cursor/VS and run this script again from a new PowerShell."
    exit 1
}

Push-Location "M:\RKDrive\rk\AutoSegmentSlicer\AutoSegmentSlicer\scripts"
try {
    Write-Host "Configuring..."
    & .\SuperBuild.ps1 -ConfigureOnly
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Host "Building..."
    & .\SuperBuild.ps1 -BuildOnly
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Host "Done."
} finally {
    Pop-Location
}

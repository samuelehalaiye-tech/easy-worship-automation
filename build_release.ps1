$ErrorActionPreference = "Stop"

$Project = "C:\Users\User\Documents\easyworshi"
$Dist = Join-Path $Project "dist"
$Release = Join-Path $Project "release"

$Py32 = "C:\Users\User\AppData\Local\Programs\Python\Python313-32\python.exe"
$Py64 = "C:\Users\User\AppData\Local\Programs\Python\Python312\python.exe"

Set-Location $Project

Write-Host "Cleaning previous builds..."

Remove-Item "$Project\build" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$Project\dist" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$Release" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "Building EasyWorship Worker..."

& $Py32 -m PyInstaller `
    --clean `
    --noconfirm `
    --onedir `
    --name EasyWorshipWorker `
    server.py

if ($LASTEXITCODE -ne 0) {
    throw "EasyWorshipWorker build failed."
}

Write-Host ""
Write-Host "Building Moonshine Worker..."

& $Py64 -m PyInstaller `
    --clean `
    --noconfirm `
    --onedir `
    --name MoonshineWorker `
    --collect-all moonshine_voice `
    moonshine_bridge.py

if ($LASTEXITCODE -ne 0) {
    throw "MoonshineWorker build failed."
}

Write-Host ""
Write-Host "Building main application..."

& $Py64 -m PyInstaller `
    --clean `
    --noconfirm `
    --onedir `
    --name EasyWorshipVoiceController `
    launcher.py

if ($LASTEXITCODE -ne 0) {
    throw "Main application build failed."
}

Write-Host ""
Write-Host "Assembling release..."

$App = Join-Path $Release "EasyWorshipVoiceController"

New-Item -ItemType Directory -Path $App -Force | Out-Null

Copy-Item `
    "$Dist\EasyWorshipVoiceController\*" `
    $App `
    -Recurse `
    -Force

Copy-Item `
    "$Dist\EasyWorshipWorker" `
    "$App\EasyWorshipWorker" `
    -Recurse `
    -Force

Copy-Item `
    "$Dist\MoonshineWorker" `
    "$App\MoonshineWorker" `
    -Recurse `
    -Force

Write-Host ""
Write-Host "=========================================="
Write-Host "BUILD COMPLETE"
Write-Host "=========================================="
Write-Host ""
Write-Host "Application:"
Write-Host "$App\EasyWorshipVoiceController.exe"
Write-Host ""
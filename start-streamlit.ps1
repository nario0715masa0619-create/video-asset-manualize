# start-streamlit.ps1
# Docker Compose で Streamlit を起動し、ブラウザを自動起動するスクリプト

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "VideoAsset Manualize - Docker Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# プロジェクトディレクトリ
$projectDir = "D:\AI_スクリプト成果物\video-asset-manualize"
Set-Location $projectDir

# Docker が実行中か確認
docker --version | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker が起動していません。Docker Desktop を起動してください。" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker は起動しています" -ForegroundColor Green
Write-Host "Streamlit を起動中..." -ForegroundColor Yellow
Write-Host ""

# ブラウザを自動起動
Start-Sleep -Seconds 2
Start-Process "http://localhost:8501"

# Docker Compose を起動
docker compose up

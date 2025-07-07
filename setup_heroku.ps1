Write-Host "🔧 Setting up Heroku CLI for Windows" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""

Write-Host "🔍 Looking for Heroku installation..." -ForegroundColor Yellow

# Common installation paths
$herokuPaths = @(
    "C:\Program Files\Heroku\bin",
    "C:\Program Files (x86)\Heroku\bin", 
    "$env:LOCALAPPDATA\Programs\Heroku\bin",
    "$env:APPDATA\npm"
)

$herokuFound = $false

foreach ($path in $herokuPaths) {
    $herokuExe = Join-Path $path "heroku.exe"
    if (Test-Path $herokuExe) {
        Write-Host "✅ Found Heroku at: $herokuExe" -ForegroundColor Green
        Write-Host ""
        Write-Host "🔧 Adding to PATH temporarily..." -ForegroundColor Yellow
        $env:PATH = "$path;$env:PATH"
        
        Write-Host "🚀 Testing Heroku..." -ForegroundColor Yellow
        try {
            $version = & $herokuExe --version 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Heroku is working! Version: $version" -ForegroundColor Green
                Write-Host ""
                Write-Host "🚀 Now let's deploy..." -ForegroundColor Green
                Write-Host ""
                python deploy.py
                $herokuFound = $true
                break
            }
        }
        catch {
            Write-Host "❌ Heroku found but not working properly" -ForegroundColor Red
        }
    }
}

if (-not $herokuFound) {
    Write-Host "❌ Heroku CLI not found in common locations" -ForegroundColor Red
    Write-Host ""
    Write-Host "📥 Please try one of these solutions:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Restart your computer after installing Heroku" -ForegroundColor White
    Write-Host "2. Install Heroku CLI via npm: npm install -g heroku" -ForegroundColor White
    Write-Host "3. Download from: https://devcenter.heroku.com/articles/heroku-cli" -ForegroundColor White
    Write-Host ""
    Write-Host "After installation, run this script again." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 
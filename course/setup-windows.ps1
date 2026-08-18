# Установка окружения для курса «Базы данных»
# Запуск: PowerShell от имени администратора (рекомендуется)
#   Set-ExecutionPolicy -Scope Process Bypass -Force
#   cd e:\Projects\db_stud\course
#   .\setup-windows.ps1

$ErrorActionPreference = "Stop"

Write-Host "=== Установка окружения курса БД ===" -ForegroundColor Cyan

# winget
if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Host "winget не найден. Установите App Installer из Microsoft Store." -ForegroundColor Red
    exit 1
}

$wingetArgs = @(
    "install", "--accept-package-agreements", "--accept-source-agreements",
    "--disable-interactivity", "--source", "winget"
)

function Install-IfMissing {
    param([string]$Id, [string]$Name, [string[]]$TestCommands)
    foreach ($cmd in $TestCommands) {
        if (Get-Command $cmd -ErrorAction SilentlyContinue) {
            Write-Host "[OK] $Name уже установлен ($cmd)" -ForegroundColor Green
            return
        }
    }
    Write-Host "Устанавливаю $Name..." -ForegroundColor Yellow
    & winget @wingetArgs --id $Id
    if ($LASTEXITCODE -gt 1) {
        Write-Host "Предупреждение: winget вернул код $LASTEXITCODE для $Name" -ForegroundColor Yellow
    }
}

# 1. Python (статический просмотр курса)
Install-IfMissing -Id "Python.Python.3.12" -Name "Python 3.12" -TestCommands @("python", "py")

# 2. Node.js LTS (React/Vite версия)
Install-IfMissing -Id "OpenJS.NodeJS.LTS" -Name "Node.js LTS" -TestCommands @("node", "npm")

# 3. PostgreSQL 17 (SQL-практика)
Install-IfMissing -Id "PostgreSQL.PostgreSQL.17" -Name "PostgreSQL 17" -TestCommands @("psql")

# Обновить PATH в текущей сессии
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" +
            [System.Environment]::GetEnvironmentVariable("Path", "User")

Write-Host "`n=== Проверка версий ===" -ForegroundColor Cyan
foreach ($cmd in @("python", "node", "npm", "psql")) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        & $cmd --version 2>&1 | ForEach-Object { Write-Host "  $cmd : $_" }
    } else {
        Write-Host "  $cmd : не найден (перезапустите PowerShell после установки)" -ForegroundColor Yellow
    }
}

# 4. Зависимости npm для React-приложения
$courseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (Get-Command npm -ErrorAction SilentlyContinue) {
    Write-Host "`n=== npm install в course/ ===" -ForegroundColor Cyan
    Push-Location $courseDir
    npm install
    Pop-Location
    Write-Host "[OK] npm install завершён" -ForegroundColor Green
}

Write-Host @"

=== Дальнейшие шаги ===

1. ПЕРЕЗАПУСТИТЕ PowerShell (чтобы подхватился PATH).

2. Запуск курса (статическая версия, проще):
   cd e:\Projects\db_stud\course
   python -m http.server 8080
   Откройте: http://localhost:8080/static/

3. Или React-версия:
   cd e:\Projects\db_stud\course
   npm run dev
   Откройте: http://localhost:5173

4. PostgreSQL — при установке задайте пароль пользователя postgres.
   Затем создайте учебную БД:
   psql -U postgres -h localhost
   CREATE USER dbstud WITH PASSWORD 'dbstud2024';
   CREATE DATABASE dbstud OWNER dbstud;
   \q

5. Проверка SQL:
   psql -U dbstud -d dbstud -h localhost
   \i e:/Projects/db_stud/course/sql/schema-university.sql

"@ -ForegroundColor Cyan

Write-Host "Готово." -ForegroundColor Green

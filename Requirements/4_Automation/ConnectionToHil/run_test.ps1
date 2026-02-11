# ============================================================================
# Script Automatizado: Deploy VeriStand + Rodar Teste
# ============================================================================
# 
# Este script faz TUDO automaticamente:
# 1. Inicia NetPipeActivator
# 2. Deploy VeriStand
# 3. Roda teste (dry run ou safe)
# 4. Gera relatório
# 5. Desconecta VeriStand
#
# USO:
#   .\run_test.ps1                    # Dry run (padrão)
#   .\run_test.ps1 -Mode safe         # Versão safe com proteções
#   .\run_test.ps1 -Mode normal       # Versão normal (cuidado!)
#
# ============================================================================

param(
    [ValidateSet("dry", "safe", "normal")]
    [string]$Mode = "dry",
    
    [switch]$SkipReport
)

# Simple output functions without ANSI colors
function Write-Header {
    param([string]$Title)
    Write-Host ""
    Write-Host "============================================================================"
    Write-Host "  $Title"
    Write-Host "============================================================================"
    Write-Host ""
}

function Write-Step {
    param([string]$StepName)
    Write-Host ""
    Write-Host "[STEP] $StepName"
    Write-Host "----------------------------------------------------------------------------"
}

function Write-Success {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "[X] $Message" -ForegroundColor Red
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[!] $Message" -ForegroundColor Yellow
}

# ============================================================================
# Configuração
# ============================================================================

# Auto-detectar o diretório do projeto (onde o script está)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$WorkDir = $ScriptDir

Write-Host "Auto-detected paths:"
Write-Host "  Script Dir:   $ScriptDir"
Write-Host "  Project Root: $ProjectRoot"
Write-Host ""

$TestFiles = @{
    "dry" = "test_max_defrost_dry_run.py"
    "safe" = "test_max_defrost_safe.py"
    "normal" = "test_max_defrost.py"
}

$ReportFiles = @{
    "dry" = "test_max_defrost_dry_run_report.html"
    "safe" = "test_max_defrost_safe_report.html"
    "normal" = "test_max_defrost_report.html"
}

# ============================================================================
# Main Script
# ============================================================================

Write-Header "HIL Test Runner - Max Defrost Test"

Write-Host "Mode: $Mode"
Write-Host "Project: $ProjectRoot"
Write-Host "Working Dir: $WorkDir"

# Verificar se estamos rodando como Admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Warning "Este script precisa de permissoes de Administrador"
    Write-Warning "Tentando elevar privilegios..."
    
    $scriptPath = $MyInvocation.MyCommand.Path
    Start-Process powershell -Verb RunAs -ArgumentList "-NoExit -ExecutionPolicy Bypass -Command `"& '$scriptPath' -Mode $Mode`""
    exit
}

Write-Success "Executando como Administrador"
Write-Host ""
Write-Warning "ATENCAO: Este script vai interagir com o hardware!"
Write-Host "Pressione ENTER para continuar ou Ctrl+C para cancelar..."
$null = Read-Host

# ============================================================================
# Passo 1: Validações
# ============================================================================

Write-Step "Validando ambiente"

# Verificar pasta existe
if (-not (Test-Path $WorkDir)) {
    Write-Error "Pasta não encontrada: $WorkDir"
    exit 1
}

Set-Location $WorkDir
Write-Success "Navegado para: $WorkDir"

# Verificar Python
try {
    $pythonVersion = python --version 2>&1
    Write-Success "Python encontrado: $pythonVersion"
} catch {
    Write-Error "Python não encontrado no PATH"
    exit 1
}

# Verificar arquivo de teste existe
$testFile = $TestFiles[$Mode]
if (-not (Test-Path $testFile)) {
    Write-Error "Arquivo de teste não encontrado: $testFile"
    exit 1
}
Write-Success "Arquivo de teste: $testFile"

# ============================================================================
# Passo 2: Configurar ambiente
# ============================================================================

Write-Step "Configurando ambiente"

$env:CI_PROJECT_DIR = $ProjectRoot
Write-Success "CI_PROJECT_DIR = $env:CI_PROJECT_DIR"

# ============================================================================
# Passo 3: Iniciar NetPipeActivator
# ============================================================================

Write-Step "Iniciando serviço NetPipeActivator"

try {
    $service = Get-Service NetPipeActivator -ErrorAction Stop
    
    if ($service.Status -eq "Running") {
        Write-Success "NetPipeActivator já está rodando"
    } else {
        Start-Service NetPipeActivator
        Start-Sleep -Seconds 2
        
        $service = Get-Service NetPipeActivator
        if ($service.Status -eq "Running") {
            Write-Success "NetPipeActivator iniciado com sucesso"
        } else {
            Write-Error "Falha ao iniciar NetPipeActivator"
            exit 1
        }
    }
} catch {
    Write-Error "Serviço NetPipeActivator não encontrado"
    Write-Warning "Verifique se VeriStand 2025 está instalado"
    exit 1
}

# ============================================================================
# Passo 4: Deploy VeriStand
# ============================================================================

Write-Step "Deploying VeriStand (pode levar ate 30 segundos)"

# Create temporary Python script in working directory to avoid import issues
$tempScript = Join-Path $WorkDir "temp_deploy.py"
$deployCode = @"
from hil_modules import read_project_config, connect_to_veristand
project_path, calibration_file, sys_addr, variables = read_project_config()
ws = connect_to_veristand(project_path, calibration_file, sys_addr)
print("VeriStand deployed")
"@

Set-Content -Path $tempScript -Value $deployCode -Encoding ASCII

try {
    $deployResult = python $tempScript 2>&1
    $deployExitCode = $LASTEXITCODE
    
    Write-Host $deployResult
    
    if ($deployExitCode -ne 0) {
        Write-Error "Falha ao deployar VeriStand"
        Write-Warning "Verifique se cRIO esta ligado e conectado"
        Remove-Item $tempScript -ErrorAction SilentlyContinue
        exit 1
    }
    
    Remove-Item $tempScript -ErrorAction SilentlyContinue
    Write-Success "VeriStand deployed e pronto para testes"
    Start-Sleep -Seconds 2
} catch {
    Write-Error "Erro ao executar deploy: $_"
    Remove-Item $tempScript -ErrorAction SilentlyContinue
    exit 1
}

# ============================================================================
# Passo 5: Avisos de Segurança
# ============================================================================

if ($Mode -eq "safe" -or $Mode -eq "normal") {
    Write-Host ""
    Write-ColorOutput "============================================================================" $ColorRed
    Write-ColorOutput "                        AVISO DE SEGURANCA" "$ColorBold$ColorRed"
    Write-ColorOutput "============================================================================" $ColorRed
    Write-Host ""
    Write-Warning "Este teste VAI CONTROLAR HARDWARE FISICO!"
    Write-Host ""
    Write-Host "Certifique-se de que:"
    Write-Host "  1. Hardware está preparado e monitorado"
    Write-Host "  2. Você entende o que o teste faz"
    Write-Host "  3. Tem acesso físico para emergências"
    Write-Host "  4. Sistemas de segurança estão ativos"
    Write-Host ""
    
    if ($Mode -eq "safe") {
        Write-Host "Modo SAFE ativo - protecoes habilitadas:" -ForegroundColor Green
        Write-Host "  Runtime limitado (30s)"
        Write-Host "  Gradual power-up"
        Write-Host "  Cooldown automatico"
        Write-Host "  Emergency shutdown (Ctrl+C)"
    } else {
        Write-Host "Modo NORMAL - SEM protecoes de runtime!" -ForegroundColor Red
        Write-Host "  Sem limite de tempo"
        Write-Host "  Power-up instantaneo"
        Write-Host "  Use apenas se validado anteriormente"
    }
    
    Write-Host ""
    $confirm = Read-Host "Digite 'SIM' para continuar"
    
    if ($confirm -ne "SIM") {
        Write-Warning "Teste cancelado pelo usuario"
        
        # Disconnect VeriStand
        Write-Step "Desconectando VeriStand"
        $tempDisconnect = Join-Path $WorkDir "temp_disconnect.py"
        Set-Content -Path $tempDisconnect -Value "from hil_modules import disconnect_hil`ndisconnect_hil()" -Encoding ASCII
        python $tempDisconnect 2>&1 | Out-Null
        Remove-Item $tempDisconnect -ErrorAction SilentlyContinue
        
        exit 0
    }
}

# ============================================================================
# Passo 6: Rodar Teste
# ============================================================================

Write-Step "Executando teste: $Mode"

if ($Mode -eq "dry") {
    Write-Host "DRY RUN MODE - Hardware nao sera alterado" -ForegroundColor Cyan
} elseif ($Mode -eq "safe") {
    Write-Host "SAFE MODE - Protecoes ativas" -ForegroundColor Green
} else {
    Write-Host "NORMAL MODE - Sem protecoes" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Iniciando pytest..."
Write-Host ""

# Add current directory to PYTHONPATH so pytest can import hil_modules
$env:PYTHONPATH = $WorkDir

# Rodar teste
$testResult = pytest -v $testFile -s --tb=short 2>&1
$testExitCode = $LASTEXITCODE

Write-Host $testResult

# ============================================================================
# Passo 7: Resultado
# ============================================================================

Write-Host ""

if ($testExitCode -eq 0) {
    Write-Success "Teste PASSOU"
} else {
    Write-Error "Teste FALHOU"
}

# ============================================================================
# Passo 8: Desconectar VeriStand
# ============================================================================

Write-Step "Desconectando VeriStand"

$tempDisconnect = Join-Path $WorkDir "temp_disconnect.py"
$disconnectCode = @"
from hil_modules import disconnect_hil
disconnect_hil()
"@

Set-Content -Path $tempDisconnect -Value $disconnectCode -Encoding ASCII
python $tempDisconnect 2>&1 | Out-Null
Remove-Item $tempDisconnect -ErrorAction SilentlyContinue

Start-Sleep -Seconds 2
Write-Success "VeriStand desconectado"

# ============================================================================
# Passo 9: Abrir Relatório
# ============================================================================

if (-not $SkipReport) {
    $reportFile = $ReportFiles[$Mode]
    
    if (Test-Path $reportFile) {
        Write-Step "Abrindo relatorio HTML"
        
        Start-Process $reportFile
        Write-Success "Relatorio aberto no navegador: $reportFile"
    } else {
        Write-Warning "Relatorio nao encontrado: $reportFile"
    }
}

# ============================================================================
# Resumo Final
# ============================================================================

Write-Header "Resumo da Execucao"

Write-Host "Modo:                $Mode"
Write-Host "Teste:              $testFile"

if ($testExitCode -eq 0) {
    Write-Host "Status:             PASSOU" -ForegroundColor Green
} else {
    Write-Host "Status:             FALHOU" -ForegroundColor Red
}

if (Test-Path $ReportFiles[$Mode]) {
    Write-Host "Relatorio:          $($ReportFiles[$Mode])"
}

Write-Host ""
Write-Host "Execucao completa" -ForegroundColor Green
Write-Host ""
Write-Host "Pressione ENTER para fechar..." -ForegroundColor Cyan
$null = Read-Host

exit $testExitCode

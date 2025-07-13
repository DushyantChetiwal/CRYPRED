# Windows Task Scheduler Setup for Hyperfrequent Arbitrage
# Run this script as Administrator to set up automatic arbitrage monitoring

param(
    [int]$IntervalSeconds = 10,
    [string]$TaskName = "CrypredArbitrage",
    [switch]$Remove
)

Write-Host "🚀 CRYPRED Arbitrage Task Scheduler Setup" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Gray

# Get current directory and script path
$CurrentDir = Get-Location
$ScriptPath = Join-Path $CurrentDir "scripts\hyperfrequent_arbitrage.py"
$PythonPath = (Get-Command python3 -ErrorAction SilentlyContinue).Source

if (-not $PythonPath) {
    $PythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
}

if (-not $PythonPath) {
    Write-Host "❌ Python not found in PATH. Please install Python or add it to PATH." -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $ScriptPath)) {
    Write-Host "❌ Arbitrage script not found at: $ScriptPath" -ForegroundColor Red
    exit 1
}

# Remove existing task if requested
if ($Remove) {
    Write-Host "🗑️  Removing existing task: $TaskName" -ForegroundColor Yellow
    try {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction Stop
        Write-Host "✅ Task removed successfully" -ForegroundColor Green
    }
    catch {
        Write-Host "⚠️  Task not found or couldn't be removed: $($_.Exception.Message)" -ForegroundColor Yellow
    }
    exit 0
}

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "⚠️  This script should be run as Administrator for best results." -ForegroundColor Yellow
    Write-Host "   You can still continue, but the task may have limited permissions." -ForegroundColor Yellow
    $continue = Read-Host "Continue anyway? (y/N)"
    if ($continue -ne 'y' -and $continue -ne 'Y') {
        exit 1
    }
}

Write-Host "📋 Configuration:" -ForegroundColor Green
Write-Host "   Task Name: $TaskName"
Write-Host "   Check Interval: $IntervalSeconds seconds"
Write-Host "   Python Path: $PythonPath"
Write-Host "   Script Path: $ScriptPath"
Write-Host "   Working Directory: $CurrentDir"

# Create the scheduled task action
$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument "$ScriptPath $IntervalSeconds" -WorkingDirectory $CurrentDir

# Create the trigger (start at logon and repeat)
$Trigger = New-ScheduledTaskTrigger -AtLogOn
$Trigger.Repetition = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Seconds $IntervalSeconds) | Select-Object -ExpandProperty Repetition

# Create task settings
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -DontStopOnIdleEnd

# Create the principal (user context)
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive

try {
    # Remove existing task if it exists
    try {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    }
    catch {
        # Task doesn't exist, continue
    }

    # Register the new task
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Description "CRYPRED Hyperfrequent Arbitrage Monitor - Checks for crypto arbitrage opportunities every $IntervalSeconds seconds"

    Write-Host "✅ Task '$TaskName' created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 Task Details:" -ForegroundColor Cyan
    Write-Host "   • Runs automatically at user logon"
    Write-Host "   • Repeats every $IntervalSeconds seconds"
    Write-Host "   • Logs to: arbitrage_runner.log"
    Write-Host "   • Data saved to: data/arbitrage/"
    Write-Host ""
    Write-Host "🔧 Management Commands:" -ForegroundColor Yellow
    Write-Host "   Start manually:  Start-ScheduledTask -TaskName '$TaskName'"
    Write-Host "   Stop task:       Stop-ScheduledTask -TaskName '$TaskName'"
    Write-Host "   Remove task:     .\setup_windows_task.ps1 -Remove"
    Write-Host "   View logs:       Get-Content arbitrage_runner.log -Tail 20"
    Write-Host ""
    Write-Host "🚀 Starting the task now..." -ForegroundColor Green
    Start-ScheduledTask -TaskName $TaskName
    
    Write-Host "✅ Hyperfrequent arbitrage monitoring is now active!" -ForegroundColor Green
}
catch {
    Write-Host "❌ Failed to create scheduled task: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Alternative: Run manually with:" -ForegroundColor Yellow
    Write-Host "   python3 scripts\hyperfrequent_arbitrage.py $IntervalSeconds"
}

Write-Host ""
Write-Host "📈 Monitor your arbitrage opportunities in real-time!" -ForegroundColor Cyan 
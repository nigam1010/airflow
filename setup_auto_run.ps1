# Setup Windows Task Scheduler to Auto-Run the Pipeline
# This creates a scheduled task that runs daily at 2 AM

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Auto-Run Setup for Data Pipeline" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$taskName = "DataScienceJobsPipeline"
$scriptPath = "d:\yogpro\Improve-Your-Hiring-Chance-For-Data-Science-Related-Roles-main\run_pipeline.ps1"

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "Task '$taskName' already exists. Removing old task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create the scheduled task action
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`""

# Create the trigger (daily at 2 AM)
$trigger = New-ScheduledTaskTrigger -Daily -At 2am

# Create task settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable

# Get current user
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Highest

# Register the scheduled task
try {
    Register-ScheduledTask `
        -TaskName $taskName `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Principal $principal `
        -Description "Automatically runs the Data Science Jobs analysis pipeline daily"
    
    Write-Host ""
    Write-Host "✓ Scheduled task created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Task Details:" -ForegroundColor Cyan
    Write-Host "  Name: $taskName" -ForegroundColor White
    Write-Host "  Schedule: Daily at 2:00 AM" -ForegroundColor White
    Write-Host "  Script: $scriptPath" -ForegroundColor White
    Write-Host ""
    Write-Host "The pipeline will now run automatically every day at 2 AM!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Useful Commands:" -ForegroundColor Yellow
    Write-Host "  View task: Get-ScheduledTask -TaskName '$taskName'" -ForegroundColor White
    Write-Host "  Run now: Start-ScheduledTask -TaskName '$taskName'" -ForegroundColor White
    Write-Host "  Disable: Disable-ScheduledTask -TaskName '$taskName'" -ForegroundColor White
    Write-Host "  Enable: Enable-ScheduledTask -TaskName '$taskName'" -ForegroundColor White
    Write-Host "  Remove: Unregister-ScheduledTask -TaskName '$taskName'" -ForegroundColor White
    Write-Host ""
    
    # Ask if user wants to test run now
    $response = Read-Host "Would you like to test run the pipeline now? (Y/N)"
    if ($response -eq 'Y' -or $response -eq 'y') {
        Write-Host ""
        Write-Host "Starting pipeline..." -ForegroundColor Yellow
        Start-ScheduledTask -TaskName $taskName
        Write-Host "✓ Pipeline started! Check pipeline_log.txt for progress." -ForegroundColor Green
    }
    
} catch {
    Write-Host ""
    Write-Host "✗ Error creating scheduled task: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "You may need to run PowerShell as Administrator" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host ""

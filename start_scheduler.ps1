# Start Airflow Scheduler
# Run this in a separate terminal window

$projectRoot = "d:\yogpro\Improve-Your-Hiring-Chance-For-Data-Science-Related-Roles-main"
$env:AIRFLOW_HOME = "$projectRoot\airflow"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Airflow Scheduler" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Airflow Home: $env:AIRFLOW_HOME" -ForegroundColor Yellow
Write-Host ""

airflow scheduler

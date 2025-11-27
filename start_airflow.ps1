# Quick Start Script for Apache Airflow
# This script helps you start Airflow quickly

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Apache Airflow Quick Start" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set Airflow Home
$projectRoot = "d:\yogpro\Improve-Your-Hiring-Chance-For-Data-Science-Related-Roles-main"
$env:AIRFLOW_HOME = "$projectRoot\airflow"

Write-Host "Airflow Home: $env:AIRFLOW_HOME" -ForegroundColor Yellow
Write-Host ""

# Check if Airflow is installed
try {
    $airflowVersion = airflow version 2>&1
    Write-Host "✓ Airflow installed: $airflowVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Airflow not installed. Installing now..." -ForegroundColor Red
    pip install apache-airflow apache-airflow-providers-postgres
}

# Initialize Airflow if needed
if (-not (Test-Path "$env:AIRFLOW_HOME\airflow.db")) {
    Write-Host ""
    Write-Host "Initializing Airflow database..." -ForegroundColor Yellow
    airflow db init
    
    Write-Host ""
    Write-Host "Creating admin user..." -ForegroundColor Yellow
    Write-Host "Username: admin" -ForegroundColor Cyan
    Write-Host "Password: admin" -ForegroundColor Cyan
    
    airflow users create `
        --username admin `
        --firstname Admin `
        --lastname User `
        --role Admin `
        --email admin@example.com `
        --password admin
}

# Copy DAG file
Write-Host ""
Write-Host "Copying DAG file..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "$env:AIRFLOW_HOME\dags" | Out-Null
Copy-Item "$projectRoot\dags\dsjobs_dag.py" -Destination "$env:AIRFLOW_HOME\dags\" -Force
Write-Host "✓ DAG file copied" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Airflow..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANT: You need to run the scheduler in a separate terminal!" -ForegroundColor Yellow
Write-Host ""
Write-Host "Open another PowerShell window and run:" -ForegroundColor Cyan
Write-Host "  cd $projectRoot" -ForegroundColor White
Write-Host '  $env:AIRFLOW_HOME = "' + $env:AIRFLOW_HOME + '"' -ForegroundColor White
Write-Host "  airflow scheduler" -ForegroundColor White
Write-Host ""
Write-Host "Access Airflow UI at: http://localhost:8080" -ForegroundColor Green
Write-Host "Login: admin / admin" -ForegroundColor Green
Write-Host ""
Write-Host "Starting Airflow Webserver..." -ForegroundColor Yellow

# Start webserver
airflow webserver --port 8080

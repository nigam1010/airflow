# Automated Data Pipeline Runner
# This script runs the complete data pipeline

$scriptDir = "d:\yogpro\Improve-Your-Hiring-Chance-For-Data-Science-Related-Roles-main\scripts"
$pythonExe = "D:/yogpro/.venv/Scripts/python.exe"
$logFile = "d:\yogpro\Improve-Your-Hiring-Chance-For-Data-Science-Related-Roles-main\pipeline_log.txt"

# Function to log with timestamp
function Write-Log {
    param($Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] $Message"
    Write-Host $logMessage
    Add-Content -Path $logFile -Value $logMessage
}

Write-Log "========================================"
Write-Log "Starting Data Pipeline"
Write-Log "========================================"

# Step 1: Clean scraped data
Write-Log "Step 1/4: Cleaning scraped data..."
try {
    & $pythonExe "$scriptDir\clean_scraped_data.py"
    if ($LASTEXITCODE -eq 0) {
        Write-Log "✓ Data cleaning completed successfully"
    } else {
        Write-Log "✗ Data cleaning failed with exit code $LASTEXITCODE"
        exit 1
    }
} catch {
    Write-Log "✗ Error in data cleaning: $_"
    exit 1
}

# Step 2: Fill domain information (Optional - requires OpenAI API key)
Write-Log "Step 2/4: Filling domain information..."
if ($env:OPENAI_API_KEY) {
    try {
        & $pythonExe "$scriptDir\fill_domain.py"
        if ($LASTEXITCODE -eq 0) {
            Write-Log "✓ Domain filling completed successfully"
        } else {
            Write-Log "⚠ Domain filling failed, continuing anyway..."
        }
    } catch {
        Write-Log "⚠ Error in domain filling (skipping): $_"
    }
} else {
    Write-Log "⚠ OPENAI_API_KEY not set, skipping domain filling"
}

# Step 3: Merge and push data to PostgreSQL
Write-Log "Step 3/4: Loading data to PostgreSQL..."
try {
    & $pythonExe "$scriptDir\merge_push_data_3nf.py"
    if ($LASTEXITCODE -eq 0) {
        Write-Log "✓ Data loading completed successfully"
    } else {
        Write-Log "✗ Data loading failed with exit code $LASTEXITCODE"
        exit 1
    }
} catch {
    Write-Log "✗ Error in data loading: $_"
    exit 1
}

# Step 4: Generate report
Write-Log "Step 4/4: Generating HTML report..."
try {
    & "D:/yogpro/.venv/Scripts/jupyter.exe" nbconvert --to html --execute "$scriptDir\report_3nf.ipynb" --output-dir "$scriptDir\..\output"
    if ($LASTEXITCODE -eq 0) {
        Write-Log "✓ Report generation completed successfully"
        Write-Log "✓ Report saved to: output\report_3nf.html"
    } else {
        Write-Log "✗ Report generation failed with exit code $LASTEXITCODE"
        exit 1
    }
} catch {
    Write-Log "✗ Error in report generation: $_"
    exit 1
}

Write-Log "========================================"
Write-Log "Pipeline completed successfully!"
Write-Log "========================================"
Write-Log ""

# Optional: Open the report in browser
# Start-Process "d:\yogpro\Improve-Your-Hiring-Chance-For-Data-Science-Related-Roles-main\output\report_3nf.html"

# Auto-Run Setup Guide (Windows)

This guide shows you how to automatically run your data pipeline daily using Windows Task Scheduler.

## Quick Setup (2 Steps)

### Step 1: Run the Setup Script

Open PowerShell **as Administrator** and run:

```powershell
cd d:\yogpro\Improve-Your-Hiring-Chance-For-Data-Science-Related-Roles-main
.\setup_auto_run.ps1
```

This will:
- Create a Windows scheduled task
- Configure it to run daily at 2 AM
- Set up logging to `pipeline_log.txt`

### Step 2: Done! 

Your pipeline will now run automatically every day at 2 AM.

## What Gets Run Automatically

The pipeline executes these steps in order:

1. **Clean Data** - `clean_scraped_data.py`
2. **Fill Domains** - `fill_domain.py` (optional, needs OpenAI API key)
3. **Load to Database** - `merge_push_data_3nf.py`
4. **Generate Report** - `report_3nf.ipynb` → `output/report_3nf.html`

## Checking Logs

View the log file to see what happened:

```powershell
Get-Content pipeline_log.txt -Tail 50
```

Or open it in Notepad:

```powershell
notepad pipeline_log.txt
```

## Manual Controls

### Run the Pipeline Now (Manual Test)

```powershell
.\run_pipeline.ps1
```

Or use Task Scheduler:

```powershell
Start-ScheduledTask -TaskName "DataScienceJobsPipeline"
```

### View Scheduled Task

```powershell
Get-ScheduledTask -TaskName "DataScienceJobsPipeline"
```

### Disable Auto-Run

```powershell
Disable-ScheduledTask -TaskName "DataScienceJobsPipeline"
```

### Enable Auto-Run Again

```powershell
Enable-ScheduledTask -TaskName "DataScienceJobsPipeline"
```

### Remove Auto-Run Completely

```powershell
Unregister-ScheduledTask -TaskName "DataScienceJobsPipeline" -Confirm:$false
```

## Changing the Schedule

To change when it runs, open Task Scheduler GUI:

1. Press `Win + R`, type `taskschd.msc`, press Enter
2. Find "DataScienceJobsPipeline" in the task list
3. Right-click → Properties → Triggers → Edit
4. Change the schedule (e.g., weekly, monthly, specific time)

Common schedules:
- **Daily at 2 AM** (default)
- **Weekly on Monday at 9 AM**
- **Monthly on the 1st at midnight**
- **Every 6 hours**

## Setting OpenAI API Key (Optional)

If you want the domain filling step to work, set your API key:

**Temporary (current session only):**
```powershell
$env:OPENAI_API_KEY = "your-api-key-here"
```

**Permanent (system-wide):**
1. Press `Win + X` → System
2. Advanced system settings → Environment Variables
3. Under "User variables", click "New"
4. Variable name: `OPENAI_API_KEY`
5. Variable value: `your-api-key-here`
6. Click OK

## Troubleshooting

### Task not running?

Check if it's enabled:
```powershell
Get-ScheduledTask -TaskName "DataScienceJobsPipeline" | Select-Object State
```

### Check last run result:

```powershell
Get-ScheduledTaskInfo -TaskName "DataScienceJobsPipeline"
```

### PostgreSQL not running?

Make sure PostgreSQL service is running:
```powershell
Get-Service postgresql-x64-18
Start-Service postgresql-x64-18
```

### Permission errors?

Run the setup script as Administrator:
```powershell
Start-Process powershell -Verb RunAs -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"d:\yogpro\Improve-Your-Hiring-Chance-For-Data-Science-Related-Roles-main\setup_auto_run.ps1`""
```

## Advanced: Airflow Alternative

If you prefer using Apache Airflow instead, note that **Airflow doesn't officially support Windows**. You would need to use:

1. **WSL2 (Windows Subsystem for Linux)**
2. **Docker Desktop with Linux containers**
3. **A Linux virtual machine**

For most use cases, the Windows Task Scheduler solution is simpler and works perfectly fine.

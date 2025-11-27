# Project Setup - Data Required

## ⚠️ Missing Data Files

The project is ready to run, but it requires input data files that are not included in the repository.

## Required Data Structure

You need to create a `data/` folder with the following files:

```
data/
├── data_jobs.csv          # Raw scraped job data (required for Step 1)
└── company_domain.csv     # Company industry mapping (created by Step 2)
```

## Required Columns in `data_jobs.csv`:

The CSV should contain these columns:
- `job_title_short` - Short job title (e.g., "Data Scientist")
- `job_title` - Full job title
- `job_location` - Job location
- `job_via` - Job posting source
- `job_schedule_type` - Full-time, Part-time, etc.
- `job_work_from_home` - "True" or "False"
- `search_location` - Search location used
- `job_posted_date` - When job was posted (timestamp)
- `job_no_degree_mention` - "True" or "False"
- `job_health_insurance` - "True" or "False"
- `job_country` - Country
- `salary_year_avg` - Average yearly salary
- `salary_rate` - Rate type
- `salary_hour_avg` - Hourly salary average
- `company_name` - Company name
- `job_skills` - List of skills required
- `job_type_skills` - Skills organized by category (JSON format)

## Where to Get Data?

### Option 1: Use Existing Dataset
If you have job posting data from sources like:
- LinkedIn scrapes
- Indeed scrapes
- Glassdoor data
- Job board APIs

### Option 2: Create Sample Data
Create a small `data/data_jobs.csv` file with sample data for testing:

```powershell
# Create data directory
New-Item -ItemType Directory -Path "data"

# You can use the firstfive.csv as a template if it exists
# or create your own CSV with the columns listed above
```

### Option 3: Web Scraping
Scrape job postings using tools like:
- Selenium
- BeautifulSoup
- Scrapy
- Job board APIs (Indeed, LinkedIn, etc.)

## Once You Have Data:

1. Place `data_jobs.csv` in the `data/` folder
2. Run the pipeline:

```powershell
cd scripts
python clean_scraped_data.py
python fill_domain.py
python merge_push_data_3nf.py
jupyter notebook report_3nf.ipynb
```

## Current Project Status:

✅ All Python scripts created and working
✅ All dependencies installed
✅ Database schema ready
❌ **Need raw data files to proceed**

## Next Steps:

1. Obtain or create `data_jobs.csv` with job posting data
2. Create `data/` directory: `New-Item -ItemType Directory -Path "data"`
3. Place data file in `data/` folder
4. Run the scripts as shown above

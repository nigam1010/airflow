import pandas as pd
import numpy as np

# Read the raw data
df = pd.read_csv('../data/data_jobs.csv')

# Replace empty strings with NaN
df.replace('', np.nan, inplace=True)

# Remove rows where salary_year_avg is NaN
df = df[df['salary_year_avg'].notna()]

# Drop specific columns
df.drop(['salary_rate', 'salary_hour_avg', 'job_title'], axis=1, inplace=True)

# Drop rows with any missing values
df.dropna(inplace=True)

# Clean job_via column - remove 'via' and trim whitespace
df['job_via'] = df['job_via'].str.replace('via', '', case=False).str.strip().str.lower()

# Round salary_year_avg to nearest integer
df['salary_year_avg'] = df['salary_year_avg'].round(0).astype(int)

# Save cleaned data
df.to_csv('../data/data_jobs_cleaned.csv', index=False)

# Create first five rows sample
df_sample = df[df['salary_year_avg'].notna()].head(5)
df_sample.to_csv('./firstfive.csv', index=False)

print("Data cleaning completed successfully!")
print(f"Total rows after cleaning: {len(df)}")

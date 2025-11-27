from openai import OpenAI
import pandas as pd
import ast
import os


# Note: Set your OpenAI API key as an environment variable
# Windows: $env:OPENAI_API_KEY="your-api-key-here"
# Linux/Mac: export OPENAI_API_KEY="your-api-key-here"

client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY")
)


# run chatgpt api service on our query
def get_company_domains_batch(company_names):
    
    # query = (
    #     "For the following companies, identify their industry and return them as a list of industries only:\n\n"
    #     + "\n".join(company_names)
    # )
    query = (
        "For the following company list, identify their industry and return them as a list of industries only:\n\n"
        + "['" + "','".join(company_names) + "']" "\n\n" + "Return only a list"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert in identifying company industries."},
            {"role": "user", "content": query}
        ]
    )
    #convert string response to list
    response_text = response.choices[0].message.content.strip()
    #domains = ast.literal_eval(response_text)
    
    try:
        domains = ast.literal_eval(response_text)
        print(domains)
    except:
        print("chatgpt didnt give a list")
        domains = ['NA']*len(company_names)

    return domains

final_df = pd.DataFrame(columns=['Company','Domain/Industry'])
df = pd.read_csv('../data/data_jobs_cleaned.csv')

frequency_table_df = df['company_name'].value_counts().head(256).reset_index()
frequency_table_df.columns = ['company_name', 'Frequency']

company_list = frequency_table_df['company_name'].tolist()

# give only 10 companies at a time to not exceed token, request limit
chunk_size = 10
for i in range(0, len(company_list), chunk_size):
    chunk = company_list[i:i + chunk_size]
    print(f"Chunk {i // chunk_size + 1}:")

    new_domains = get_company_domains_batch(chunk)

    new_data = pd.DataFrame({
        "Company": chunk,
        "Domain/Industry": new_domains
        })
    final_df = pd.concat([final_df, new_data], ignore_index=True)


print(final_df)

final_df.to_csv('../data/company_domain.csv', index=False)
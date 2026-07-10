"""
Usage Examples - AI GTM Assistant

Practical examples for different use cases and customizations.
"""

# ============================================================================
# EXAMPLE 1: Basic Usage - Running the Streamlit App
# ============================================================================

"""
The simplest way to use this project:

1. Open terminal/command prompt
2. Navigate to project directory
3. Activate virtual environment:
   Windows: venv\Scripts\activate
   macOS/Linux: source venv/bin/activate
4. Run: streamlit run app.py
5. Open http://localhost:8501 in browser
6. Upload CSV and process!
"""

# ============================================================================
# EXAMPLE 2: Using the LeadProcessor Programmatically
# ============================================================================

from lead_processor import LeadProcessor
import pandas as pd

# Initialize processor with your preferred LLM
processor = LeadProcessor(api_choice="Gemini")  # or "OpenAI"

# Create sample data
data = {
    'Company Name': ['TechCorp', 'FinanceInc'],
    'Website': ['techcorp.com', 'financeinc.io']
}
df = pd.DataFrame(data)

# Process all leads
results = processor.process_batch(df)

# Save results
results.to_csv('output.csv', index=False)
print("Processing complete!")
print(results)

# ============================================================================
# EXAMPLE 3: Processing Individual Leads
# ============================================================================

from lead_processor import LeadProcessor

processor = LeadProcessor(api_choice="OpenAI")

# Single lead
lead = {
    'Company Name': 'CloudSolutions',
    'Website': 'cloudsolutions.io'
}

try:
    result = processor.process_lead(lead)
    print(f"Company: {result['Company']}")
    print(f"Industry: {result['Industry']}")
    print(f"Generated Email:\n{result['Generated_Email']}")
except Exception as e:
    print(f"Error: {e}")

# ============================================================================
# EXAMPLE 4: Using EmailGenerator Directly
# ============================================================================

from llm import EmailGenerator

# Initialize with Gemini
generator = EmailGenerator(api_choice="Gemini")

# Generate email for a company
email = generator.generate_email(
    company_name="TechStartup Inc",
    industry="Software Development",
    description="Building innovative AI solutions for businesses"
)

print("Generated Email:")
print(email)

# ============================================================================
# EXAMPLE 5: Using CompanyDataFetcher
# ============================================================================

from api import CompanyDataFetcher

# Initialize fetcher
fetcher = CompanyDataFetcher()

# Fetch company data
company_data = fetcher.fetch_company_data(
    company_name="Acme Corporation",
    website="acme.com"
)

print(f"Company: {company_data['name']}")
print(f"Industry: {company_data['industry']}")
print(f"Size: {company_data['company_size']}")
print(f"Description: {company_data['description']}")

# ============================================================================
# EXAMPLE 6: Custom Email Prompt
# ============================================================================

from llm import EmailGenerator

# Extend EmailGenerator to use custom prompt
class CustomEmailGenerator(EmailGenerator):
    def _build_prompt(self, company_name: str, industry: str, description: str) -> str:
        # Your custom prompt
        prompt = f"""You are a B2B sales expert specializing in {industry}.
        
Write a compelling cold email for {company_name}.

Company Overview:
{description}

Requirements:
- Maximum 100 words
- Include specific industry insight
- Strong call-to-action
- Professional yet personable tone

Email:"""
        return prompt

# Use custom generator
generator = CustomEmailGenerator(api_choice="Gemini")
email = generator.generate_email(
    company_name="DataTech",
    industry="Data Analytics",
    description="Provider of advanced analytics solutions"
)

print(email)

# ============================================================================
# EXAMPLE 7: Batch Processing with Error Handling
# ============================================================================

from lead_processor import LeadProcessor
import pandas as pd

def process_companies_with_logging(csv_file):
    """Process companies from CSV with detailed logging."""
    
    # Read CSV
    df = pd.read_csv(csv_file)
    processor = LeadProcessor(api_choice="OpenAI")
    
    results = []
    errors = []
    
    for idx, row in df.iterrows():
        try:
            print(f"Processing {idx + 1}/{len(df)}: {row['Company Name']}")
            result = processor.process_lead(row)
            results.append(result)
            print(f"  ✓ Success")
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            errors.append({
                'company': row['Company Name'],
                'error': str(e)
            })
    
    # Create results dataframe
    results_df = pd.DataFrame(results)
    
    # Print summary
    print("\n" + "="*50)
    print("PROCESSING SUMMARY")
    print("="*50)
    print(f"Total: {len(df)}")
    print(f"Success: {len(results)}")
    print(f"Errors: {len(errors)}")
    print(f"Success Rate: {len(results)/len(df)*100:.1f}%")
    
    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"  - {error['company']}: {error['error']}")
    
    return results_df, errors

# Usage
# results, errors = process_companies_with_logging('companies.csv')
# results.to_csv('output.csv', index=False)

# ============================================================================
# EXAMPLE 8: Data Validation
# ============================================================================

from utils import validate_csv
import pandas as pd

# Load and validate CSV
df = pd.read_csv('companies.csv')

validation = validate_csv(df)

if validation['valid']:
    print("✓ CSV is valid!")
else:
    print(f"✗ Validation error: {validation['message']}")

# ============================================================================
# EXAMPLE 9: Using Mock Data for Testing
# ============================================================================

from api import CompanyDataFetcher

# This automatically uses mock data if Clearbit API key not available
fetcher = CompanyDataFetcher()

# Perfect for testing without API keys
companies = [
    'TechStarrup Inc',
    'FinTech Solutions',
    'Healthcare Innovations'
]

for company in companies:
    data = fetcher.fetch_company_data(company, f'{company.lower().replace(" ", "")}.com')
    print(f"{company}: {data['industry']}")

# ============================================================================
# EXAMPLE 10: Customizing Configuration
# ============================================================================

# In config.py, you can adjust:

# Email generation settings
EMAIL_MAX_WORDS = 150  # Increase from 120
EMAIL_TEMPERATURE = 0.8  # More creative (0-1, default 0.7)
EMAIL_MAX_TOKENS = 250  # More tokens for longer emails

# API settings
API_TIMEOUT = 15  # Increase timeout from 10 seconds
API_RETRY_ATTEMPTS = 5  # More retry attempts

# File upload settings
MAX_FILE_SIZE_MB = 100  # Increase from 50 MB

# Then use in code:
from config import EMAIL_MAX_WORDS, EMAIL_TEMPERATURE

# ============================================================================
# EXAMPLE 11: Exporting Results in Different Formats
# ============================================================================

import pandas as pd

# Assuming you have processed results
results_df = pd.DataFrame([...])  # Your results

# Export as CSV
results_df.to_csv('output.csv', index=False)

# Export as Excel (requires openpyxl)
# results_df.to_excel('output.xlsx', index=False)

# Export as JSON
results_df.to_json('output.json', orient='records')

# Export specific columns
results_df[['Company', 'Generated_Email']].to_csv('emails_only.csv', index=False)

# ============================================================================
# EXAMPLE 12: Creating Custom Reports
# ============================================================================

import pandas as pd

# Create industry analysis
def generate_industry_report(results_df):
    """Generate report grouped by industry."""
    
    report = results_df.groupby('Industry').agg({
        'Company': 'count',
        'Company_Size': 'first'
    }).rename(columns={'Company': 'Count'})
    
    print("INDUSTRY ANALYSIS")
    print(report)
    
    return report

# Usage
# results_df = pd.read_csv('processed_leads.csv')
# industry_report = generate_industry_report(results_df)

# ============================================================================
# EXAMPLE 13: Testing with Different LLM Models
# ============================================================================

from llm import EmailGenerator

# Test both models
models = {
    'OpenAI': 'GPT-3.5 Turbo',
    'Gemini': 'Google Gemini Pro'
}

company_info = {
    'company_name': 'InnovateHub',
    'industry': 'Technology',
    'description': 'Building next-gen business solutions'
}

for api_choice, model_name in models.items():
    try:
        generator = EmailGenerator(api_choice=api_choice)
        email = generator.generate_email(**company_info)
        print(f"\n{model_name}:")
        print(email)
    except Exception as e:
        print(f"\n{model_name}: Error - {e}")

# ============================================================================
# EXAMPLE 14: Scheduling Batch Processing (Pseudocode)
# ============================================================================

"""
# To run batch processing on a schedule (requires 'schedule' library):
# pip install schedule

import schedule
import time
from lead_processor import LeadProcessor
import pandas as pd

def process_daily():
    '''Process companies daily at 9 AM'''
    df = pd.read_csv('leads.csv')
    processor = LeadProcessor(api_choice="Gemini")
    results = processor.process_batch(df)
    results.to_csv(f'output_{datetime.now().date()}.csv')
    print("Daily processing complete!")

# Schedule the job
schedule.every().day.at("09:00").do(process_daily)

# Keep running
while True:
    schedule.run_pending()
    time.sleep(60)
"""

# ============================================================================
# EXAMPLE 15: Performance Tips
# ============================================================================

"""
PERFORMANCE OPTIMIZATION TIPS:

1. Batch Processing:
   - Process multiple companies at once
   - More efficient than one-by-one

2. Caching:
   - Cache API responses to avoid duplicates
   - Implement in api.py

3. Async Processing:
   - Use asyncio for parallel processing
   - Can process 10+ companies simultaneously

4. Error Handling:
   - Skip failed records, continue processing
   - Don't retry immediately, use backoff

5. API Optimization:
   - Use batch endpoints if available
   - Reuse connections
   - Implement rate limiting

6. Data Optimization:
   - Clean data before processing
   - Remove duplicates
   - Use efficient file formats

7. Memory Management:
   - Process in chunks for large files
   - Don't load entire dataset in memory
"""

# ============================================================================
# Common Patterns Summary
# ============================================================================

"""
QUICK REFERENCE:

1. Run the app:
   $ streamlit run app.py

2. Process CSV programmatically:
   processor = LeadProcessor()
   results = processor.process_batch(df)

3. Generate single email:
   generator = EmailGenerator()
   email = generator.generate_email(name, industry, description)

4. Fetch company data:
   fetcher = CompanyDataFetcher()
   data = fetcher.fetch_company_data(name, website)

5. Validate CSV:
   from utils import validate_csv
   is_valid = validate_csv(df)

6. Export results:
   results.to_csv('output.csv')
   
Remember: Always activate virtual environment first!
"""

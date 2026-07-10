"""
Lead Processor Module

Handles the core logic for:
- Processing company leads
- Fetching company data from APIs
- Generating personalized emails using LLM
"""

import pandas as pd
from api import CompanyDataFetcher
from llm import EmailGenerator
from utils import sanitize_data


class LeadProcessor:
    """
    Main processor class for handling lead enrichment and email generation.
    
    Attributes:
        api_fetcher: CompanyDataFetcher instance for fetching company data
        email_generator: EmailGenerator instance for generating personalized emails
    """
    
    def __init__(self, api_choice: str = "Gemini"):
        """
        Initialize the LeadProcessor.
        
        Args:
            api_choice: "OpenAI" or "Gemini" for LLM selection
        """
        self.api_fetcher = CompanyDataFetcher()
        self.email_generator = EmailGenerator(api_choice=api_choice)
    
    def process_lead(self, lead_row) -> dict:
        """
        Process a single lead by fetching data and generating personalized email.
        
        Args:
            lead_row: Pandas Series containing 'Company Name' and 'Website'
        
        Returns:
            Dictionary with processed lead data
        
        Raises:
            Exception: If processing fails for any reason
        """
        company_name = lead_row.get('Company Name', '')
        website = lead_row.get('Website', '')
        
        if not company_name or not website:
            raise ValueError("Missing 'Company Name' or 'Website'")
        
        # Fetch company data
        company_data = self.api_fetcher.fetch_company_data(company_name, website)
        
        # Generate personalized email
        email = self.email_generator.generate_email(
            company_name=company_data.get('name', company_name),
            industry=company_data.get('industry', 'Unknown'),
            description=company_data.get('description', 'No description available')
        )
        
        # Compile result
        result = {
            'Company': sanitize_data(company_data.get('name', company_name)),
            'Website': sanitize_data(website),
            'Industry': sanitize_data(company_data.get('industry', 'Unknown')),
            'Description': sanitize_data(company_data.get('description', '')),
            'Company_Size': sanitize_data(company_data.get('company_size', 'Unknown')),
            'Generated_Email': sanitize_data(email)
        }
        
        return result
    
    def process_batch(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process multiple leads at once.
        
        Args:
            df: Pandas DataFrame with company data
        
        Returns:
            DataFrame with processed results
        """
        results = []
        errors = []
        
        for idx, row in df.iterrows():
            try:
                result = self.process_lead(row)
                results.append(result)
            except Exception as e:
                errors.append({
                    'Company': row.get('Company Name', 'Unknown'),
                    'Error': str(e)
                })
        
        results_df = pd.DataFrame(results)
        
        if errors:
            print(f"Processed with {len(errors)} errors")
            for error in errors:
                print(f"  - {error['Company']}: {error['Error']}")
        
        return results_df

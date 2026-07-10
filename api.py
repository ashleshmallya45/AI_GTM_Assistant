"""
API Module - Company Data Fetching

Handles fetching company information from various sources.
Currently uses mock data as fallback; can be extended with real APIs like Clearbit.
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class CompanyDataFetcher:
    """
    Fetch company data from APIs.
    
    Supports:
    - Clearbit API (if key available)
    - Mock/fallback data for demo purposes
    """
    
    def __init__(self):
        """Initialize the data fetcher."""
        self.clearbit_api_key = os.getenv("CLEARBIT_API_KEY")
    
    def fetch_company_data(self, company_name: str, website: str) -> dict:
        """
        Fetch company data using available APIs.
        
        Falls back to mock data if no API key is available.
        
        Args:
            company_name: Name of the company
            website: Website URL of the company
        
        Returns:
            Dictionary with company information:
            - name
            - industry
            - description
            - company_size
        """
        
        # Try Clearbit API if available
        if self.clearbit_api_key:
            try:
                data = self._fetch_from_clearbit(website)
                if data:
                    return data
            except Exception as e:
                print(f"Clearbit API error for {company_name}: {str(e)}")
        
        # Fallback to enriched mock data based on company name
        return self._get_mock_data(company_name, website)
    
    def _fetch_from_clearbit(self, website: str) -> dict:
        """
        Fetch company data from Clearbit API.
        
        Args:
            website: Company website URL
        
        Returns:
            Dictionary with company data or None
        """
        try:
            url = f"https://company.clearbit.com/v1/companies/find?domain={website}"
            headers = {"Authorization": f"Bearer {self.clearbit_api_key}"}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'name': data.get('name', ''),
                    'industry': data.get('industryTag', {}).get('category', 'Unknown'),
                    'description': data.get('description', ''),
                    'company_size': data.get('metrics', {}).get('employees', 'Unknown')
                }
        except Exception as e:
            print(f"Error fetching from Clearbit: {str(e)}")
        
        return None
    
    def _get_mock_data(self, company_name: str, website: str) -> dict:
        """
        Get mock company data for demonstration.
        
        This is useful for testing without API keys.
        
        Args:
            company_name: Name of the company
            website: Website URL
        
        Returns:
            Dictionary with mock company data
        """
        
        # Sample database of companies for demo purposes
        mock_companies = {
            "techstartup": {
                "industry": "Software Development",
                "description": "An innovative tech startup building next-generation software solutions",
                "company_size": "50-100"
            },
            "fintech": {
                "industry": "Financial Technology",
                "description": "Revolutionizing financial services with cutting-edge technology",
                "company_size": "100-500"
            },
            "healthcare": {
                "industry": "Healthcare Technology",
                "description": "Transforming healthcare through digital innovation and AI",
                "company_size": "200-1000"
            },
            "ecommerce": {
                "industry": "E-commerce",
                "description": "Leading online retail and marketplace solutions provider",
                "company_size": "500-5000"
            },
            "marketing": {
                "industry": "Marketing & Advertising",
                "description": "Digital marketing platform for data-driven campaigns",
                "company_size": "50-200"
            },
            "analytics": {
                "industry": "Data & Analytics",
                "description": "Advanced business intelligence and data analytics solutions",
                "company_size": "100-500"
            }
        }
        
        # Try to find a matching company by keyword
        company_lower = company_name.lower()
        for key, data in mock_companies.items():
            if key in company_lower:
                return {
                    'name': company_name,
                    'industry': data['industry'],
                    'description': data['description'],
                    'company_size': data['company_size']
                }
        
        # Default mock data
        return {
            'name': company_name,
            'industry': 'Technology',
            'description': f'{company_name} is an innovative company operating in the digital space, delivering value to customers worldwide.',
            'company_size': '100-500'
        }

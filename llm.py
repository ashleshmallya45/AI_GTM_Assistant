"""
LLM Module - Email Generation

Handles integration with OpenAI and Google Gemini APIs
for generating personalized outreach emails.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class EmailGenerator:
    """
    Generate personalized cold emails using LLM APIs.
    
    Supports both OpenAI and Google Gemini APIs.
    """
    
    def __init__(self, api_choice: str = "Gemini"):
        """
        Initialize the EmailGenerator.
        
        Args:
            api_choice: "OpenAI" or "Gemini"
        
        Raises:
            ValueError: If API choice is invalid or API key is missing
        """
        self.api_choice = api_choice
        
        if api_choice == "OpenAI":
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY not found in .env file")
            self._init_openai()
        
        elif api_choice == "Gemini":
            self.api_key = os.getenv("GEMINI_API_KEY")
            if not self.api_key:
                raise ValueError("GEMINI_API_KEY not found in .env file")
            self._init_gemini()
        
        else:
            raise ValueError(f"Invalid API choice: {api_choice}. Use 'OpenAI' or 'Gemini'")
    
    def _init_openai(self):
        """Initialize OpenAI client."""
        try:
            import openai
            openai.api_key = self.api_key
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
    
    def _init_gemini(self):
        """Initialize Google Gemini client."""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        except ImportError:
            raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")
    
    def generate_email(self, company_name: str, industry: str, description: str) -> str:
        """
        Generate a personalized cold email for a company.
        
        Args:
            company_name: Name of the company
            industry: Industry of the company
            description: Brief description of the company
        
        Returns:
            Generated personalized email
        
        Raises:
            Exception: If API call fails
        """
        prompt = self._build_prompt(company_name, industry, description)
        
        if self.api_choice == "OpenAI":
            return self._generate_openai(prompt)
        else:
            return self._generate_gemini(prompt)
    
    def _build_prompt(self, company_name: str, industry: str, description: str) -> str:
        """
        Build the prompt for LLM.
        
        Args:
            company_name: Name of the company
            industry: Industry of the company
            description: Brief description of the company
        
        Returns:
            Formatted prompt string
        """
        prompt = f"""You are an experienced Sales Development Representative (SDR). 
Write a short, personalized outreach email for the following company.

Company: {company_name}
Industry: {industry}
Description: {description}

Requirements:
- Keep it professional and under 120 words
- Include one personalized compliment based on the company info
- Make it compelling and engaging
- Use a friendly but professional tone
- Include a clear call-to-action
- Avoid generic templates

Email:"""
        return prompt
    
    def _generate_openai(self, prompt: str) -> str:
        """
        Generate email using OpenAI API.
        
        Args:
            prompt: The prompt to send to OpenAI
        
        Returns:
            Generated email text
        """
        try:
            import openai
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert SDR writing personalized cold emails."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            return response['choices'][0]['message']['content'].strip()
        
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def _generate_gemini(self, prompt: str) -> str:
        """
        Generate email using Google Gemini API.
        
        Args:
            prompt: The prompt to send to Gemini
        
        Returns:
            Generated email text
        """
        try:
            response = self.gemini_model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "max_output_tokens": 200,
                }
            )
            
            if response and response.text:
                return response.text.strip()
            else:
                return self._generate_mock_email()
        
        except Exception as e:
            print(f"Gemini API error: {str(e)}")
            return self._generate_mock_email()
    
    def _generate_mock_email(self) -> str:
        """Generate a mock email as fallback."""
        return """Hi there,

I came across your company and was impressed by your innovative approach to solving industry challenges.

I'd love to explore how we can collaborate and create mutual value.

Looking forward to connecting!

Best regards"""

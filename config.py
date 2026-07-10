"""
Configuration Module

Central place for all configurable parameters.
"""

# API Configuration
API_TIMEOUT = 10  # seconds
API_RETRY_ATTEMPTS = 3

# Email Generation
EMAIL_MAX_WORDS = 120
EMAIL_TEMPERATURE = 0.7
EMAIL_MAX_TOKENS = 200

# LLM Models
OPENAI_MODEL = "gpt-3.5-turbo"
GEMINI_MODEL = "gemini-1.5-flash"

# Data Processing
BATCH_SIZE = 10
MAX_COMPANIES_PER_BATCH = 100

# UI Configuration
STREAMLIT_PAGE_TITLE = "AI Lead Generation Assistant"
STREAMLIT_PAGE_ICON = "🤖"
STREAMLIT_LAYOUT = "wide"

# Display Limits
MAX_DESCRIPTION_LENGTH = 500
MAX_EMAIL_DISPLAY_LENGTH = 2000

# File Upload
MAX_FILE_SIZE_MB = 50
ALLOWED_FILE_TYPES = ["csv"]

# Clearbit API
CLEARBIT_DOMAIN_CONFIDENCE_MIN = 0.8
CLEARBIT_TIMEOUT = 10

# Mock Data Configuration
USE_MOCK_DATA_FALLBACK = True
MOCK_DATA_ENRICHMENT = True

# Logging
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "app.log"

# Cache Configuration
ENABLE_CACHE = True
CACHE_TTL_SECONDS = 3600  # 1 hour

# Error Messages
ERROR_MESSAGES = {
    "MISSING_API_KEY": "API key not found. Please configure your .env file.",
    "INVALID_CSV": "CSV format is invalid. Please check required columns.",
    "PROCESSING_ERROR": "Error processing company. Please try again.",
    "API_ERROR": "API request failed. Please check your configuration.",
}

# Success Messages
SUCCESS_MESSAGES = {
    "PROCESSING_COMPLETE": "Successfully processed all companies!",
    "DOWNLOAD_READY": "Data is ready to download.",
    "CSV_VALID": "CSV file is valid and ready for processing.",
}

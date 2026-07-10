"""
Utility Functions Module

Helper functions for:
- Data validation
- Data sanitization
- UI feedback (success/error messages)
- General utilities
"""

import pandas as pd
import streamlit as st
from typing import Dict, List


def validate_csv(df: pd.DataFrame) -> Dict:
    """
    Validate that the CSV has required columns.
    
    Args:
        df: Pandas DataFrame to validate
    
    Returns:
        Dictionary with 'valid' (bool) and 'message' (str)
    """
    required_columns = ['Company Name', 'Website']
    
    if df.empty:
        return {
            'valid': False,
            'message': "CSV file is empty"
        }
    
    # Check for required columns (case-insensitive)
    df_columns = [col.lower() for col in df.columns]
    required_lower = [col.lower() for col in required_columns]
    
    missing_columns = [col for col in required_lower if col not in df_columns]
    
    if missing_columns:
        return {
            'valid': False,
            'message': f"Missing required columns: {', '.join(missing_columns)}. Required columns: {', '.join(required_columns)}"
        }
    
    # Check for empty cells in required columns
    required_mapped = {}
    for col in df.columns:
        if col.lower() in required_lower:
            required_mapped[col.lower()] = col
    
    for col_lower, col_actual in required_mapped.items():
        empty_count = df[col_actual].isna().sum()
        if empty_count > 0:
            return {
                'valid': False,
                'message': f"Column '{col_actual}' has {empty_count} empty cells"
            }
    
    return {
        'valid': True,
        'message': 'CSV is valid'
    }


def sanitize_data(data) -> str:
    """
    Sanitize data for safe display.
    
    Args:
        data: Data to sanitize (any type)
    
    Returns:
        Sanitized string representation
    """
    if data is None:
        return "N/A"
    
    # Convert to string and strip whitespace
    sanitized = str(data).strip()
    
    # Remove extra whitespace
    sanitized = ' '.join(sanitized.split())
    
    # Limit length for display
    max_length = 500
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length] + "..."
    
    return sanitized


def show_success_message(message: str) -> None:
    """
    Display a success message in Streamlit.
    
    Args:
        message: Message to display
    """
    st.markdown(f'<div class="success-box">{message}</div>', unsafe_allow_html=True)
    st.success(message)


def show_error_message(message: str) -> None:
    """
    Display an error message in Streamlit.
    
    Args:
        message: Error message to display
    """
    st.markdown(f'<div class="error-box">{message}</div>', unsafe_allow_html=True)
    st.error(message)


def show_warning_message(message: str) -> None:
    """
    Display a warning message in Streamlit.
    
    Args:
        message: Warning message to display
    """
    st.warning(message)


def format_csv_for_download(df: pd.DataFrame) -> bytes:
    """
    Convert DataFrame to CSV bytes for download.
    
    Args:
        df: Pandas DataFrame to convert
    
    Returns:
        CSV data as bytes
    """
    from io import BytesIO
    
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    
    return buffer.getvalue()


def validate_email_format(email: str) -> bool:
    """
    Basic validation for email format.
    
    Args:
        email: Email string to validate
    
    Returns:
        True if email format is valid, False otherwise
    """
    import re
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def clean_company_name(name: str) -> str:
    """
    Clean and normalize company name.
    
    Args:
        name: Company name to clean
    
    Returns:
        Cleaned company name
    """
    # Remove extra whitespace
    cleaned = ' '.join(name.split())
    
    # Remove trailing/leading special characters
    cleaned = cleaned.strip('.,!?;:')
    
    return cleaned


def extract_domain_from_url(url: str) -> str:
    """
    Extract domain name from URL.
    
    Args:
        url: URL string
    
    Returns:
        Domain name
    """
    from urllib.parse import urlparse
    
    try:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        
        # Remove 'www.'
        if domain.startswith('www.'):
            domain = domain[4:]
        
        return domain
    except:
        return url


def get_file_size(file_path: str) -> str:
    """
    Get human-readable file size.
    
    Args:
        file_path: Path to file
    
    Returns:
        Human-readable file size string
    """
    import os
    
    try:
        size_bytes = os.path.getsize(file_path)
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        
        return f"{size_bytes:.2f} TB"
    except:
        return "Unknown"


def log_processing_event(event_type: str, details: str) -> None:
    """
    Log processing events for debugging.
    
    Args:
        event_type: Type of event (e.g., 'SUCCESS', 'ERROR', 'WARNING')
        details: Event details
    """
    import datetime
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {event_type}: {details}"
    
    # In a production app, this would write to a file
    # For now, it's just printed
    print(log_message)

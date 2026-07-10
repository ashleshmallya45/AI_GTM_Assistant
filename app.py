"""
Main Streamlit Application for AI Lead Generation & Personalized Outreach Assistant

This module provides a web interface for:
- Uploading CSV files with company data
- Processing companies through enrichment and email generation
- Displaying results in an interactive table
- Downloading the processed data as CSV
"""

import streamlit as st
import pandas as pd
from io import BytesIO
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lead_processor import LeadProcessor
from utils import validate_csv, show_success_message, show_error_message

# Configure Streamlit page
st.set_page_config(
    page_title="AI Lead Generation Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #28a745;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #dc3545;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "processed_df" not in st.session_state:
    st.session_state.processed_df = None
if "processing_complete" not in st.session_state:
    st.session_state.processing_complete = False

# Main header
st.markdown("""
<div class="main-header">
    <h1>🤖 AI Lead Generation & Outreach Assistant</h1>
    <p>Automatically enrich company data and generate personalized cold emails</p>
</div>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    api_choice = st.radio(
        "Select LLM API",
        ["OpenAI", "Gemini"],
        help="Choose which LLM API to use for email generation"
    )
    
    st.divider()
    
    st.subheader("📋 Instructions")
    with st.expander("How to use this app", expanded=False):
        st.markdown("""
        1. **Prepare your CSV** with columns: Company Name, Website
        2. **Upload the file** using the uploader below
        3. **Configure API** settings on the left
        4. **Click Process** to enrich data and generate emails
        5. **Download results** as CSV
        
        **Note:** Ensure you have API keys configured in your `.env` file
        """)
    
    st.divider()
    
    # API Key reminder
    st.warning("⚠️ Make sure your API keys are configured in `.env` file")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📤 Upload CSV File")
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file with company data",
        type=["csv"],
        help="CSV should have 'Company Name' and 'Website' columns"
    )
    
    if uploaded_file is not None:
        # Read and display uploaded file
        df_input = pd.read_csv(uploaded_file)
        
        st.subheader("📊 Preview of Uploaded Data")
        st.dataframe(df_input, use_container_width=True)
        
        # Validate CSV
        validation_result = validate_csv(df_input)
        
        if not validation_result["valid"]:
            show_error_message(validation_result["message"])
        else:
            # Process button
            if st.button("🚀 Process Companies", use_container_width=True):
                with st.spinner("Processing... This may take a few moments."):
                    try:
                        processor = LeadProcessor(api_choice=api_choice)
                        
                        # Progress bar
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Process leads
                        results = []
                        for idx, row in df_input.iterrows():
                            status_text.text(f"Processing {idx + 1}/{len(df_input)}: {row['Company Name']}")
                            progress = (idx + 1) / len(df_input)
                            progress_bar.progress(progress)
                            
                            try:
                                result = processor.process_lead(row)
                                results.append(result)
                            except Exception as e:
                                st.warning(f"Error processing {row['Company Name']}: {str(e)}")
                                continue
                        
                        # Store results in session state
                        st.session_state.processed_df = pd.DataFrame(results)
                        st.session_state.processing_complete = True
                        
                        progress_bar.empty()
                        status_text.empty()
                        
                        show_success_message(f"✅ Successfully processed {len(results)}/{len(df_input)} companies!")
                        
                    except Exception as e:
                        show_error_message(f"❌ Error during processing: {str(e)}")

# Display results if available
if st.session_state.processing_complete and st.session_state.processed_df is not None:
    st.divider()
    st.header("📈 Results")
    
    df_results = st.session_state.processed_df
    
    # Display statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Companies Processed", len(df_results))
    with col2:
        success_rate = (len(df_results) / len(df_results) * 100) if len(df_results) > 0 else 0
        st.metric("Success Rate", f"{success_rate:.1f}%")
    with col3:
        industries = df_results['Industry'].nunique() if len(df_results) > 0 else 0
        st.metric("Industries Found", industries)
    
    st.divider()
    
    # Display results table
    st.subheader("📋 Processed Companies")
    
    # Create display dataframe with formatted columns
    if len(df_results) > 0 and 'Company' in df_results.columns:
        display_df = df_results[['Company', 'Industry', 'Description', 'Generated_Email']].copy()
        display_df['Description'] = display_df['Description'].apply(
            lambda x: x[:100] + "..." if len(str(x)) > 100 else x
        )
    else:
        display_df = df_results.copy() if len(df_results) > 0 else pd.DataFrame()
    
    st.dataframe(display_df, use_container_width=True, height=400)
    
    # Download button
    st.subheader("💾 Download Results")
    
    csv_buffer = BytesIO()
    df_results.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
    st.download_button(
        label="📥 Download as CSV",
        data=csv_buffer.getvalue(),
        file_name="processed_leads.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    # Show detailed view option
    if len(df_results) > 0:
        with st.expander("📝 View Full Emails"):
            for idx, row in df_results.iterrows():
                with st.container():
                    company = row.get('Company', 'Unknown')
                    industry = row.get('Industry', 'N/A')
                    description = row.get('Description', 'N/A')
                    email = row.get('Generated_Email', 'No email generated')
                    company_size = row.get('Company_Size', 'N/A')
                    
                    st.subheader(f"Company: {company}")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Industry:** {industry}")
                    with col2:
                        st.write(f"**Size:** {company_size}")
                    
                    st.write("**Description:**")
                    st.write(description)
                    
                    st.write("**Generated Email:**")
                    st.info(email)
                    st.divider()

else:
    # Empty state
    if uploaded_file is None:
        st.info("👆 Upload a CSV file to get started!")
    else:
        st.info("👆 Click 'Process Companies' to generate personalized emails")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px; margin-top: 30px;'>
    <p>AI Lead Generation & Outreach Assistant | Built with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)

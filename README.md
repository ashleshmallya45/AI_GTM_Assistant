# 🤖 AI Lead Generation & Personalized Outreach Assistant

An intelligent, professional-grade GTM (Go-To-Market) automation tool that automatically enriches company data and generates personalized cold emails using AI.

## 🌟 Features

### Core Capabilities
- **📤 CSV Upload**: Upload company lists with minimal data (name and website)
- **🔍 Company Enrichment**: Automatically fetch company details including:
  - Industry classification
  - Company description
  - Company size
  - Additional metadata
  
- **🤖 AI-Powered Email Generation**: Generate personalized cold emails using:
  - **OpenAI GPT-3.5 Turbo** for advanced language understanding
  - **Google Gemini** as an alternative LLM provider
  - Customizable prompts for different use cases

- **📊 Beautiful Dashboard**: Interactive Streamlit interface featuring:
  - Real-time processing with progress indicators
  - Data preview and statistics
  - Formatted result tables

- **💾 Export Functionality**:
  - Download processed results as CSV
  - Full email content preview
  - Detailed company information

### API Integration
- **Clearbit API** (optional): Enterprise-grade company data enrichment
- **Fallback Mock Data**: Fully functional demo without API keys
- **Error Handling**: Graceful degradation if APIs fail

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit |
| **Data Processing** | Pandas |
| **LLM APIs** | OpenAI, Google Gemini |
| **Company Data** | Clearbit API (optional) |
| **Language** | Python 3.8+ |
| **Configuration** | python-dotenv (.env files) |

## 📋 Project Structure

```
AI_GTM_Assistant/
│
├── app.py                    # Main Streamlit application
├── lead_processor.py         # Core lead processing logic
├── llm.py                    # LLM integration (OpenAI & Gemini)
├── api.py                    # Company data fetching
├── utils.py                  # Utility functions & helpers
│
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── sample_leads.csv         # Sample data for testing
│
└── README.md                # This file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- At least one API key:
  - OpenAI API key (from https://platform.openai.com/api-keys)
  - OR Google Gemini API key (from https://ai.google.dev/)

### Step 1: Clone/Download the Project
```bash
# Navigate to the project directory
cd AI_GTM_Assistant
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure API Keys
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your API keys
# Windows:
notepad .env
# macOS/Linux:
nano .env
```

**Environment Variables Required:**
```env
# Choose one (or both):
OPENAI_API_KEY=sk-your-key-here
GEMINI_API_KEY=your-gemini-key-here

# Optional:
CLEARBIT_API_KEY=your-clearbit-key-here
```

### Step 5: Run the Application
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## 📖 How to Use

### Basic Workflow

1. **Prepare Your Data**
   - Create a CSV file with two columns:
     - `Company Name`: Name of the company
     - `Website`: Company website URL
   - Example provided in `sample_leads.csv`

2. **Upload CSV**
   - Click the "Choose a CSV file" button
   - Select your CSV file
   - Preview the data

3. **Configure LLM**
   - Select your preferred LLM provider (OpenAI or Gemini)
   - Ensure API key is configured in `.env`

4. **Process Companies**
   - Click "🚀 Process Companies" button
   - Watch real-time progress with loading indicators

5. **Review Results**
   - View enriched data in the results table
   - Expand "View Full Emails" to read complete emails
   - Check company details and statistics

6. **Export Data**
   - Click "📥 Download as CSV" button
   - Use the processed data in your CRM or outreach tool

### Example CSV Format

```csv
Company Name,Website
Acme Corporation,acme.com
TechInnovate,techinnovate.io
Global Retail Inc,globalretail.com
```

### Generated Output

The system generates a CSV with:
```
Company | Website | Industry | Description | Company_Size | Generated_Email
--------|---------|----------|-------------|------|----------------
```

## 🏗 Project Architecture

### Application Flow

```
┌─────────────────┐
│   CSV Upload    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Validation     │◄──── validate_csv()
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│  Lead Processor      │
│  (for each company)  │
└────────┬─────────────┘
         │
         ├─────────────────┐
         │                 │
         ▼                 ▼
┌──────────────────┐  ┌─────────────────┐
│ Company Data     │  │ Email Generator │
│ Fetcher (API)    │  │ (LLM)           │
│ - Clearbit       │  │ - OpenAI/Gemini │
│ - Mock Data      │  │ - Personalized  │
└────────┬─────────┘  │   Emails        │
         │            └────────┬────────┘
         │                     │
         └──────────┬──────────┘
                    │
                    ▼
           ┌─────────────────┐
           │  Results DF     │
           │  (Enriched)     │
           └────────┬────────┘
                    │
                    ▼
           ┌─────────────────┐
           │  Display Table  │
           │  & Download CSV │
           └─────────────────┘
```

### Key Components

#### `app.py` - Streamlit Frontend
- User interface and interactions
- File upload handling
- Results display and visualization
- Download functionality

#### `lead_processor.py` - Core Logic
- Orchestrates the enrichment process
- Processes individual leads and batches
- Aggregates results

#### `llm.py` - AI Email Generation
- Integrates with OpenAI and Gemini APIs
- Builds contextual prompts
- Handles API authentication and error handling

#### `api.py` - Company Data Fetching
- Fetchescompany information
- Supports Clearbit API (if available)
- Provides intelligent fallback to mock data

#### `utils.py` - Utility Functions
- Data validation
- Data sanitization
- UI helper functions
- General utilities

## 🔧 Configuration & Customization

### Change LLM Provider
The app supports both OpenAI and Gemini. Select in the sidebar or modify:

```python
processor = LeadProcessor(api_choice="OpenAI")  # or "Gemini"
```

### Customize Email Prompt
Edit the prompt in `llm.py` function `_build_prompt()`:

```python
def _build_prompt(self, company_name, industry, description):
    prompt = f"""Your custom prompt here..."""
    return prompt
```

### Add New Data Sources
Extend `api.py` to add new data sources:

```python
def _fetch_from_new_api(self, website):
    # Your implementation here
    pass
```

### Modify Mock Data
Update the `mock_companies` dictionary in `api.py` to customize demo data.

## 🚨 Error Handling

The system handles common errors gracefully:

- **Missing API Keys**: Shows clear error messages and instructions
- **Invalid CSV**: Validates format and provides specific feedback
- **API Failures**: Attempts fallback or skips failed records
- **Rate Limiting**: Implements retry logic with backoff

## 📊 Performance & Scalability

- **Current**: Processes 100-500 leads efficiently
- **Batch Processing**: Supports sequential processing with progress tracking
- **Async Ready**: Architecture supports async/await for better performance
- **Error Recovery**: Continues processing even if individual leads fail

## 🎓 Educational Value

This project demonstrates:
- ✅ Clean, modular Python architecture
- ✅ RESTful API integration
- ✅ LLM/AI API usage patterns
- ✅ Data validation and sanitization
- ✅ Streamlit for rapid prototyping
- ✅ Environment variable management
- ✅ Error handling best practices
- ✅ Professional UI/UX patterns

## 🔐 Security Best Practices

- ✅ API keys stored in `.env` (never in code)
- ✅ No sensitive data logged
- ✅ Input validation and sanitization
- ✅ Error messages don't expose system details
- ✅ HTTPS for API calls

## 🚀 Future Improvements

### Phase 2 - Advanced Features
- [ ] Multi-language support for email generation
- [ ] Custom email templates
- [ ] A/B testing different email variations
- [ ] Integration with email sending platforms (SendGrid, etc.)
- [ ] Analytics dashboard for email performance

### Phase 3 - Enterprise Features
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] User authentication and team management
- [ ] Campaign management and tracking
- [ ] Webhook support for CRM integration
- [ ] API rate limiting and caching
- [ ] Detailed audit logs

### Phase 4 - AI Enhancements
- [ ] Fine-tuned models for specific industries
- [ ] Sentiment analysis of generated emails
- [ ] Real-time company research integration
- [ ] Dynamic prompt optimization
- [ ] Multi-language company data enrichment

### Performance
- [ ] Async processing for faster execution
- [ ] Redis caching for API responses
- [ ] Bulk processing optimizations
- [ ] Database indexing strategies

## 📝 Example Workflow

### Input CSV
```
Company Name,Website
CloudTech Solutions,cloudtech.io
DataViz Pro,dataviz-pro.com
```

### Processing
```
Processing 1/2: CloudTech Solutions
├─ Fetched: Industry=Cloud Computing, Size=100-500
├─ Generated: Personalized email with 105 words
✓ Completed

Processing 2/2: DataViz Pro
├─ Fetched: Industry=Data Analytics, Size=50-100
├─ Generated: Personalized email with 112 words
✓ Completed
```

### Output
| Company | Website | Industry | Generated_Email |
|---------|---------|----------|-----------------|
| CloudTech Solutions | cloudtech.io | Cloud Computing | "Hi team, I've been impressed..." |
| DataViz Pro | dataviz-pro.com | Data Analytics | "Your data visualization platform..." |

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional data source integrations
- UI/UX enhancements
- Performance optimizations
- Bug fixes and testing
- Documentation improvements

## 📄 License

This project is open source and available for educational and commercial use.

## 💡 Tips & Tricks

### For Best Results
1. Use clear, consistent company names
2. Ensure websites are valid and reachable
3. Use high-quality API keys for better enrichment
4. Test with 5-10 companies first
5. Review generated emails before sending

### Troubleshooting

**Q: "API Key not found" error**
- A: Ensure `.env` file exists and has correct keys
- A: Check file permissions

**Q: Slow processing**
- A: Reduce batch size
- A: Check internet connection
- A: Consider using higher-tier API plans

**Q: Missing company data**
- A: This is normal without Clearbit API
- A: Mock data provides realistic fallback
- A: Add Clearbit API key for better enrichment

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review error messages carefully
3. Verify API keys and `.env` configuration
4. Ensure all dependencies are installed

## 🎉 Conclusion

This project serves as an excellent foundation for building professional GTM automation tools. It demonstrates best practices in Python development, API integration, and AI utilization.

Happy lead generating! 🚀

---

**Built with ❤️ for sales teams and entrepreneurs**

*Last Updated: 2024*

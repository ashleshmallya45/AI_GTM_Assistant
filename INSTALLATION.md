# Installation Guide - AI GTM Assistant

Complete step-by-step guide to install and configure the AI GTM Assistant.

## 📋 Prerequisites

Before you start, make sure you have:
- ✅ Python 3.8 or higher
- ✅ pip (Python package manager)
- ✅ At least 200MB free disk space
- ✅ One of these API keys:
  - OpenAI API key (https://platform.openai.com/api-keys)
  - Google Gemini API key (https://ai.google.dev/)

## 🖥 System Requirements

### Windows
- Windows 10 or later
- PowerShell or Command Prompt

### macOS
- macOS 10.14 or later
- Terminal

### Linux
- Ubuntu 18.04 or later (or similar distribution)
- Bash or Zsh

## 📥 Installation Steps

### Step 1: Get Python

**Windows:**
1. Download from https://www.python.org/downloads/
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click "Install Now"

**macOS:**
```bash
# Using Homebrew
brew install python3

# Or download from https://www.python.org/downloads/
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip
```

Verify installation:
```bash
python --version  # Should show Python 3.8+
pip --version
```

### Step 2: Download/Clone Project

**Option A: Download as ZIP**
1. Download the project ZIP file
2. Extract to desired location
3. Open terminal/command prompt in that folder

**Option B: Clone from Git (if available)**
```bash
git clone <repository-url>
cd AI_GTM_Assistant
```

### Step 3: Create Virtual Environment (Recommended)

Creating a virtual environment isolates dependencies and prevents conflicts.

**Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# You should see (venv) in your terminal
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# You should see (venv) in your terminal
```

### Step 4: Upgrade pip

```bash
# Ensure pip is up to date
pip install --upgrade pip
```

### Step 5: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

**What gets installed:**
- streamlit: Web application framework
- pandas: Data processing
- numpy: Numerical computing
- requests: HTTP library
- openai: OpenAI API client
- google-generativeai: Google Gemini API client
- python-dotenv: Environment variable management

### Step 6: Configure API Keys

1. **Copy the example file:**
```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

2. **Get your API keys:**

**For OpenAI:**
- Go to https://platform.openai.com/api-keys
- Sign up/Login
- Create new API key
- Copy the key

**For Google Gemini:**
- Go to https://ai.google.dev/
- Click "Get API Key"
- Create new API key
- Copy the key

**For Clearbit (Optional):**
- Go to https://clearbit.com/api
- Create account
- Get API key

3. **Edit the .env file:**

**Windows (Notepad):**
```bash
notepad .env
```

**macOS/Linux (nano):**
```bash
nano .env
```

**Windows (VS Code):**
```bash
code .env
```

4. **Add your API keys:**

```env
OPENAI_API_KEY=sk-your-actual-key-here
GEMINI_API_KEY=your-actual-gemini-key-here
CLEARBIT_API_KEY=your-actual-clearbit-key-here
```

⚠️ **Important:** Never share your `.env` file or API keys!

### Step 7: Verify Installation

Run the setup check script:

```bash
python setup_check.py
```

This will verify:
- ✅ Python version
- ✅ All dependencies installed
- ✅ .env file configured
- ✅ Sample data available

### Step 8: Run the Application

```bash
streamlit run app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://xxx.xxx.x.xxx:8501
```

The app should automatically open in your default browser. If not, visit:
**http://localhost:8501**

## 🧪 Test the Installation

1. Upload `sample_leads.csv` in the web interface
2. Click "Process Companies"
3. Wait for processing to complete
4. Check the results in the table
5. Download the CSV

If this works, your installation is successful! 🎉

## 🐛 Troubleshooting

### Issue: "Python is not recognized"
**Solution:**
- Make sure Python is in your PATH
- Reinstall Python and check "Add Python to PATH"
- Or use full path: `C:\Python310\python` (Windows)

### Issue: "No module named 'streamlit'"
**Solution:**
```bash
# Make sure virtual environment is activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Then install requirements again
pip install -r requirements.txt
```

### Issue: "API key not found" error
**Solution:**
1. Check .env file exists in same directory as app.py
2. Verify API keys are added correctly
3. No spaces around = sign: `KEY=value` (not `KEY = value`)
4. Save .env file properly

### Issue: "Port 8501 is already in use"
**Solution:**
```bash
# Use a different port
streamlit run app.py --server.port 8502
```

### Issue: Slow processing
**Solution:**
- Reduce batch size
- Check internet connection
- Use smaller CSV file first
- Ensure API keys are valid

### Issue: Mock data showing as company data
**Solution:**
- This is expected if Clearbit API key isn't configured
- Add CLEARBIT_API_KEY to .env for real data
- Or use mock data for testing (it's fine!)

## 📦 Updating Packages

To update all packages to latest versions:

```bash
pip install --upgrade -r requirements.txt
```

## 🗑 Uninstall

To completely remove the installation:

**Windows:**
```bash
# Deactivate virtual environment
deactivate

# Delete the venv folder
rmdir /s /q venv
```

**macOS/Linux:**
```bash
# Deactivate virtual environment
deactivate

# Delete the venv folder
rm -rf venv
```

## 📝 Environment Variables Reference

| Variable | Required | Purpose |
|----------|----------|---------|
| `OPENAI_API_KEY` | One of these two | OpenAI GPT-3.5 API key |
| `GEMINI_API_KEY` | One of these two | Google Gemini API key |
| `CLEARBIT_API_KEY` | Optional | Company data enrichment |

## ✅ Verification Checklist

After installation, verify:
- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All packages installed (`pip list` shows all requirements)
- [ ] .env file created with API keys
- [ ] `streamlit run app.py` works without errors
- [ ] Web app opens at http://localhost:8501
- [ ] Sample data processes successfully

## 🆘 Need Help?

1. Check Python version: `python --version`
2. Check installed packages: `pip list`
3. Run setup check: `python setup_check.py`
4. Check .env file exists and has correct format
5. Verify API keys are valid and active

## 🎉 You're Ready!

Once all steps are complete, you're ready to start using the AI GTM Assistant!

```bash
streamlit run app.py
```

Happy lead generating! 🚀

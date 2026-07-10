"""
Quick Start Guide - AI GTM Assistant

This script helps you quickly set up and test the AI GTM Assistant.
Run this before starting the Streamlit app.
"""

import os
import sys
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    print("🔍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version OK: {sys.version.split()[0]}")
    return True


def check_dependencies():
    """Check if all required packages are installed."""
    print("\n🔍 Checking dependencies...")
    
    required_packages = {
        'streamlit': 'Streamlit (Web UI)',
        'pandas': 'Pandas (Data Processing)',
        'requests': 'Requests (HTTP)',
        'dotenv': 'python-dotenv (Environment Variables)'
    }
    
    missing = []
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {name} installed")
        except ImportError:
            print(f"❌ {name} NOT installed")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print(f"\n📦 Install them using:")
        print(f"   pip install -r requirements.txt")
        return False
    
    return True


def check_environment_file():
    """Check if .env file exists."""
    print("\n🔍 Checking environment configuration...")
    
    env_path = Path('.env')
    env_example = Path('.env.example')
    
    if env_path.exists():
        print("✅ .env file found")
        
        # Check if it has API keys
        with open(env_path, 'r') as f:
            content = f.read()
            if 'OPENAI_API_KEY' in content or 'GEMINI_API_KEY' in content:
                print("✅ API keys configured")
                return True
            else:
                print("⚠️  .env file exists but no API keys configured")
                return False
    else:
        print("❌ .env file not found")
        
        if env_example.exists():
            print(f"\n📝 To set up, run:")
            print(f"   cp .env.example .env")
            print(f"   # Edit .env and add your API keys")
        return False


def check_sample_data():
    """Check if sample data exists."""
    print("\n🔍 Checking sample data...")
    
    sample_path = Path('sample_leads.csv')
    
    if sample_path.exists():
        print("✅ Sample data (sample_leads.csv) found")
        return True
    else:
        print("❌ Sample data not found")
        return False


def print_next_steps():
    """Print next steps for the user."""
    print("\n" + "="*50)
    print("📋 NEXT STEPS")
    print("="*50)
    
    print("\n1️⃣  Install dependencies (if not done):")
    print("   pip install -r requirements.txt")
    
    print("\n2️⃣  Configure API keys:")
    print("   cp .env.example .env")
    print("   # Edit .env and add your API keys")
    
    print("\n3️⃣  Run the application:")
    print("   streamlit run app.py")
    
    print("\n4️⃣  Open in browser:")
    print("   http://localhost:8501")
    
    print("\n5️⃣  Test with sample data:")
    print("   Upload sample_leads.csv")
    
    print("\n" + "="*50)


def run_checks():
    """Run all setup checks."""
    print("\n" + "="*50)
    print("🚀 AI GTM ASSISTANT - SETUP CHECK")
    print("="*50 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment File", check_environment_file),
        ("Sample Data", check_sample_data),
    ]
    
    results = []
    for check_name, check_func in checks:
        result = check_func()
        results.append((check_name, result))
    
    # Summary
    print("\n" + "="*50)
    print("📊 SETUP SUMMARY")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {check_name}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 Setup complete! You're ready to go!")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
    
    print_next_steps()


if __name__ == "__main__":
    run_checks()

#!/usr/bin/env python3
"""
JobSniper AI - Final Launcher
=============================

This script ensures everything works perfectly before launching the application.
"""

import sys
import subprocess
import os
from pathlib import Path

def print_header():
    """Print application header"""
    print("🎯 JobSniper AI - Final Working Version")
    print("=" * 50)
    print("Professional Resume Analysis & Career Intelligence")
    print("=" * 50)

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ required. Current: {sys.version}")
        print("Please upgrade Python and try again.")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def check_dependencies():
    """Check required dependencies"""
    print("\n📦 Checking dependencies...")
    
    required = ['streamlit', 'plotly', 'pandas', 'PyPDF2']
    missing = []
    
    for package in required:
        try:
            __import__(package.lower().replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n🔧 Install missing packages:")
        print(f"   pip install {' '.join(missing)}")
        print("\n📦 Or install minimal requirements:")
        print("   pip install -r requirements_minimal.txt")
        return False
    
    return True

def check_files():
    """Check required files exist"""
    print("\n📁 Checking files...")
    
    required_files = ['app_final.py']
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            return False
    
    return True

def test_basic_functionality():
    """Test basic functionality"""
    print("\n🧪 Testing basic functionality...")
    
    try:
        # Test imports
        import streamlit as st
        import plotly.express as px
        import pandas as pd
        print("✅ Core imports working")
        
        # Test data creation
        test_data = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 4, 9]})
        fig = px.line(test_data, x='x', y='y')
        print("✅ Chart generation working")
        
        # Test file operations
        test_text = "This is a test resume with Python and JavaScript skills."
        if 'python' in test_text.lower():
            print("✅ Text processing working")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def run_application():
    """Run the Streamlit application"""
    print("\n🚀 Starting JobSniper AI...")
    print("📱 Opening in your default browser...")
    print("🔗 URL: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        # Run streamlit with optimized settings
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'app_final.py',
            '--server.headless', 'false',
            '--server.runOnSave', 'true',
            '--browser.gatherUsageStats', 'false',
            '--theme.base', 'light'
        ])
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Application stopped by user.")
        print("Thank you for using JobSniper AI!")
    except FileNotFoundError:
        print("❌ Streamlit not found. Install with: pip install streamlit")
    except Exception as e:
        print(f"❌ Error: {e}")

def show_quick_help():
    """Show quick help information"""
    print("\n💡 Quick Help:")
    print("   📄 Upload resume (PDF, DOCX, TXT)")
    print("   📝 Or use sample resume")
    print("   🔍 Click 'Analyze Resume'")
    print("   📊 View results and insights")
    print("\n🆘 If you encounter issues:")
    print("   1. Check all dependencies are installed")
    print("   2. Try the sample resume first")
    print("   3. Ensure file is under 10MB")
    print("   4. Use supported formats only")

def main():
    """Main function"""
    print_header()
    
    # Run all checks
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Files", check_files),
        ("Functionality", test_basic_functionality)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        if not check_func():
            all_passed = False
            break
    
    if all_passed:
        print("\n🎉 All checks passed! Ready to launch.")
        show_quick_help()
        
        # Ask user if they want to continue
        try:
            response = input("\n▶️  Press Enter to start JobSniper AI (or 'q' to quit): ")
            if response.lower() != 'q':
                run_application()
            else:
                print("👋 Goodbye!")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
    
    else:
        print("\n❌ Some checks failed. Please fix the issues above.")
        print("\n🔧 Quick fix commands:")
        print("   pip install streamlit plotly pandas PyPDF2")
        print("   # or")
        print("   pip install -r requirements_minimal.txt")

if __name__ == "__main__":
    main()
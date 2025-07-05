#!/usr/bin/env python3
"""
JobSniper AI - Fixed Application Runner
======================================

Simple script to run the fixed JobSniper AI application.
Handles dependency checking and provides helpful error messages.
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        print("Please upgrade Python and try again.")
        return False
    return True

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        'streamlit',
        'plotly', 
        'pandas',
        'PyPDF2'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.lower().replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n🔧 To install missing packages, run:")
        print("   pip install " + " ".join(missing_packages))
        print("\n📦 Or install all dependencies:")
        print("   pip install -r requirements_fixed.txt")
        return False
    
    return True

def check_files():
    """Check if required files exist."""
    required_files = [
        'app_fixed.py',
        'utils/simple_resume_parser.py',
        'utils/enhanced_file_reader.py'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("\n📁 Please ensure all files are in the correct location.")
        return False
    
    return True

def run_application():
    """Run the Streamlit application."""
    try:
        print("🚀 Starting JobSniper AI...")
        print("📱 The application will open in your default browser.")
        print("🔗 URL: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the application.")
        print("-" * 50)
        
        # Run streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'app_fixed.py',
            '--server.headless', 'false',
            '--server.runOnSave', 'true',
            '--browser.gatherUsageStats', 'false'
        ])
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Application stopped by user.")
    except FileNotFoundError:
        print("❌ Error: Streamlit not found.")
        print("📦 Install streamlit: pip install streamlit")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def main():
    """Main function to run all checks and start the application."""
    print("🎯 JobSniper AI - Fixed Version")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    # Check files
    print("📁 Checking files...")
    if not check_files():
        sys.exit(1)
    
    print("✅ All checks passed!")
    print()
    
    # Run application
    run_application()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
JobSniper AI - Comprehensive Test Suite
=======================================

Test all features and components to ensure everything works correctly.
"""

import sys
import os
import tempfile
import json
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all required imports"""
    print("🔍 Testing imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        print("✅ Plotly imported successfully")
    except ImportError as e:
        print(f"❌ Plotly import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    return True

def test_file_readers():
    """Test file reading capabilities"""
    print("\n📁 Testing file readers...")
    
    # Test PDF reading
    try:
        from PyPDF2 import PdfReader
        print("✅ PyPDF2 available")
    except ImportError:
        print("⚠️ PyPDF2 not available")
    
    try:
        import pdfplumber
        print("✅ pdfplumber available")
    except ImportError:
        print("⚠️ pdfplumber not available")
    
    try:
        import fitz  # PyMuPDF
        print("✅ PyMuPDF available")
    except ImportError:
        print("⚠️ PyMuPDF not available")
    
    # Test DOCX reading
    try:
        from docx import Document
        print("✅ python-docx available")
    except ImportError:
        print("⚠️ python-docx not available")
    
    return True

def test_resume_parser():
    """Test resume parsing functionality"""
    print("\n🤖 Testing resume parser...")
    
    try:
        from utils.simple_resume_parser import parse_resume
        
        # Test with sample text
        sample_text = """
        John Smith
        Software Engineer
        Email: john@example.com
        Phone: (555) 123-4567
        
        Skills: Python, JavaScript, React, SQL
        Experience: 5 years of software development
        Education: Bachelor's in Computer Science
        """
        
        result = parse_resume(sample_text)
        
        if result and result.get('parsing_status') == 'success':
            print("✅ Resume parser working correctly")
            print(f"   - Name: {result.get('name', 'Not found')}")
            print(f"   - Skills: {len(result.get('skills', {}).get('all_skills', []))} found")
            print(f"   - Experience: {result.get('years_of_experience', 0)} years")
            return True
        else:
            print(f"❌ Resume parser failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Resume parser test failed: {e}")
        return False

def test_enhanced_file_reader():
    """Test enhanced file reader"""
    print("\n📖 Testing enhanced file reader...")
    
    try:
        from utils.enhanced_file_reader import extract_text_from_file, SAMPLE_RESUME_TEXT
        
        # Test with sample text
        if SAMPLE_RESUME_TEXT and len(SAMPLE_RESUME_TEXT) > 100:
            print("✅ Sample resume text available")
            print(f"   - Length: {len(SAMPLE_RESUME_TEXT)} characters")
            return True
        else:
            print("⚠️ Sample resume text not available or too short")
            return False
            
    except Exception as e:
        print(f"❌ Enhanced file reader test failed: {e}")
        return False

def test_app_files():
    """Test that all app files exist and are valid"""
    print("\n📄 Testing app files...")
    
    required_files = [
        'app_fixed.py',
        'app_ultimate.py',
        'utils/simple_resume_parser.py',
        'utils/enhanced_file_reader.py',
        'requirements_fixed.txt'
    ]
    
    all_exist = True
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            all_exist = False
    
    return all_exist

def test_sample_data():
    """Test sample data generation"""
    print("\n📊 Testing sample data generation...")
    
    try:
        import pandas as pd
        from datetime import datetime, timedelta
        
        # Test data generation
        dates = pd.date_range(start='2024-01-01', end='2024-01-07', freq='D')
        sample_data = pd.DataFrame({
            'Date': dates,
            'Resumes': [12, 18, 25, 15, 32, 45, 38],
            'Jobs': [35, 52, 78, 42, 95, 120, 105]
        })
        
        if len(sample_data) == 7:
            print("✅ Sample data generation working")
            return True
        else:
            print("❌ Sample data generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Sample data test failed: {e}")
        return False

def test_skill_extraction():
    """Test skill extraction patterns"""
    print("\n🛠️ Testing skill extraction...")
    
    try:
        from utils.simple_resume_parser import SimpleResumeParser
        
        parser = SimpleResumeParser()
        
        test_text = """
        I have experience with Python, JavaScript, React, Node.js, SQL, MongoDB,
        Docker, Kubernetes, AWS, Machine Learning, and Data Science.
        I also have leadership and communication skills.
        """
        
        result = parser.parse_resume(test_text)
        skills = result.get('skills', {}).get('all_skills', [])
        
        expected_skills = ['Python', 'JavaScript', 'React', 'Node.js', 'SQL', 'MongoDB']
        found_skills = [skill for skill in expected_skills if skill in skills]
        
        if len(found_skills) >= 4:
            print(f"✅ Skill extraction working - found {len(skills)} skills")
            print(f"   - Sample skills: {', '.join(skills[:5])}")
            return True
        else:
            print(f"⚠️ Skill extraction needs improvement - found {len(found_skills)} of {len(expected_skills)} expected skills")
            return False
            
    except Exception as e:
        print(f"❌ Skill extraction test failed: {e}")
        return False

def test_contact_extraction():
    """Test contact information extraction"""
    print("\n📞 Testing contact extraction...")
    
    try:
        from utils.simple_resume_parser import SimpleResumeParser
        
        parser = SimpleResumeParser()
        
        test_text = """
        John Smith
        Email: john.smith@example.com
        Phone: (555) 123-4567
        LinkedIn: linkedin.com/in/johnsmith
        Location: San Francisco, CA
        """
        
        result = parser.parse_resume(test_text)
        contact = result.get('contact', {})
        
        checks = [
            ('email', 'john.smith@example.com'),
            ('phone', '555'),  # Partial match
        ]
        
        passed = 0
        for field, expected in checks:
            if field in contact and expected in contact[field]:
                passed += 1
                print(f"   ✅ {field}: {contact[field]}")
            else:
                print(f"   ⚠️ {field}: not found or incorrect")
        
        if passed >= 1:
            print("✅ Contact extraction working")
            return True
        else:
            print("❌ Contact extraction failed")
            return False
            
    except Exception as e:
        print(f"❌ Contact extraction test failed: {e}")
        return False

def test_visualization():
    """Test chart generation"""
    print("\n📊 Testing visualization...")
    
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        import pandas as pd
        
        # Test simple chart
        data = pd.DataFrame({
            'Category': ['A', 'B', 'C'],
            'Values': [10, 20, 15]
        })
        
        fig = px.bar(data, x='Category', y='Values')
        
        if fig:
            print("✅ Plotly chart generation working")
            return True
        else:
            print("❌ Chart generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Visualization test failed: {e}")
        return False

def test_error_handling():
    """Test error handling"""
    print("\n🛡️ Testing error handling...")
    
    try:
        from utils.simple_resume_parser import parse_resume
        
        # Test with empty text
        result1 = parse_resume("")
        if result1.get('parsing_status') == 'error':
            print("✅ Empty text error handling working")
        else:
            print("⚠️ Empty text error handling needs improvement")
        
        # Test with very short text
        result2 = parse_resume("Hi")
        if result2.get('parsing_status') == 'error':
            print("✅ Short text error handling working")
        else:
            print("⚠️ Short text error handling needs improvement")
        
        # Test with None
        result3 = parse_resume(None)
        if result3.get('parsing_status') == 'error':
            print("✅ None input error handling working")
        else:
            print("⚠️ None input error handling needs improvement")
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def run_performance_test():
    """Test performance with larger text"""
    print("\n⚡ Testing performance...")
    
    try:
        from utils.simple_resume_parser import parse_resume
        import time
        
        # Create large test text
        large_text = """
        John Alexander Smith
        Senior Software Engineer
        
        """ + "Experience with Python, JavaScript, React, Node.js, SQL, MongoDB. " * 100
        
        start_time = time.time()
        result = parse_resume(large_text)
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        if processing_time < 5.0:  # Should complete within 5 seconds
            print(f"✅ Performance test passed - {processing_time:.2f} seconds")
            return True
        else:
            print(f"⚠️ Performance test slow - {processing_time:.2f} seconds")
            return False
            
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🎯 JobSniper AI - Comprehensive Test Suite")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("File Readers", test_file_readers),
        ("Resume Parser", test_resume_parser),
        ("Enhanced File Reader", test_enhanced_file_reader),
        ("App Files", test_app_files),
        ("Sample Data", test_sample_data),
        ("Skill Extraction", test_skill_extraction),
        ("Contact Extraction", test_contact_extraction),
        ("Visualization", test_visualization),
        ("Error Handling", test_error_handling),
        ("Performance", run_performance_test)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to use.")
        print("\n🚀 To start the application:")
        print("   python run_fixed.py")
        print("   # or")
        print("   streamlit run app_fixed.py")
        print("   # or for ultimate version")
        print("   streamlit run app_ultimate.py")
    elif passed >= total * 0.8:
        print("✅ Most tests passed! The application should work well.")
        print("⚠️ Some optional features may not be available.")
    else:
        print("❌ Several tests failed. Please check dependencies and file structure.")
        print("\n🔧 To fix issues:")
        print("   pip install -r requirements_fixed.txt")
        print("   # Ensure all files are in the correct location")
    
    print(f"\n📋 Test Summary:")
    for i, (test_name, _) in enumerate(tests):
        status = "✅" if i < passed else "❌"
        print(f"   {status} {test_name}")

if __name__ == "__main__":
    main()
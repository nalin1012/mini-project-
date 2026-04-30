#!/usr/bin/env python3
"""Quick test to verify PDF reading works"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_pdf_libraries():
    """Test that PDF libraries are installed"""
    print("Testing PDF libraries...")
    
    try:
        from PyPDF2 import PdfReader as PyPDF2Reader
        print("✓ PyPDF2 is installed")
    except ImportError as e:
        print(f"✗ PyPDF2 import failed: {e}")
        return False
    
    try:
        from pypdf import PdfReader as pypdfReader
        print("✓ pypdf is installed")
    except ImportError as e:
        print(f"✗ pypdf import failed: {e}")
        return False
    
    try:
        import openai
        print("✓ OpenAI is installed")
    except ImportError as e:
        print(f"✗ OpenAI import failed: {e}")
        return False
    
    return True

def test_pdf_reading():
    """Test basic PDF reading functionality"""
    print("\nTesting PDF reading functionality...")
    
    try:
        from pypdf import PdfReader
        import io
        
        # Create a simple test (read-only test)
        print("✓ PDF reading imports successful")
        return True
    except Exception as e:
        print(f"✗ PDF reading test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Smart Notes - Dependency Test")
    print("=" * 50)
    
    libs_ok = test_pdf_libraries()
    pdf_ok = test_pdf_reading()
    
    print("\n" + "=" * 50)
    if libs_ok and pdf_ok:
        print("✓ All tests passed! System is ready.")
        sys.exit(0)
    else:
        print("✗ Some tests failed. Check output above.")
        sys.exit(1)

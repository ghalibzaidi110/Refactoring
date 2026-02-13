#!/usr/bin/env python3
"""
Test script for RefactorGPT
"""
import sys
import json

def test_formatter():
    """Test the formatter module"""
    print("Testing formatter...")
    try:
        from app.services.formatter import format_code
        code = "def hello(  ):\n  print('hi')"
        result, improvements = format_code(code)
        print(f"✅ Formatter works: {len(improvements)} improvements")
        return True
    except Exception as e:
        print(f"❌ Formatter failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_refactor():
    """Test the refactor module without LLM"""
    print("\nTesting refactor (no LLM)...")
    try:
        from app.services.refactor import refactor_code
        code = "def hello():\n  print('hi')"
        result = refactor_code(code, use_llm=False)
        print(f"✅ Refactor works: {result['summary']}")
        print(f"   Improvements: {len(result['improvements'])}")
        return True
    except Exception as e:
        print(f"❌ Refactor failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_request():
    """Test making an API request"""
    print("\nTesting API request...")
    try:
        import requests
        url = "http://localhost:8000/refactor"
        data = {
            "code": "def hello():\n  print('hi')",
            "use_llm": False
        }
        response = requests.post(url, json=data)
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API works: {result['summary']}")
            return True
        else:
            print(f"❌ API failed: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("⚠️  Server not running. Start with: ./start.sh")
        return None
    except Exception as e:
        print(f"❌ API test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_schemas():
    """Test Pydantic schemas"""
    print("\nTesting schemas...")
    try:
        from app.schemas import RefactorRequest, RefactorResponse
        
        # Test request
        req = RefactorRequest(code="print('test')")
        print(f"✅ RefactorRequest created: use_llm={req.use_llm}")
        
        # Test response
        resp = RefactorResponse(
            summary="Test",
            refactored_code="print('test')",
            improvements=["test"]
        )
        print(f"✅ RefactorResponse created")
        return True
    except Exception as e:
        print(f"❌ Schemas failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("RefactorGPT Test Suite")
    print("=" * 50)
    
    results = []
    results.append(("Schemas", test_schemas()))
    results.append(("Formatter", test_formatter()))
    results.append(("Refactor", test_refactor()))
    results.append(("API", test_api_request()))
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print("=" * 50)
    for name, result in results:
        if result is True:
            print(f"✅ {name}: PASSED")
        elif result is False:
            print(f"❌ {name}: FAILED")
        else:
            print(f"⚠️  {name}: SKIPPED")
    
    print("\nIf tests fail, check the error messages above.")

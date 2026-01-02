"""Test script for the Resume Analyzer API"""
import requests
import time
import sys

API_BASE = "http://127.0.0.1:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing Health Check Endpoint...")
    try:
        response = requests.get(f"{API_BASE}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check Passed: {data['status']} - {data['message']}")
            return True
        else:
            print(f"❌ Health Check Failed: Status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on port 5000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_homepage():
    """Test the homepage"""
    print("\n🔍 Testing Homepage...")
    try:
        response = requests.get(API_BASE, timeout=5)
        if response.status_code == 200 and len(response.text) > 100:
            print(f"✅ Homepage Loaded: {len(response.text)} characters")
            return True
        else:
            print(f"❌ Homepage Failed: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("="*60)
    print("🚀 AI Resume Analyzer - Testing Suite")
    print("="*60)
    
    # Wait for server to be ready
    print("\n⏳ Waiting for server to start...")
    time.sleep(2)
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health_check()))
    results.append(("Homepage", test_homepage()))
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✨ All tests passed! The application is working correctly.")
        print("\n📝 Next Steps:")
        print("   1. Open http://localhost:5000 in your browser")
        print("   2. Upload a resume (PDF or DOCX)")
        print("   3. Optionally add a job description")
        print("   4. Click 'Analyze Resume' to see AI-powered insights")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())

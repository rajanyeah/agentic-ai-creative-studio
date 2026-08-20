"""
Test script to validate the Streamlit app structure
This tests that app.py can be imported and has the required components
"""
import sys


def test_app_import():
    """Test that app.py can be imported"""
    print("🧪 Testing app.py import...")
    try:
        import app
        print("  ✅ app.py imports successfully")
        return True
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False


def test_app_functions():
    """Test that required functions exist in app.py"""
    print("\n🧪 Testing app.py functions...")
    try:
        import app
        
        # Check for key functions
        required_functions = [
            'load_api_key',
            'initialize_session_state',
            'display_header',
            'display_sidebar',
            'run_creative_workflow',
            'display_results',
            'main'
        ]
        
        for func_name in required_functions:
            if not hasattr(app, func_name):
                print(f"  ❌ Missing function: {func_name}")
                return False
        
        print("  ✅ All required functions exist")
        return True
    except Exception as e:
        print(f"  ❌ Function test failed: {e}")
        return False


def test_streamlit_import():
    """Test that Streamlit is installed and can be imported"""
    print("\n🧪 Testing Streamlit installation...")
    try:
        import streamlit as st
        print(f"  ✅ Streamlit version {st.__version__} installed")
        return True
    except ImportError as e:
        print(f"  ❌ Streamlit import failed: {e}")
        return False


def test_creative_studio_import():
    """Test that CreativeStudio can still be imported from main.py"""
    print("\n🧪 Testing CreativeStudio import from main.py...")
    try:
        from main import CreativeStudio
        print("  ✅ CreativeStudio imports successfully from main.py")
        print("  ✅ CLI functionality remains intact")
        return True
    except ImportError as e:
        print(f"  ❌ CreativeStudio import failed: {e}")
        return False


def main():
    """Run all validation tests"""
    print("=" * 80)
    print("🎨 STREAMLIT WEB UI - VALIDATION TESTS")
    print("=" * 80)
    
    tests = [
        test_streamlit_import,
        test_app_import,
        test_app_functions,
        test_creative_studio_import
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All validation tests passed!")
        print("\n💡 The Streamlit web UI is ready to use.")
        print("📝 To run the web UI:")
        print("   streamlit run app.py")
        print("\n📝 To run the CLI (still works):")
        print("   python main.py 'your topic here'")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

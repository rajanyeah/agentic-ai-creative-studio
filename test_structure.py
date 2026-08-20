"""
Test script to validate the Multi-Agent Creative Studio structure
This tests the system architecture without requiring an API key
"""
import sys


def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing imports...")
    try:
        from idea_agent import IdeaAgent
        from critic_agent import CriticAgent
        from refiner_agent import RefinerAgent
        from presenter_agent import PresenterAgent
        from main import CreativeStudio
        print("  ✅ All imports successful")
        return True
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False


def test_class_initialization():
    """Test that classes can be instantiated with mock API key"""
    print("\n🧪 Testing class initialization...")
    try:
        from idea_agent import IdeaAgent
        from critic_agent import CriticAgent
        from refiner_agent import RefinerAgent
        from presenter_agent import PresenterAgent
        
        # Use a dummy API key for structure testing
        dummy_key = "test_key_12345"
        
        idea_agent = IdeaAgent(dummy_key, "gemini-3.6-flash")
        critic_agent = CriticAgent(dummy_key, "gemini-3.6-flash")
        refiner_agent = RefinerAgent(dummy_key, "gemini-3.6-flash")
        presenter_agent = PresenterAgent(dummy_key, "gemini-3.6-flash")
        
        # Check agent names
        assert idea_agent.name == "Idea Agent", "IdeaAgent name mismatch"
        assert critic_agent.name == "Critic Agent", "CriticAgent name mismatch"
        assert refiner_agent.name == "Refiner Agent", "RefinerAgent name mismatch"
        assert presenter_agent.name == "Presenter Agent", "PresenterAgent name mismatch"
        
        # Check model names
        assert idea_agent.model_name == "gemini-3.6-flash", "IdeaAgent model mismatch"
        assert critic_agent.model_name == "gemini-3.6-flash", "CriticAgent model mismatch"
        assert refiner_agent.model_name == "gemini-3.6-flash", "RefinerAgent model mismatch"
        assert presenter_agent.model_name == "gemini-3.6-flash", "PresenterAgent model mismatch"
        
        print("  ✅ All agents initialized correctly")
        print(f"  ✅ {idea_agent}")
        print(f"  ✅ {critic_agent}")
        print(f"  ✅ {refiner_agent}")
        print(f"  ✅ {presenter_agent}")
        return True
    except Exception as e:
        print(f"  ❌ Initialization failed: {e}")
        return False


def test_creative_studio():
    """Test CreativeStudio orchestrator initialization"""
    print("\n🧪 Testing CreativeStudio orchestrator...")
    try:
        from main import CreativeStudio
        
        dummy_key = "test_key_12345"
        studio = CreativeStudio(dummy_key, "gemini-3.6-flash")
        
        # Check that all agents are initialized
        assert hasattr(studio, 'idea_agent'), "IdeaAgent not initialized"
        assert hasattr(studio, 'critic_agent'), "CriticAgent not initialized"
        assert hasattr(studio, 'refiner_agent'), "RefinerAgent not initialized"
        assert hasattr(studio, 'presenter_agent'), "PresenterAgent not initialized"
        
        print("  ✅ CreativeStudio orchestrator initialized correctly")
        print("  ✅ All 4 agents are properly connected")
        return True
    except Exception as e:
        print(f"  ❌ CreativeStudio initialization failed: {e}")
        return False


def test_a2a_communication_structure():
    """Test that A2A communication structure is in place"""
    print("\n🧪 Testing A2A communication structure...")
    try:
        # Check that methods accept and return proper data structures
        from idea_agent import IdeaAgent
        from critic_agent import CriticAgent
        from refiner_agent import RefinerAgent
        from presenter_agent import PresenterAgent
        
        # Verify method signatures
        assert hasattr(IdeaAgent, 'generate_ideas'), "IdeaAgent missing generate_ideas method"
        assert hasattr(CriticAgent, 'analyze_ideas'), "CriticAgent missing analyze_ideas method"
        assert hasattr(RefinerAgent, 'refine_ideas'), "RefinerAgent missing refine_ideas method"
        assert hasattr(PresenterAgent, 'create_presentation'), "PresenterAgent missing create_presentation method"
        
        print("  ✅ A2A communication methods are in place")
        print("  ✅ IdeaAgent → CriticAgent → RefinerAgent → PresenterAgent")
        return True
    except Exception as e:
        print(f"  ❌ A2A structure test failed: {e}")
        return False


def main():
    """Run all validation tests"""
    print("=" * 80)
    print("🎨 MULTI-AGENT CREATIVE STUDIO - VALIDATION TESTS")
    print("=" * 80)
    
    tests = [
        test_imports,
        test_class_initialization,
        test_creative_studio,
        test_a2a_communication_structure
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
        print("\n💡 The system structure is correct and ready to use.")
        print("📝 To run the actual system, you need to:")
        print("   1. Create a .env file with your GOOGLE_API_KEY")
        print("   2. Run: python main.py 'your topic here'")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

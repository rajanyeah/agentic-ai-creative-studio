"""
Example script demonstrating how to use the Multi-Agent Creative Studio programmatically
"""
import os
from dotenv import load_dotenv
from main import CreativeStudio


def run_example():
    """Run a simple example of the creative studio"""
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ Please set GOOGLE_API_KEY in your .env file")
        return
    
    # Define a creative topic
    topic = "A subscription box service for pet owners"
    
    # Initialize the Creative Studio
    studio = CreativeStudio(api_key)
    
    # Run the complete workflow
    results = studio.run(topic, save_output=True)
    
    # Display summary
    studio.display_summary(results)
    
    # Access specific results
    print("\n📋 Accessing Specific Results:")
    print(f"- Topic: {results['topic']}")
    print(f"- Number of workflow steps: {len(results['workflow'])}")
    print(f"- Final presentation generated at: {results['final_output']['generated_at']}")


if __name__ == "__main__":
    run_example()

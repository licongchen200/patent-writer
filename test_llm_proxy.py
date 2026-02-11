#!/usr/bin/env python3
"""
Test script to verify internal LLM proxy connection
"""
import os
import sys

def test_llm_connection():
    """Test connection to internal LLM proxy"""
    
    print("Testing Internal LLM Proxy Connection...")
    print("=" * 60)
    
    # Check environment variables
    api_base = os.getenv("OPENAI_API_BASE", "http://llm-proxy.ceui.cnap.comcast.net")
    api_key = os.getenv("OPENAI_API_KEY", "dummy-key-not-needed")
    
    print(f"\nAPI Base URL: {api_base}")
    print(f"API Key: {api_key[:20]}..." if len(api_key) > 20 else f"API Key: {api_key}")
    
    try:
        from openai import OpenAI
        
        # Initialize client
        client = OpenAI(
            base_url=api_base,
            api_key=api_key
        )
        
        print("\n✓ OpenAI client initialized")
        print("\nSending test request...")
        
        # Test with a simple prompt
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": "Hello! Please respond with 'LLM proxy is working!' if you receive this."}
            ],
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        
        print("\n" + "=" * 60)
        print("✅ SUCCESS! LLM Proxy is working!")
        print("=" * 60)
        print(f"\nResponse: {result}")
        print("\nYou're ready to run the patent writer!")
        print("\nNext step: python main.py")
        
        return True
        
    except ImportError:
        print("\n❌ ERROR: OpenAI library not installed")
        print("Run: pip install openai")
        return False
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ CONNECTION FAILED")
        print("=" * 60)
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check if llm-proxy is running:")
        print("   kubectl get pods -n mybot | grep llm-proxy")
        print("2. Verify the service is accessible:")
        print("   kubectl get svc llm-proxy -n mybot")
        print("3. Test direct access:")
        print("   curl http://llm-proxy.ceui.cnap.comcast.net/health")
        print("\nIf using Docker, make sure the container can reach the k8s service")
        
        return False

if __name__ == "__main__":
    success = test_llm_connection()
    sys.exit(0 if success else 1)

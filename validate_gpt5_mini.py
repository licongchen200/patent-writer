#!/usr/bin/env python3
"""
Validate GPT-5-mini configuration before applying to main.py
"""
import sys
import os

print("=" * 70)
print("VALIDATING GPT-5-MINI CONFIGURATION")
print("=" * 70)

# Step 1: Check if langchain_openai is installed
print("\n[1/4] Checking if langchain_openai is installed...")
try:
    from langchain_openai import ChatOpenAI
    print("    ✓ langchain_openai is installed")
except ImportError as e:
    print(f"    ✗ FAILED: {e}")
    print("    Install: pip install langchain-openai")
    sys.exit(1)

# Step 2: Check environment variables
print("\n[2/4] Checking environment variables...")
api_base = os.getenv("OPENAI_API_BASE", "http://llm-proxy.ceui.cnap.comcast.net/v1")
api_key = os.getenv("OPENAI_API_KEY", "dummy-key-not-needed")
print(f"    API Base: {api_base}")
print(f"    API Key: {'[SET]' if os.getenv('OPENAI_API_KEY') else '[USING DEFAULT]'}")

# Step 3: Initialize ChatOpenAI with gpt-5-mini
print("\n[3/4] Initializing ChatOpenAI with gpt-5-mini...")
try:
    llm = ChatOpenAI(
        model="gpt-5-mini",
        base_url=api_base,
        api_key=api_key,
        temperature=0.7,
        max_tokens=100
    )
    print("    ✓ ChatOpenAI initialized successfully")
except Exception as e:
    print(f"    ✗ FAILED: {e}")
    sys.exit(1)

# Step 4: Test a simple call
print("\n[4/4] Testing actual API call to gpt-5-mini...")
try:
    response = llm.invoke("Say 'GPT-5-mini is working!' in 5 words or less.")
    result = response.content
    print(f"    ✓ API call successful!")
    print(f"    Response: {result}")
    print("\n" + "=" * 70)
    print("✓✓✓ VALIDATION PASSED - GPT-5-MINI IS WORKING! ✓✓✓")
    print("=" * 70)
except Exception as e:
    print(f"    ✗ FAILED: {e}")
    print("\nTroubleshooting:")
    print("1. Verify llm-proxy is running")
    print("2. Check network connectivity to llm-proxy.ceui.cnap.comcast.net")
    print("3. Verify gpt-5-mini is available on your llm-proxy")
    sys.exit(1)

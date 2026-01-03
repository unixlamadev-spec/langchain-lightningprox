#!/usr/bin/env python3
"""
Basic usage example for langchain-lightningprox.

Before running:
1. Get an LNBits wallet at https://demo.lnbits.com
2. Fund it with ~100 sats
3. Set your admin key below or in environment variable
"""

import os
from langchain_lightningprox import LightningProxLLM

# Load from environment or set directly
LNBITS_URL = os.getenv("LNBITS_URL", "https://demo.lnbits.com")
LNBITS_ADMIN_KEY = os.getenv("LNBITS_ADMIN_KEY", "your_admin_key_here")


def main():
    print("🚀 LightningProx + LangChain Example\n")
    
    # Initialize the LLM
    llm = LightningProxLLM(
        lnbits_url=LNBITS_URL,
        lnbits_admin_key=LNBITS_ADMIN_KEY,
        model="claude-sonnet-4-20250514",
        max_tokens=150
    )
    
    print(f"📡 LNBits: {LNBITS_URL}")
    print(f"🤖 Model: {llm.model}\n")
    
    # Example 1: Simple question
    print("=" * 50)
    print("Example 1: Simple Question")
    print("=" * 50)
    
    question = "What makes Lightning Network fast?"
    print(f"\n❓ Question: {question}\n")
    
    try:
        answer = llm.invoke(question)
        print(f"💡 Answer: {answer}\n")
    except RuntimeError as e:
        print(f"❌ Error: {e}\n")
        return
    
    # Example 2: Different question
    print("=" * 50)
    print("Example 2: Follow-up Question")
    print("=" * 50)
    
    question2 = "Give me one real-world use case for AI micropayments."
    print(f"\n❓ Question: {question2}\n")
    
    try:
        answer2 = llm.invoke(question2)
        print(f"💡 Answer: {answer2}\n")
    except RuntimeError as e:
        print(f"❌ Error: {e}\n")
        return
    
    print("=" * 50)
    print("✅ Done! Each query was paid via Lightning.")
    print("=" * 50)


if __name__ == "__main__":
    main()

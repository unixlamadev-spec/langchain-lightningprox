# langchain-lightningprox

LangChain integration for [LightningProx](https://lightningprox.com) — pay-per-use AI access via Bitcoin Lightning Network micropayments.

**No API keys. No accounts. No subscriptions. Just Lightning payments.**

## Installation

```bash
pip install langchain-lightningprox
```

## Quick Start

```python
from langchain_lightningprox import LightningProxLLM

# Initialize with your LNBits wallet
llm = LightningProxLLM(
    lnbits_url="https://demo.lnbits.com",
    lnbits_admin_key="your_admin_key_here"
)

# Use it like any LangChain LLM
response = llm.invoke("Explain quantum computing in one sentence.")
print(response)
```

## How It Works

```
┌──────────────┐      ┌───────────────┐      ┌─────────────┐
│  Your Code   │ ──▶  │ LightningProx │ ──▶  │  Claude/GPT │
│              │      │               │      │             │
│  (LNBits)    │ ─$─▶ │   (verify)    │      │  (respond)  │
│              │ ◀──  │               │ ◀──  │             │
└──────────────┘      └───────────────┘      └─────────────┘
```

1. Your code sends a prompt via the LangChain interface
2. LightningProx returns a Lightning invoice (~5-50 sats)
3. The library automatically pays via your LNBits wallet
4. LightningProx verifies payment and forwards to Claude/GPT
5. Response returned to your code

**All automatic. No manual intervention.**

## Setup

### 1. Get an LNBits Wallet

The easiest way to start is with [demo.lnbits.com](https://demo.lnbits.com):

1. Go to https://demo.lnbits.com
2. Create a new wallet
3. Click your wallet → **API info**
4. Copy the **Admin key**

### 2. Fund Your Wallet

Send a small amount of sats (~500) to your wallet's Lightning address. You can use any Lightning wallet (Phoenix, Muun, Cash App, etc.) to send.

### 3. Use It

```python
from langchain_lightningprox import LightningProxLLM

llm = LightningProxLLM(
    lnbits_url="https://demo.lnbits.com",
    lnbits_admin_key="your_admin_key_here"
)

# Single query
response = llm.invoke("What is Bitcoin?")
print(response)
```

## Configuration

```python
llm = LightningProxLLM(
    # Required
    lnbits_admin_key="your_admin_key",
    
    # Optional (defaults shown)
    lnbits_url="https://demo.lnbits.com",
    model="claude-sonnet-4-20250514",  # or "gpt-4-turbo"
    max_tokens=256,
    api_url="https://lightningprox.com/v1/messages",
)
```

### Available Models

| Model | Provider | Best For |
|-------|----------|----------|
| `claude-sonnet-4-20250514` | Anthropic | General use (default) |
| `claude-3-5-sonnet-20241022` | Anthropic | General use |
| `gpt-4-turbo` | OpenAI | General use |

## Examples

### Basic Usage

```python
from langchain_lightningprox import LightningProxLLM

llm = LightningProxLLM(
    lnbits_url="https://demo.lnbits.com",
    lnbits_admin_key="your_key"
)

# Simple question
answer = llm.invoke("What causes rainbows?")
print(answer)
```

### With Environment Variables

```python
import os
from langchain_lightningprox import LightningProxLLM

llm = LightningProxLLM(
    lnbits_url=os.getenv("LNBITS_URL", "https://demo.lnbits.com"),
    lnbits_admin_key=os.getenv("LNBITS_ADMIN_KEY")
)
```

### Multiple Queries

```python
questions = [
    "What is photosynthesis?",
    "How do airplanes fly?",
    "Why is the sky blue?"
]

for q in questions:
    print(f"Q: {q}")
    print(f"A: {llm.invoke(q)}\n")
```

### Using Different Models

```python
# Use GPT-4 Turbo instead
llm = LightningProxLLM(
    lnbits_admin_key="your_key",
    model="gpt-4-turbo"
)
```

## Pricing

- **~5-50 sats per request** (depending on response length)
- **50% discount** on cached/repeated queries
- No minimums, no subscriptions

At current rates, 1000 sats ≈ $1 USD gets you roughly 20-200 queries.

## Use Cases

### Autonomous Agents

Perfect for AI agents that need to pay for their own intelligence:

```python
class ResearchAgent:
    def __init__(self):
        self.llm = LightningProxLLM(
            lnbits_admin_key=os.getenv("AGENT_WALLET_KEY")
        )
    
    def research(self, topic):
        return self.llm.invoke(f"Summarize recent developments in {topic}")
```

### Pay-Per-Use Applications

Build apps where users pay per query without managing API keys:

```python
def answer_question(user_question, user_wallet_key):
    llm = LightningProxLLM(lnbits_admin_key=user_wallet_key)
    return llm.invoke(user_question)
```

### Cost-Controlled Experiments

Test prompts without committing to monthly subscriptions:

```python
# Each query costs ~5-50 sats
# Perfect for experimentation
for prompt_variation in prompt_variations:
    result = llm.invoke(prompt_variation)
    evaluate(result)
```

## Alternative Wallet Providers

While this library uses LNBits by default, you can integrate other Lightning wallets by subclassing:

```python
class StrikeLightningProx(LightningProxLLM):
    def _pay_invoice(self, payment_request: str) -> bool:
        # Implement Strike API payment
        pass
```

Supported wallet APIs:
- **LNBits** (built-in)
- **Strike** (subclass)
- **Voltage** (subclass)
- **LND** (subclass)
- Any wallet with a payment API

## Error Handling

```python
from langchain_lightningprox import LightningProxLLM

llm = LightningProxLLM(lnbits_admin_key="your_key")

try:
    response = llm.invoke("Hello!")
except RuntimeError as e:
    if "Payment failed" in str(e):
        print("Insufficient balance in wallet")
    else:
        print(f"Error: {e}")
```

## Why Lightning Payments?

- **Micropayments** — Pay fractions of a cent per request
- **No accounts** — Payment IS authentication
- **Instant** — Settlements in milliseconds
- **Global** — Works anywhere, no banking required
- **Autonomous** — Agents can pay without human intervention

## Links

- **Website:** [lightningprox.com](https://lightningprox.com)
- **Docs:** [lightningprox.com/docs](https://lightningprox.com/docs)
- **API Capabilities:** [lightningprox.com/api/capabilities](https://lightningprox.com/api/capabilities)
- **GitHub:** [github.com/unixlamadev-spec/langchain-lightningprox](https://github.com/unixlamadev-spec/langchain-lightningprox)

## License

MIT

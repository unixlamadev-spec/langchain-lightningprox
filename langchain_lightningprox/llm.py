"""LangChain integration for LightningProx - Pay-per-use AI via Lightning Network."""

from typing import Any, Dict, List, Optional
import requests
import time


class LightningProxLLM:
    """
    LangChain-compatible LLM that uses LightningProx for pay-per-use AI access.
    
    Requires a Lightning wallet (LNBits, Strike, etc.) for automatic payments.
    
    Example:
        ```python
        from langchain_lightningprox import LightningProxLLM
        
        llm = LightningProxLLM(
            lnbits_url="https://demo.lnbits.com",
            lnbits_admin_key="your_admin_key"
        )
        
        response = llm.invoke("What is the capital of France?")
        print(response)
        ```
    """
    
    def __init__(
        self,
        lnbits_url: str = "https://demo.lnbits.com",
        lnbits_admin_key: Optional[str] = None,
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 256,
        api_url: str = "https://lightningprox.com/v1/messages",
        payment_timeout: int = 30,
        **kwargs: Any
    ):
        """
        Initialize LightningProxLLM.
        
        Args:
            lnbits_url: URL of your LNBits instance (default: demo.lnbits.com)
            lnbits_admin_key: Admin key for LNBits wallet (required for auto-pay)
            model: AI model to use (default: claude-sonnet-4-20250514)
            max_tokens: Maximum tokens in response
            api_url: LightningProx API endpoint
            payment_timeout: Seconds to wait for payment confirmation
        """
        self.lnbits_url = lnbits_url.rstrip("/")
        self.lnbits_admin_key = lnbits_admin_key
        self.model = model
        self.max_tokens = max_tokens
        self.api_url = api_url
        self.payment_timeout = payment_timeout
        
        if not self.lnbits_admin_key:
            raise ValueError(
                "lnbits_admin_key is required for automatic payments. "
                "Get one at https://demo.lnbits.com"
            )
    
    @property
    def _llm_type(self) -> str:
        return "lightningprox"
    
    def _request(
        self, 
        messages: List[Dict[str, str]], 
        payment_hash: Optional[str] = None
    ) -> Dict[str, Any]:
        """Make a request to LightningProx API."""
        headers = {"Content-Type": "application/json"}
        if payment_hash:
            headers["X-Payment-Hash"] = payment_hash
        
        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": messages
        }
        
        response = requests.post(self.api_url, json=payload, headers=headers)
        return response.json()
    
    def _pay_invoice(self, payment_request: str) -> bool:
        """Pay a Lightning invoice via LNBits."""
        response = requests.post(
            f"{self.lnbits_url}/api/v1/payments",
            headers={
                "Content-Type": "application/json",
                "X-Api-Key": self.lnbits_admin_key
            },
            json={
                "out": True,
                "bolt11": payment_request
            }
        )
        return response.ok
    
    def invoke(self, prompt: str, **kwargs: Any) -> str:
        """
        Send a prompt and get a response, handling payment automatically.
        
        Args:
            prompt: The user's prompt/question
            **kwargs: Additional arguments (unused, for compatibility)
            
        Returns:
            The AI model's response text
            
        Raises:
            RuntimeError: If payment fails or no response received
        """
        messages = [{"role": "user", "content": prompt}]
        
        # Step 1: Request invoice
        result = self._request(messages)
        
        if "payment" not in result:
            # Already paid or error
            if "content" in result:
                return result["content"][0]["text"]
            raise RuntimeError(f"Unexpected response: {result}")
        
        payment = result["payment"]
        charge_id = payment["charge_id"]
        payment_request = payment["payment_request"]
        amount_sats = payment.get("amount_sats", "?")
        
        # Step 2: Pay the invoice
        if not self._pay_invoice(payment_request):
            raise RuntimeError(f"Payment failed for {amount_sats} sats")
        
        # Step 3: Retry with payment proof
        # Small delay to allow payment to propagate
        time.sleep(0.5)
        
        result = self._request(messages, payment_hash=charge_id)
        
        if "content" in result and len(result["content"]) > 0:
            return result["content"][0]["text"]
        
        raise RuntimeError(f"No response after payment: {result}")
    
    def __call__(self, prompt: str, **kwargs: Any) -> str:
        """Allow calling the LLM directly."""
        return self.invoke(prompt, **kwargs)
    
    # LangChain compatibility methods
    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs: Any) -> str:
        """LangChain compatibility method."""
        return self.invoke(prompt, **kwargs)
    
    def _generate(self, prompts: List[str], stop: Optional[List[str]] = None, **kwargs: Any) -> List[str]:
        """Generate responses for multiple prompts."""
        return [self.invoke(prompt, **kwargs) for prompt in prompts]


# Convenience alias
LightningProx = LightningProxLLM

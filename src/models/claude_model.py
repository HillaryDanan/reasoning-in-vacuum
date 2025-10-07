"""
Claude model wrapper using Anthropic API.

Implements BaseModel interface for Claude interactions.
"""

from typing import Dict, Any
import anthropic

from src.models.base_model import BaseModel, ModelResponse
from src.config import (
    ANTHROPIC_API_KEY,
    CLAUDE_MODEL,
    MODEL_TEMPERATURE,
    MAX_TOKENS,
)


class ClaudeModel(BaseModel):
    """
    Wrapper for Anthropic Claude API.
    
    Handles API calls, response parsing, and error handling specific
    to Anthropic's API.
    """
    
    def __init__(
        self,
        model_name: str = CLAUDE_MODEL,
        api_key: str = ANTHROPIC_API_KEY,
        temperature: float = MODEL_TEMPERATURE,
        max_tokens: int = MAX_TOKENS,
        **kwargs
    ):
        """
        Initialize Claude model.
        
        Args:
            model_name: Anthropic model identifier
            api_key: Anthropic API key
            temperature: Sampling temperature
            max_tokens: Maximum response tokens
            **kwargs: Additional parameters passed to BaseModel
        """
        super().__init__(
            model_name=model_name,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        # Initialize Anthropic client
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def _make_api_call(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Make API call to Anthropic.
        
        Args:
            prompt: Input prompt
            **kwargs: Additional Anthropic API parameters
            
        Returns:
            Raw API response as dictionary
        """
        # Override defaults with kwargs
        temperature = kwargs.get('temperature', self.temperature)
        max_tokens = kwargs.get('max_tokens', self.max_tokens)
        
        # Make API call
        response = self.client.messages.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            **{k: v for k, v in kwargs.items() 
               if k not in ['temperature', 'max_tokens']}
        )
        
        # Convert to dictionary for consistent handling
        return {
            'id': response.id,
            'type': response.type,
            'role': response.role,
            'content': response.content,
            'model': response.model,
            'stop_reason': response.stop_reason,
            'usage': {
                'input_tokens': response.usage.input_tokens,
                'output_tokens': response.usage.output_tokens,
            }
        }
    
    def _parse_response(self, raw_response: Dict[str, Any]) -> ModelResponse:
        """
        Parse Anthropic API response.
        
        Args:
            raw_response: Raw API response dictionary
            
        Returns:
            Standardized ModelResponse object
        """
        try:
            # Extract text from response (Claude returns list of content blocks)
            # Note: content blocks are TextBlock objects, not dicts
            text = raw_response['content'][0].text if raw_response['content'] else ""
            
            # Extract metadata
            metadata = {
                'stop_reason': raw_response['stop_reason'],
                'tokens_used': (
                    raw_response['usage']['input_tokens'] + 
                    raw_response['usage']['output_tokens']
                ),
                'prompt_tokens': raw_response['usage']['input_tokens'],
                'completion_tokens': raw_response['usage']['output_tokens'],
                'model': raw_response['model'],
            }
            
            return ModelResponse(
                text=text,
                model_name=self.model_name,
                success=True,
                metadata=metadata
            )
            
        except (KeyError, IndexError) as e:
            return ModelResponse(
                text="",
                model_name=self.model_name,
                success=False,
                error=f"Failed to parse response: {e}",
                metadata={'raw_response': raw_response}
            )


if __name__ == "__main__":
    # Test Claude model
    print("Testing Claude Model...")
    
    model = ClaudeModel()
    
    # Simple test
    test_prompt = "⨀ ⨁ ⨂ → ⨂ ⨀ ⨁\n⨃ ⨄ ⨅ → ⨅ ⨃ ⨄\n\n⨆ ⨇ ⨈ →"
    
    print(f"\nPrompt:\n{test_prompt}\n")
    print("Generating response...")
    
    response = model.generate(test_prompt)
    
    print(f"\nSuccess: {response.success}")
    print(f"Response: {response.text}")
    print(f"Metadata: {response.metadata}")
    print(f"\nModel Stats: {model.get_stats()}")
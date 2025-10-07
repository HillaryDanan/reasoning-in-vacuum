"""
GPT-4 model wrapper using OpenAI API.

Implements BaseModel interface for GPT-4 interactions.
"""

from typing import Dict, Any
import openai

from src.models.base_model import BaseModel, ModelResponse
from src.config import (
    OPENAI_API_KEY,
    GPT4_MODEL,
    MODEL_TEMPERATURE,
    MAX_TOKENS,
)


class GPT4Model(BaseModel):
    """
    Wrapper for OpenAI GPT-4 API.
    
    Handles API calls, response parsing, and error handling specific
    to OpenAI's API.
    """
    
    def __init__(
        self,
        model_name: str = GPT4_MODEL,
        api_key: str = OPENAI_API_KEY,
        temperature: float = MODEL_TEMPERATURE,
        max_tokens: int = MAX_TOKENS,
        **kwargs
    ):
        """
        Initialize GPT-4 model.
        
        Args:
            model_name: OpenAI model identifier
            api_key: OpenAI API key
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
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def _make_api_call(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Make API call to OpenAI.
        
        Args:
            prompt: Input prompt
            **kwargs: Additional OpenAI API parameters
            
        Returns:
            Raw API response as dictionary
        """
        # Override defaults with kwargs
        temperature = kwargs.get('temperature', self.temperature)
        max_tokens = kwargs.get('max_tokens', self.max_tokens)
        
        # Make API call
        response = self.client.chat.completions.create(
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
        return response.model_dump()
    
    def _parse_response(self, raw_response: Dict[str, Any]) -> ModelResponse:
        """
        Parse OpenAI API response.
        
        Args:
            raw_response: Raw API response dictionary
            
        Returns:
            Standardized ModelResponse object
        """
        try:
            # Extract text from response
            text = raw_response['choices'][0]['message']['content']
            
            # Extract metadata
            metadata = {
                'finish_reason': raw_response['choices'][0]['finish_reason'],
                'tokens_used': raw_response['usage']['total_tokens'],
                'prompt_tokens': raw_response['usage']['prompt_tokens'],
                'completion_tokens': raw_response['usage']['completion_tokens'],
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
    # Test GPT-4 model
    print("Testing GPT-4 Model...")
    
    model = GPT4Model()
    
    # Simple test
    test_prompt = "⨀ ⨁ ⨂ → ⨂ ⨀ ⨁\n⨃ ⨄ ⨅ → ⨅ ⨃ ⨄\n\n⨆ ⨇ ⨈ →"
    
    print(f"\nPrompt:\n{test_prompt}\n")
    print("Generating response...")
    
    response = model.generate(test_prompt)
    
    print(f"\nSuccess: {response.success}")
    print(f"Response: {response.text}")
    print(f"Metadata: {response.metadata}")
    print(f"\nModel Stats: {model.get_stats()}")
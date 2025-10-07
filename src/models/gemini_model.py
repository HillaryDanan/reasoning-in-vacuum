"""
Gemini model wrapper using Google Generative AI API.

Implements BaseModel interface for Gemini interactions.
"""

from typing import Dict, Any
import google.generativeai as genai

from src.models.base_model import BaseModel, ModelResponse
from src.config import (
    GOOGLE_API_KEY,
    GEMINI_MODEL,
    MODEL_TEMPERATURE,
    MAX_TOKENS,
)


class GeminiModel(BaseModel):
    """
    Wrapper for Google Gemini API.
    
    Handles API calls, response parsing, and error handling specific
    to Google's Generative AI API.
    """
    
    def __init__(
        self,
        model_name: str = GEMINI_MODEL,
        api_key: str = GOOGLE_API_KEY,
        temperature: float = MODEL_TEMPERATURE,
        max_tokens: int = MAX_TOKENS,
        **kwargs
    ):
        """
        Initialize Gemini model.
        
        Args:
            model_name: Google model identifier
            api_key: Google API key
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
        
        # Configure Google API
        genai.configure(api_key=self.api_key)
        
        # Initialize model
        self.model = genai.GenerativeModel(self.model_name)
    
    def _make_api_call(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Make API call to Google Generative AI.
        
        Args:
            prompt: Input prompt
            **kwargs: Additional Google API parameters
            
        Returns:
            Raw API response as dictionary
        """
        # Override defaults with kwargs
        temperature = kwargs.get('temperature', self.temperature)
        max_tokens = kwargs.get('max_output_tokens', self.max_tokens)
        
        # Create generation config
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
            **{k: v for k, v in kwargs.items() 
               if k not in ['temperature', 'max_output_tokens']}
        )
        
        # Make API call
        response = self.model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        # Convert to dictionary for consistent handling
        return {
            'text': response.text,
            'candidates': [
                {
                    'content': {
                        'parts': [{'text': part.text} for part in candidate.content.parts],
                        'role': candidate.content.role,
                    },
                    'finish_reason': candidate.finish_reason,
                    'safety_ratings': [
                        {
                            'category': rating.category,
                            'probability': rating.probability,
                        }
                        for rating in candidate.safety_ratings
                    ],
                }
                for candidate in response.candidates
            ],
            'usage_metadata': {
                'prompt_token_count': response.usage_metadata.prompt_token_count,
                'candidates_token_count': response.usage_metadata.candidates_token_count,
                'total_token_count': response.usage_metadata.total_token_count,
            } if hasattr(response, 'usage_metadata') else None,
        }
    
    def _parse_response(self, raw_response: Dict[str, Any]) -> ModelResponse:
        """
        Parse Google Generative AI response.
        
        Args:
            raw_response: Raw API response dictionary
            
        Returns:
            Standardized ModelResponse object
        """
        try:
            # Extract text from response
            text = raw_response['text']
            
            # Extract metadata
            metadata = {
                'finish_reason': raw_response['candidates'][0]['finish_reason'],
                'model': self.model_name,
            }
            
            # Add token counts if available
            if raw_response.get('usage_metadata'):
                metadata['tokens_used'] = raw_response['usage_metadata']['total_token_count']
                metadata['prompt_tokens'] = raw_response['usage_metadata']['prompt_token_count']
                metadata['completion_tokens'] = raw_response['usage_metadata']['candidates_token_count']
            
            # Add safety ratings
            if raw_response['candidates'][0].get('safety_ratings'):
                metadata['safety_ratings'] = raw_response['candidates'][0]['safety_ratings']
            
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
    # Test Gemini model
    print("Testing Gemini Model...")
    
    model = GeminiModel()
    
    # Simple test
    test_prompt = "⨀ ⨁ ⨂ → ⨂ ⨀ ⨁\n⨃ ⨄ ⨅ → ⨅ ⨃ ⨄\n\n⨆ ⨇ ⨈ →"
    
    print(f"\nPrompt:\n{test_prompt}\n")
    print("Generating response...")
    
    response = model.generate(test_prompt)
    
    print(f"\nSuccess: {response.success}")
    print(f"Response: {response.text}")
    print(f"Metadata: {response.metadata}")
    print(f"\nModel Stats: {model.get_stats()}")
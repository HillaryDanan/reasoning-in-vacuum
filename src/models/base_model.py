"""
Base model interface for LLM API interactions.

Provides abstract base class for consistent model interactions across
different LLM providers (OpenAI, Anthropic, Google).
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
import time
import logging

from src.config import (
    MAX_RETRIES,
    RATE_LIMIT_DELAY,
    REQUEST_TIMEOUT,
    MODEL_TEMPERATURE,
    MAX_TOKENS,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ModelResponse:
    """
    Standardized response format across all models.
    
    Attributes:
        text: The model's text response
        model_name: Name/ID of the model used
        success: Whether the request succeeded
        error: Error message if failed
        metadata: Additional metadata (tokens used, latency, etc.)
    """
    text: str
    model_name: str
    success: bool = True
    error: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BaseModel(ABC):
    """
    Abstract base class for LLM models.
    
    All model wrappers (GPT-4, Claude, Gemini) must implement this interface
    to ensure consistent behavior across experiments.
    """
    
    def __init__(
        self,
        model_name: str,
        api_key: str,
        temperature: float = MODEL_TEMPERATURE,
        max_tokens: int = MAX_TOKENS,
        max_retries: int = MAX_RETRIES,
        rate_limit_delay: float = RATE_LIMIT_DELAY,
    ):
        """
        Initialize base model.
        
        Args:
            model_name: Model identifier (e.g., "gpt-4", "claude-3-5-sonnet")
            api_key: API authentication key
            temperature: Sampling temperature (0.0 for deterministic)
            max_tokens: Maximum tokens in response
            max_retries: Maximum retry attempts for failed requests
            rate_limit_delay: Delay between requests (seconds)
        """
        self.model_name = model_name
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.max_retries = max_retries
        self.rate_limit_delay = rate_limit_delay
        
        # Request tracking
        self.request_count = 0
        self.total_tokens = 0
        self.failed_requests = 0
        
        logger.info(f"Initialized {self.__class__.__name__} with model: {model_name}")
    
    @abstractmethod
    def _make_api_call(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Make API call to model provider.
        
        This must be implemented by each model wrapper to handle
        provider-specific API details.
        
        Args:
            prompt: Input prompt string
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Dict containing raw API response
            
        Raises:
            Exception: If API call fails after retries
        """
        pass
    
    @abstractmethod
    def _parse_response(self, raw_response: Dict[str, Any]) -> ModelResponse:
        """
        Parse raw API response into standardized format.
        
        Args:
            raw_response: Raw API response dictionary
            
        Returns:
            ModelResponse object
        """
        pass
    
    def generate(
        self,
        prompt: str,
        log_request: bool = True,
        **kwargs
    ) -> ModelResponse:
        """
        Generate response from model with retry logic.
        
        This is the main public interface for getting model responses.
        Handles retries, rate limiting, and error logging.
        
        Args:
            prompt: Input prompt string
            log_request: Whether to log this request
            **kwargs: Additional parameters for API call
            
        Returns:
            ModelResponse object
        """
        if log_request:
            logger.info(f"Making request to {self.model_name}")
            logger.debug(f"Prompt: {prompt[:100]}...")
        
        # Rate limiting
        if self.request_count > 0:
            time.sleep(self.rate_limit_delay)
        
        # Retry loop
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                # Make API call
                start_time = time.time()
                raw_response = self._make_api_call(prompt, **kwargs)
                latency = time.time() - start_time
                
                # Parse response
                response = self._parse_response(raw_response)
                
                # Add latency to metadata
                response.metadata['latency_seconds'] = latency
                response.metadata['attempt'] = attempt + 1
                
                # Update tracking
                self.request_count += 1
                if 'tokens_used' in response.metadata:
                    self.total_tokens += response.metadata['tokens_used']
                
                if log_request:
                    logger.info(
                        f"✓ Success (attempt {attempt + 1}, "
                        f"{latency:.2f}s, "
                        f"{response.metadata.get('tokens_used', '?')} tokens)"
                    )
                
                return response
                
            except Exception as e:
                last_exception = e
                logger.warning(
                    f"⚠ Attempt {attempt + 1}/{self.max_retries} failed: {e}"
                )
                
                if attempt < self.max_retries - 1:
                    # Exponential backoff
                    wait_time = self.rate_limit_delay * (2 ** attempt)
                    logger.info(f"Waiting {wait_time:.1f}s before retry...")
                    time.sleep(wait_time)
        
        # All retries failed
        self.failed_requests += 1
        error_msg = f"All {self.max_retries} attempts failed. Last error: {last_exception}"
        logger.error(error_msg)
        
        return ModelResponse(
            text="",
            model_name=self.model_name,
            success=False,
            error=error_msg,
            metadata={'attempts': self.max_retries}
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get usage statistics for this model instance.
        
        Returns:
            Dictionary with request counts, token usage, etc.
        """
        return {
            'model_name': self.model_name,
            'total_requests': self.request_count,
            'failed_requests': self.failed_requests,
            'success_rate': (
                (self.request_count - self.failed_requests) / self.request_count
                if self.request_count > 0 else 0.0
            ),
            'total_tokens': self.total_tokens,
        }
    
    def reset_stats(self):
        """Reset usage statistics."""
        self.request_count = 0
        self.total_tokens = 0
        self.failed_requests = 0
        logger.info(f"Reset statistics for {self.model_name}")
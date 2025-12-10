"""LLM service for OpenAI GPT-4 integration."""
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class LLMService:
    """Service for interacting with OpenAI GPT-4."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4-turbo-preview"
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        functions: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Dict[str, Any]:
        """Get chat completion from GPT-4."""
        try:
            kwargs = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            if functions:
                kwargs["functions"] = functions
                kwargs["function_call"] = "auto"
            
            response = await self.client.chat.completions.create(**kwargs)
            
            result = {
                "content": response.choices[0].message.content,
                "role": response.choices[0].message.role,
                "function_call": None
            }
            
            if hasattr(response.choices[0].message, 'function_call'):
                result["function_call"] = response.choices[0].message.function_call
            
            logger.info(
                "llm_completion",
                model=self.model,
                tokens=response.usage.total_tokens
            )
            
            return result
            
        except Exception as e:
            logger.error("llm_error", error=str(e))
            raise
    
    async def chat_completion_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000
    ):
        """Get streaming chat completion from GPT-4."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error("llm_stream_error", error=str(e))
            raise
    
    async def get_embeddings(self, text: str) -> List[float]:
        """Get embeddings for text."""
        try:
            response = await self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error("embedding_error", error=str(e))
            raise


# Global LLM service instance
llm_service = LLMService()



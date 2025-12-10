"""Base agent class for all specialized agents."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.services.llm_service import llm_service
from app.utils.logger import get_logger

logger = get_logger(__name__)


class BaseAgent(ABC):
    """Base class for all agents."""
    
    def __init__(self, agent_type: str, system_prompt: str):
        """
        Initialize base agent.
        
        Args:
            agent_type: Type of agent (engage, verify, etc.)
            system_prompt: System prompt for this agent
        """
        self.agent_type = agent_type
        self.system_prompt = system_prompt
        self.llm_service = llm_service
        self.logger = get_logger(f"agent.{agent_type}")
    
    async def process(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process user message and return response.
        
        Args:
            user_message: User's message
            conversation_history: Previous messages
            context: Conversation context and state
            
        Returns:
            Dict containing response and updated context
        """
        try:
            # Build messages for LLM
            messages = self._build_messages(
                user_message,
                conversation_history,
                context
            )
            
            # Get tools/functions for this agent
            functions = self._get_functions()
            
            # Get LLM response
            response = await self.llm_service.chat_completion(
                messages=messages,
                functions=functions,
                temperature=0.7
            )
            
            # Handle function calls if any
            if response.get("function_call"):
                function_result = await self._handle_function_call(
                    response["function_call"],
                    context
                )
                
                # Get final response after function execution
                messages.append({
                    "role": "assistant",
                    "content": None,
                    "function_call": response["function_call"]
                })
                messages.append({
                    "role": "function",
                    "name": response["function_call"]["name"],
                    "content": str(function_result)
                })
                
                final_response = await self.llm_service.chat_completion(
                    messages=messages,
                    temperature=0.7
                )
                response_content = final_response["content"]
            else:
                response_content = response["content"]
            
            # Process the response
            processed_response = await self._process_response(
                response_content,
                context
            )
            
            self.logger.info(
                "agent_processed",
                agent_type=self.agent_type,
                message_length=len(user_message)
            )
            
            return processed_response
            
        except Exception as e:
            self.logger.error("agent_error", error=str(e))
            return {
                "response": "I apologize, but I'm having trouble processing your request. Could you please try again?",
                "context": context,
                "error": True
            }
    
    def _build_messages(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        context: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Build messages list for LLM."""
        messages = [
            {"role": "system", "content": self._get_dynamic_prompt(context)}
        ]
        
        # Add relevant conversation history (last 10 messages)
        for msg in conversation_history[-10:]:
            messages.append(msg)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        return messages
    
    def _get_dynamic_prompt(self, context: Dict[str, Any]) -> str:
        """Get dynamic system prompt based on context."""
        prompt = self.system_prompt
        
        # Add context-specific information to prompt
        if context.get("user_name"):
            prompt += f"\n\nCustomer name: {context['user_name']}"
        
        if context.get("preferred_language"):
            prompt += f"\nPreferred language: {context['preferred_language']}"
        
        return prompt
    
    @abstractmethod
    def _get_functions(self) -> Optional[List[Dict[str, Any]]]:
        """Get function definitions for this agent."""
        pass
    
    @abstractmethod
    async def _handle_function_call(
        self,
        function_call: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Any:
        """Handle function call from LLM."""
        pass
    
    @abstractmethod
    async def _process_response(
        self,
        response: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process agent response and update context."""
        pass
    
    def should_handoff(self, context: Dict[str, Any]) -> Optional[str]:
        """
        Determine if conversation should be handed off to another agent.
        
        Returns:
            Agent type to hand off to, or None
        """
        return None



"""Master Agent - Orchestrates conversation and routes to specialized agents."""
from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.utils.logger import get_logger
import os

logger = get_logger(__name__)


class MasterAgent(BaseAgent):
    """Master agent that orchestrates the conversation."""
    
    def __init__(self):
        """Initialize master agent."""
        # Load system prompt
        prompt_path = os.path.join("agents", "prompts", "master_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()
        
        super().__init__("master", system_prompt)
    
    def _get_functions(self) -> Optional[List[Dict[str, Any]]]:
        """Get function definitions for routing."""
        return [
            {
                "name": "route_to_agent",
                "description": "Route the conversation to a specialized agent",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "agent_type": {
                            "type": "string",
                            "enum": ["engage", "verify", "underwrite", "sanction"],
                            "description": "The agent to route to"
                        },
                        "reason": {
                            "type": "string",
                            "description": "Reason for routing to this agent"
                        }
                    },
                    "required": ["agent_type", "reason"]
                }
            }
        ]
    
    async def _handle_function_call(
        self,
        function_call: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Any:
        """Handle function call for routing."""
        import json
        
        if function_call["name"] == "route_to_agent":
            args = json.loads(function_call["arguments"])
            agent_type = args["agent_type"]
            reason = args["reason"]
            
            logger.info(
                "routing_to_agent",
                agent_type=agent_type,
                reason=reason
            )
            
            return {
                "agent_type": agent_type,
                "reason": reason,
                "success": True
            }
        
        return {"success": False}
    
    async def _process_response(
        self,
        response: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process master agent response."""
        return {
            "response": response,
            "context": context,
            "agent": "master"
        }
    
    def determine_next_agent(self, context: Dict[str, Any]) -> Optional[str]:
        """
        Determine next agent based on conversation context.
        
        Args:
            context: Conversation context
            
        Returns:
            Agent type or None
        """
        current_stage = context.get("stage", "initial")
        
        # Stage-based routing
        stage_to_agent = {
            "initial": "engage",
            "qualified": "verify",
            "documents_verified": "underwrite",
            "approved": "sanction"
        }
        
        return stage_to_agent.get(current_stage)



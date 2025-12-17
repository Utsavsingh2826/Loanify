"""Engage Agent - Sales and relationship management."""
from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.utils.logger import get_logger
import os
import json

logger = get_logger(__name__)


class EngageAgent(BaseAgent):
    """Agent responsible for customer engagement and lead qualification."""
    
    def __init__(self):
        """Initialize engage agent."""
        # Path resolution: prompts are mounted at /agents in container
        prompt_path = "/agents/prompts/engage_prompt.txt"
        with open(prompt_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()
        
        super().__init__("engage", system_prompt)
    
    def _get_functions(self) -> Optional[List[Dict[str, Any]]]:
        """Get function definitions for engagement."""
        return [
            {
                "name": "capture_customer_requirements",
                "description": "Capture customer's loan requirements",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "loan_purpose": {
                            "type": "string",
                            "description": "Purpose of the loan"
                        },
                        "loan_amount": {
                            "type": "number",
                            "description": "Desired loan amount"
                        },
                        "tenure_months": {
                            "type": "number",
                            "description": "Desired tenure in months"
                        },
                        "monthly_income": {
                            "type": "number",
                            "description": "Customer's monthly income"
                        },
                        "employment_type": {
                            "type": "string",
                            "enum": ["salaried", "self_employed", "business"],
                            "description": "Type of employment"
                        }
                    },
                    "required": ["loan_purpose"]
                }
            },
            {
                "name": "check_basic_eligibility",
                "description": "Check if customer meets basic eligibility criteria",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "monthly_income": {
                            "type": "number",
                            "description": "Monthly income"
                        },
                        "employment_type": {
                            "type": "string",
                            "description": "Employment type"
                        }
                    },
                    "required": ["monthly_income", "employment_type"]
                }
            }
        ]
    
    async def _handle_function_call(
        self,
        function_call: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Any:
        """Handle function calls."""
        args = json.loads(function_call["arguments"])
        
        if function_call["name"] == "capture_customer_requirements":
            # Store requirements in context
            context["loan_requirements"] = args
            logger.info("customer_requirements_captured", **args)
            return {
                "success": True,
                "message": "Requirements captured successfully"
            }
        
        elif function_call["name"] == "check_basic_eligibility":
            # Basic eligibility check
            monthly_income = args["monthly_income"]
            employment_type = args["employment_type"]
            
            # Minimum income requirements
            min_income = 15000 if employment_type == "salaried" else 25000
            
            eligible = monthly_income >= min_income
            
            context["basic_eligibility"] = {
                "eligible": eligible,
                "monthly_income": monthly_income,
                "employment_type": employment_type
            }
            
            logger.info(
                "eligibility_checked",
                eligible=eligible,
                income=monthly_income
            )
            
            if eligible:
                return {
                    "eligible": True,
                    "message": f"You meet the basic eligibility criteria! With your income of ₹{monthly_income}, you can proceed with the loan application."
                }
            else:
                return {
                    "eligible": False,
                    "message": f"Unfortunately, the minimum monthly income requirement is ₹{min_income} for {employment_type} applicants."
                }
        
        return {"success": False}
    
    async def _process_response(
        self,
        response: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process engage agent response."""
        # Check if customer is qualified to move to verification
        should_proceed = self._should_proceed_to_verification(context)
        
        if should_proceed:
            context["stage"] = "qualified"
            context["next_agent"] = "verify"
        
        return {
            "response": response,
            "context": context,
            "agent": "engage",
            "should_handoff": should_proceed
        }
    
    def _should_proceed_to_verification(self, context: Dict[str, Any]) -> bool:
        """Check if customer should proceed to verification."""
        # Check if requirements are captured and basic eligibility passed
        requirements = context.get("loan_requirements", {})
        eligibility = context.get("basic_eligibility", {})
        
        has_requirements = bool(requirements.get("loan_purpose"))
        is_eligible = eligibility.get("eligible", False)
        
        return has_requirements and is_eligible



"""Sanction Agent - Loan sanction letter generation."""
from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.utils.logger import get_logger
import os
import json
from datetime import datetime

logger = get_logger(__name__)


class SanctionAgent(BaseAgent):
    """Agent responsible for generating loan sanction letters."""
    
    def __init__(self):
        """Initialize sanction agent."""
        # Path resolution: prompts are mounted at /agents in container
        prompt_path = "/agents/prompts/sanction_prompt.txt"
        with open(prompt_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()
        
        super().__init__("sanction", system_prompt)
    
    def _get_functions(self) -> Optional[List[Dict[str, Any]]]:
        """Get function definitions for sanction."""
        return [
            {
                "name": "generate_sanction_letter",
                "description": "Generate PDF sanction letter",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "customer_name": {
                            "type": "string",
                            "description": "Customer's full name"
                        },
                        "email": {
                            "type": "string",
                            "description": "Customer's email address"
                        },
                        "loan_amount": {
                            "type": "number",
                            "description": "Approved loan amount"
                        },
                        "interest_rate": {
                            "type": "number",
                            "description": "Interest rate"
                        },
                        "tenure_months": {
                            "type": "number",
                            "description": "Loan tenure in months"
                        },
                        "monthly_emi": {
                            "type": "number",
                            "description": "Monthly EMI amount"
                        }
                    },
                    "required": ["customer_name", "email", "loan_amount", "interest_rate", "tenure_months", "monthly_emi"]
                }
            },
            {
                "name": "send_sanction_letter",
                "description": "Send sanction letter via email",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {
                            "type": "string",
                            "description": "Email address"
                        },
                        "sanction_letter_path": {
                            "type": "string",
                            "description": "Path to sanction letter PDF"
                        }
                    },
                    "required": ["email", "sanction_letter_path"]
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
        
        if function_call["name"] == "generate_sanction_letter":
            # Import PDF service
            from app.services.pdf_service import pdf_service
            
            # Generate sanction letter
            letter_data = {
                "customer_name": args["customer_name"],
                "email": args["email"],
                "loan_amount": args["loan_amount"],
                "interest_rate": args["interest_rate"],
                "tenure_months": args["tenure_months"],
                "monthly_emi": args["monthly_emi"],
                "sanction_date": datetime.now().strftime("%Y-%m-%d"),
                "application_number": context.get("application_number", "APP" + str(datetime.now().timestamp()).replace(".", ""))
            }
            
            pdf_path = await pdf_service.generate_sanction_letter(letter_data)
            
            # Store in context
            context["sanction_letter_path"] = pdf_path
            context["sanction_letter_generated"] = True
            
            logger.info(
                "sanction_letter_generated",
                application_number=letter_data["application_number"],
                customer=args["customer_name"]
            )
            
            return {
                "success": True,
                "pdf_path": pdf_path,
                "message": "Sanction letter generated successfully"
            }
        
        elif function_call["name"] == "send_sanction_letter":
            # Import notification service
            from app.services.notification_service import notification_service
            
            email = args["email"]
            pdf_path = args["sanction_letter_path"]
            
            # Send email
            result = await notification_service.send_email(
                to_email=email,
                subject="Loan Sanction Letter - LoaniFi",
                body="Congratulations! Please find your loan sanction letter attached.",
                attachment_path=pdf_path
            )
            
            context["sanction_letter_sent"] = True
            
            logger.info("sanction_letter_sent", email=email)
            
            return {
                "success": result,
                "message": f"Sanction letter sent to {email}"
            }
        
        return {"success": False}
    
    async def _process_response(
        self,
        response: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process sanction agent response."""
        # Check if process is complete
        is_complete = context.get("sanction_letter_sent", False)
        
        if is_complete:
            context["stage"] = "sanctioned"
            context["completed"] = True
        
        return {
            "response": response,
            "context": context,
            "agent": "sanction",
            "completed": is_complete
        }



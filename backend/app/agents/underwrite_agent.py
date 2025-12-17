"""Underwrite Agent - Risk assessment and loan eligibility."""
from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.utils.logger import get_logger
import os
import json

logger = get_logger(__name__)


class UnderwriteAgent(BaseAgent):
    """Agent responsible for credit risk assessment and underwriting."""
    
    def __init__(self):
        """Initialize underwrite agent."""
        # Path resolution: prompts are mounted at /agents in container
        prompt_path = "/agents/prompts/underwrite_prompt.txt"
        with open(prompt_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()
        
        super().__init__("underwrite", system_prompt)
    
    def _get_functions(self) -> Optional[List[Dict[str, Any]]]:
        """Get function definitions for underwriting."""
        return [
            {
                "name": "calculate_eligibility",
                "description": "Calculate loan eligibility based on income and obligations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "monthly_income": {
                            "type": "number",
                            "description": "Monthly income"
                        },
                        "existing_emis": {
                            "type": "number",
                            "description": "Existing monthly EMI obligations"
                        },
                        "credit_score": {
                            "type": "number",
                            "description": "Credit score"
                        },
                        "requested_amount": {
                            "type": "number",
                            "description": "Requested loan amount"
                        },
                        "tenure_months": {
                            "type": "number",
                            "description": "Requested tenure in months"
                        }
                    },
                    "required": ["monthly_income", "credit_score"]
                }
            },
            {
                "name": "determine_interest_rate",
                "description": "Determine interest rate based on risk profile",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "credit_score": {
                            "type": "number",
                            "description": "Credit score"
                        },
                        "employment_type": {
                            "type": "string",
                            "description": "Employment type"
                        },
                        "monthly_income": {
                            "type": "number",
                            "description": "Monthly income"
                        }
                    },
                    "required": ["credit_score", "employment_type"]
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
        
        if function_call["name"] == "calculate_eligibility":
            monthly_income = args["monthly_income"]
            existing_emis = args.get("existing_emis", 0)
            credit_score = args["credit_score"]
            requested_amount = args.get("requested_amount")
            tenure_months = args.get("tenure_months", 36)
            
            # Calculate DTI
            dti = (existing_emis / monthly_income) * 100 if monthly_income > 0 else 100
            
            # Calculate maximum EMI (50% of income minus existing obligations)
            max_emi = (monthly_income * 0.5) - existing_emis
            
            # Determine interest rate
            interest_rate = self._get_interest_rate(
                credit_score,
                context.get("employment_type", "salaried"),
                monthly_income
            )
            
            # Calculate maximum loan amount
            monthly_rate = interest_rate / 100 / 12
            if monthly_rate > 0:
                max_loan_amount = (max_emi * (1 - (1 + monthly_rate) ** -tenure_months)) / monthly_rate
            else:
                max_loan_amount = max_emi * tenure_months
            
            # Risk assessment
            risk_category = self._assess_risk(credit_score, dti)
            
            # Approval decision
            approved = dti < 60 and credit_score >= 600 and max_loan_amount > 0
            
            if approved and requested_amount:
                # Approve requested amount if within eligibility
                approved_amount = min(requested_amount, max_loan_amount)
            else:
                approved_amount = max_loan_amount if approved else 0
            
            # Calculate EMI for approved amount
            if approved_amount > 0 and monthly_rate > 0:
                emi = (approved_amount * monthly_rate * (1 + monthly_rate) ** tenure_months) / ((1 + monthly_rate) ** tenure_months - 1)
            else:
                emi = 0
            
            result = {
                "approved": approved,
                "approved_amount": round(approved_amount, 2),
                "max_eligible_amount": round(max_loan_amount, 2),
                "interest_rate": interest_rate,
                "tenure_months": tenure_months,
                "monthly_emi": round(emi, 2),
                "dti_ratio": round(dti, 2),
                "risk_category": risk_category,
                "credit_score": credit_score
            }
            
            # Store in context
            context["underwriting_result"] = result
            
            logger.info("eligibility_calculated", **result)
            
            return result
        
        elif function_call["name"] == "determine_interest_rate":
            credit_score = args["credit_score"]
            employment_type = args["employment_type"]
            monthly_income = args.get("monthly_income", 0)
            
            interest_rate = self._get_interest_rate(
                credit_score,
                employment_type,
                monthly_income
            )
            
            return {
                "interest_rate": interest_rate,
                "explanation": f"Rate based on credit score of {credit_score} and {employment_type} employment"
            }
        
        return {"success": False}
    
    def _get_interest_rate(
        self,
        credit_score: int,
        employment_type: str,
        monthly_income: float
    ) -> float:
        """Calculate interest rate based on risk factors."""
        if credit_score >= 750:
            if employment_type == "salaried" and monthly_income >= 50000:
                return 10.5
            elif employment_type == "self_employed" and monthly_income >= 75000:
                return 11.5
            else:
                return 12.5
        elif credit_score >= 700:
            if employment_type == "salaried" and monthly_income >= 30000:
                return 13.5
            else:
                return 15.0
        elif credit_score >= 650:
            if employment_type == "salaried":
                return 17.0
            else:
                return 18.5
        else:
            return 22.0
    
    def _assess_risk(self, credit_score: int, dti: float) -> str:
        """Assess risk category."""
        if credit_score >= 750 and dti < 35:
            return "low"
        elif credit_score >= 650 and dti < 45:
            return "medium"
        else:
            return "high"
    
    async def _process_response(
        self,
        response: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process underwrite agent response."""
        # Check if loan is approved and ready for sanction
        should_proceed = self._should_proceed_to_sanction(context)
        
        if should_proceed:
            context["stage"] = "approved"
            context["next_agent"] = "sanction"
        
        return {
            "response": response,
            "context": context,
            "agent": "underwrite",
            "should_handoff": should_proceed
        }
    
    def _should_proceed_to_sanction(self, context: Dict[str, Any]) -> bool:
        """Check if ready to proceed to sanction."""
        underwriting_result = context.get("underwriting_result", {})
        return underwriting_result.get("approved", False)



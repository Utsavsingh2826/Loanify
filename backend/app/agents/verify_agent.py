"""Verify Agent - Document and identity verification."""
from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.utils.logger import get_logger
import os
import json

logger = get_logger(__name__)


class VerifyAgent(BaseAgent):
    """Agent responsible for document verification and KYC."""
    
    def __init__(self):
        """Initialize verify agent."""
        # Path resolution: prompts are mounted at /agents in container
        prompt_path = "/agents/prompts/verify_prompt.txt"
        with open(prompt_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()
        
        super().__init__("verify", system_prompt)
        
        # Required documents
        self.required_documents = [
            "pan_card",
            "aadhaar_card",
            "bank_statement",
            "income_proof",
            "address_proof",
            "photo"
        ]
    
    def _get_functions(self) -> Optional[List[Dict[str, Any]]]:
        """Get function definitions for verification."""
        return [
            {
                "name": "check_document_status",
                "description": "Check status of document collection",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "verify_document",
                "description": "Verify a specific document",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "document_type": {
                            "type": "string",
                            "description": "Type of document to verify"
                        },
                        "document_id": {
                            "type": "string",
                            "description": "Document ID"
                        }
                    },
                    "required": ["document_type", "document_id"]
                }
            },
            {
                "name": "check_credit_score",
                "description": "Check customer's credit score",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pan_number": {
                            "type": "string",
                            "description": "PAN number for credit check"
                        }
                    },
                    "required": ["pan_number"]
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
        
        if function_call["name"] == "check_document_status":
            submitted_docs = context.get("submitted_documents", [])
            verified_docs = context.get("verified_documents", [])
            
            pending_docs = [
                doc for doc in self.required_documents 
                if doc not in submitted_docs
            ]
            
            return {
                "total_required": len(self.required_documents),
                "submitted": len(submitted_docs),
                "verified": len(verified_docs),
                "pending": pending_docs
            }
        
        elif function_call["name"] == "verify_document":
            # Mock document verification
            document_type = args["document_type"]
            document_id = args["document_id"]
            
            # Import verification services
            from app.services.document_service import document_service
            
            verification_result = await document_service.verify_document(
                document_id,
                document_type
            )
            
            # Update context
            if "verified_documents" not in context:
                context["verified_documents"] = []
            
            if verification_result.get("valid"):
                context["verified_documents"].append(document_type)
            
            logger.info(
                "document_verified",
                document_type=document_type,
                valid=verification_result.get("valid")
            )
            
            return verification_result
        
        elif function_call["name"] == "check_credit_score":
            pan_number = args["pan_number"]
            
            # Import credit score service
            from app.services.credit_score_service import credit_score_service
            
            credit_data = await credit_score_service.get_credit_score(pan_number)
            
            # Store in context
            context["credit_score"] = credit_data["score"]
            context["credit_report"] = credit_data
            
            logger.info("credit_score_checked", score=credit_data["score"])
            
            return credit_data
        
        return {"success": False}
    
    async def _process_response(
        self,
        response: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process verify agent response."""
        # Check if all documents verified and ready for underwriting
        should_proceed = self._should_proceed_to_underwriting(context)
        
        if should_proceed:
            context["stage"] = "documents_verified"
            context["next_agent"] = "underwrite"
        
        return {
            "response": response,
            "context": context,
            "agent": "verify",
            "should_handoff": should_proceed
        }
    
    def _should_proceed_to_underwriting(self, context: Dict[str, Any]) -> bool:
        """Check if ready to proceed to underwriting."""
        verified_docs = context.get("verified_documents", [])
        credit_score = context.get("credit_score")
        
        # All documents verified and credit score obtained
        all_docs_verified = len(verified_docs) >= len(self.required_documents)
        has_credit_score = credit_score is not None
        
        return all_docs_verified and has_credit_score



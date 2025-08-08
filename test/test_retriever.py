import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from nodes.retriever import retrieve_context

class TestRetriever:
    """Test cases for the context retriever node."""
    
    def test_billing_context_retrieval(self):
        """Test retrieval of billing-related context."""
        state = {
            "ticket_id": "TEST-001",
            "subject": "Refund request",
            "description": "I need a refund for my subscription",
            "category": "Billing"
        }
        
        result = retrieve_context(state)
        
        assert "context" in result
        assert len(result["context"]) > 0
        assert result["processing_step"] == "context_retrieved"
        assert "context_docs" in result
    
    def test_technical_context_retrieval(self):
        """Test retrieval of technical context."""
        state = {
            "ticket_id": "TEST-002",
            "subject": "API error 401",
            "description": "Getting unauthorized errors when calling the API",
            "category": "Technical"
        }
        
        result = retrieve_context(state)
        
        assert "context" in result
        assert len(result["context"]) > 0
        assert result["processing_step"] == "context_retrieved"
    
    def test_security_context_retrieval(self):
        """Test retrieval of security-related context."""
        state = {
            "ticket_id": "TEST-003",
            "subject": "Account security",
            "description": "Suspicious activity on my account",
            "category": "Security"
        }
        
        result = retrieve_context(state)
        
        assert "context" in result
        assert len(result["context"]) > 0
        assert result["processing_step"] == "context_retrieved"
    
    def test_general_context_retrieval(self):
        """Test retrieval of general context."""
        state = {
            "ticket_id": "TEST-004",
            "subject": "General question",
            "description": "How do I use your service?",
            "category": "General"
        }
        
        result = retrieve_context(state)
        
        assert "context" in result
        assert len(result["context"]) > 0
        assert result["processing_step"] == "context_retrieved"
    
    def test_context_with_reviewer_feedback(self):
        """Test context retrieval with reviewer feedback for retry."""
        state = {
            "ticket_id": "TEST-005",
            "subject": "Billing issue",
            "description": "Problem with my bill",
            "category": "Billing",
            "reviewer_feedback": "Need more specific information about refund policies"
        }
        
        result = retrieve_context(state)
        
        assert "context" in result
        assert len(result["context"]) > 0
        assert result["processing_step"] == "context_retrieved"

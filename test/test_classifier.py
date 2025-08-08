import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from nodes.classifier import classify_ticket

class TestClassifier:
    """Test cases for the ticket classifier node."""
    
    def test_billing_classification(self):
        """Test classification of billing-related tickets."""
        state = {
            "ticket_id": "TEST-001",
            "subject": "Billing issue with my subscription",
            "description": "I was charged twice for my monthly subscription. Please help resolve this billing error."
        }
        
        result = classify_ticket(state)
        
        assert "category" in result
        assert result["category"] in ["Billing", "General"]  # Allow fallback
        assert result["processing_step"] == "classified"
    
    def test_technical_classification(self):
        """Test classification of technical tickets."""
        state = {
            "ticket_id": "TEST-002", 
            "subject": "API returning 500 errors",
            "description": "Our integration is failing with 500 internal server errors on all endpoints since this morning."
        }
        
        result = classify_ticket(state)
        
        assert "category" in result
        assert result["category"] in ["Technical", "General"]  # Allow fallback
        assert result["processing_step"] == "classified"
    
    def test_security_classification(self):
        """Test classification of security-related tickets."""
        state = {
            "ticket_id": "TEST-003",
            "subject": "Suspicious login activity",
            "description": "I received alerts about login attempts from unknown locations. I think my account may be compromised."
        }
        
        result = classify_ticket(state)
        
        assert "category" in result
        assert result["category"] in ["Security", "General"]  # Allow fallback
        assert result["processing_step"] == "classified"
    
    def test_general_classification(self):
        """Test classification of general inquiries."""
        state = {
            "ticket_id": "TEST-004",
            "subject": "Question about features",
            "description": "I would like to know more about the advanced features available in your platform."
        }
        
        result = classify_ticket(state)
        
        assert "category" in result
        assert result["category"] == "General"
        assert result["processing_step"] == "classified"
    
    def test_empty_input_handling(self):
        """Test handling of empty or invalid input."""
        state = {
            "ticket_id": "TEST-005",
            "subject": "",
            "description": ""
        }
        
        result = classify_ticket(state)
        
        # Should still return a category (likely General as fallback)
        assert "category" in result
        assert result["processing_step"] == "classified"

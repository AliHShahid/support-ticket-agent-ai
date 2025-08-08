import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from nodes.draft_generator import generate_draft

class TestDraftGenerator:
    """Test cases for the draft generator node."""
    
    def test_basic_draft_generation(self):
        """Test basic draft response generation."""
        state = {
            "ticket_id": "TEST-001",
            "subject": "Login problem",
            "description": "Cannot log into my account",
            "category": "Technical",
            "context": "Login issues can be resolved by resetting password or clearing browser cache.",
            "attempt_count": 0
        }
        
        result = generate_draft(state)
        
        assert "draft_response" in result
        assert len(result["draft_response"]) > 0
        assert result["processing_step"] == "draft_generated"
        assert result["attempt_count"] == 1
    
    def test_draft_with_reviewer_feedback(self):
        """Test draft generation with reviewer feedback for retry."""
        state = {
            "ticket_id": "TEST-002",
            "subject": "Billing question",
            "description": "Question about my bill",
            "category": "Billing",
            "context": "Billing information and policies",
            "attempt_count": 1,
            "reviewer_feedback": "Response needs to be more specific about billing policies"
        }
        
        result = generate_draft(state)
        
        assert "draft_response" in result
        assert len(result["draft_response"]) > 0
        assert result["processing_step"] == "draft_generated"
        assert result["attempt_count"] == 2
    
    def test_multiple_attempts(self):
        """Test draft generation tracking attempt count."""
        state = {
            "ticket_id": "TEST-003",
            "subject": "Test ticket",
            "description": "Test description",
            "category": "General",
            "context": "General support information",
            "attempt_count": 1
        }
        
        result = generate_draft(state)
        
        assert result["attempt_count"] == 2
        assert "draft_response" in result
    
    def test_error_handling(self):
        """Test draft generation error handling."""
        state = {
            "ticket_id": "TEST-004",
            "subject": "",  # Empty subject to potentially cause issues
            "description": "",  # Empty description
            "category": "General",
            "context": "",
            "attempt_count": 0
        }
        
        result = generate_draft(state)
        
        # Should still generate some response even with minimal input
        assert "draft_response" in result
        assert result["attempt_count"] == 1
        assert result["processing_step"] == "draft_generated"

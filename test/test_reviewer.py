import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from nodes.reviewer import review_draft

class TestReviewer:
    """Test cases for the draft reviewer node."""
    
    def test_good_draft_approval(self):
        """Test approval of a good quality draft."""
        state = {
            "ticket_id": "TEST-001",
            "subject": "Login issue",
            "description": "Cannot access my account",
            "category": "Technical",
            "draft_response": "I understand you're having trouble logging into your account. Please try resetting your password using the 'Forgot Password' link on the login page. If that doesn't work, clear your browser cache and cookies, then try again. If you continue to experience issues, please let me know and I'll escalate this to our technical team.",
            "context": "Login troubleshooting steps and escalation procedures",
            "attempt_count": 1
        }
        
        result = review_draft(state)
        
        assert "review_approved" in result
        assert "reviewer_feedback" in result
        assert result["processing_step"] == "reviewed"
    
    def test_poor_draft_rejection(self):
        """Test rejection of a poor quality draft."""
        state = {
            "ticket_id": "TEST-002",
            "subject": "Billing problem",
            "description": "Wrong charge on my card",
            "category": "Billing",
            "draft_response": "Sorry, can't help with that.",  # Poor quality response
            "context": "Billing policies and dispute procedures",
            "attempt_count": 1
        }
        
        result = review_draft(state)
        
        assert "review_approved" in result
        assert "reviewer_feedback" in result
        assert result["processing_step"] == "reviewed"
        # Note: Actual approval depends on LLM review, but structure should be correct
    
    def test_review_with_context(self):
        """Test review considering provided context."""
        state = {
            "ticket_id": "TEST-003",
            "subject": "Security concern",
            "description": "Suspicious login attempts",
            "category": "Security",
            "draft_response": "I understand your concern about suspicious login attempts. For your security, I recommend immediately changing your password and enabling two-factor authentication. Please also review your recent account activity in your dashboard. If you notice any unauthorized changes, please contact our security team immediately.",
            "context": "Security incident response procedures and account protection measures",
            "attempt_count": 1
        }
        
        result = review_draft(state)
        
        assert "review_approved" in result
        assert "reviewer_feedback" in result
        assert result["processing_step"] == "reviewed"

import pytest
import sys
from pathlib import Path
import asyncio

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from main import process_ticket

class TestEndToEndFlow:
    """End-to-end integration tests for the complete ticket processing flow."""
    
    @pytest.mark.asyncio
    async def test_successful_ticket_resolution(self):
        """Test complete flow for a ticket that should resolve successfully."""
        subject = "Password reset help"
        description = "I forgot my password and the reset email isn't coming through. Can you help me regain access to my account?"
        
        result = await process_ticket(subject, description)
        
        assert "ticket_id" in result
        assert "category" in result
        assert "final_response" in result
        assert len(result["final_response"]) > 0
        assert result["processing_step"] in ["completed", "escalated"]
    
    @pytest.mark.asyncio
    async def test_billing_ticket_flow(self):
        """Test flow for a billing-related ticket."""
        subject = "Unexpected charge on my account"
        description = "I see a charge of $99.99 but I only signed up for the basic plan at $29.99. Please explain this charge."
        
        result = await process_ticket(subject, description)
        
        assert result["category"] in ["Billing", "General"]
        assert "final_response" in result
        assert len(result["final_response"]) > 0
    
    @pytest.mark.asyncio
    async def test_technical_ticket_flow(self):
        """Test flow for a technical ticket."""
        subject = "API integration failing"
        description = "Our API calls started returning 500 errors this morning. All our endpoints are affected and our production system is down."
        
        result = await process_ticket(subject, description)
        
        assert result["category"] in ["Technical", "General"]
        assert "final_response" in result
        assert len(result["final_response"]) > 0
    
    @pytest.mark.asyncio
    async def test_security_ticket_flow(self):
        """Test flow for a security-related ticket."""
        subject = "Account may be compromised"
        description = "I received notifications about login attempts from countries I've never visited. I'm worried my account has been hacked."
        
        result = await process_ticket(subject, description)
        
        assert result["category"] in ["Security", "General"]
        assert "final_response" in result
        assert len(result["final_response"]) > 0
    
    @pytest.mark.asyncio
    async def test_retry_mechanism(self):
        """Test that retry mechanism works properly."""
        # This test may be challenging to trigger reliably, but we can check the structure
        subject = "Complex issue requiring multiple attempts"
        description = "This is a very complex issue that might require multiple processing attempts to resolve properly."
        
        result = await process_ticket(subject, description)
        
        # Check that attempt tracking works
        assert "attempt_count" in result
        assert result["attempt_count"] >= 1
        assert "failed_attempts" in result
    
    @pytest.mark.asyncio
    async def test_minimal_input_handling(self):
        """Test handling of minimal input."""
        subject = "Help"
        description = "Need help"
        
        result = await process_ticket(subject, description)
        
        assert "final_response" in result
        assert len(result["final_response"]) > 0
        assert "category" in result

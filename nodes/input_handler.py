from typing import Dict, Any
from utils.logger import setup_logger
from utils.helpers import create_ticket_id

logger = setup_logger("input_handler")

def process_input(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process and validate input ticket data.
    
    Args:
        state: Graph state containing ticket information
        
    Returns:
        Updated state with processed input
    """
    
    # Extract input data
    subject = state.get("subject", "").strip()
    description = state.get("description", "").strip()
    
    # Validate input
    if not subject or not description:
        raise ValueError("Both subject and description are required")
    
    # Generate ticket ID if not present
    ticket_id = state.get("ticket_id") or create_ticket_id()
    
    # Log input processing
    logger.info(f"Processing ticket {ticket_id}: {subject[:50]}...")
    
    # Update state
    updated_state = {
        **state,
        "ticket_id": ticket_id,
        "subject": subject,
        "description": description,
        "processing_step": "input_processed",
        "attempt_count": 0,
        "failed_attempts": []
    }
    
    return updated_state

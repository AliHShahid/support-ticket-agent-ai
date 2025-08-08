from typing import Dict, Any
from utils.logger import setup_logger
from utils.helpers import load_config

logger = setup_logger("retry_logic")

def should_retry(state: Dict[str, Any]) -> str:
    """
    Determine if the system should retry or escalate based on attempt count and review result.
    
    Args:
        state: Graph state containing review results and attempt count
        
    Returns:
        Next step: "retry", "escalate", or "finalize"
    """
    
    config = load_config()
    ticket_id = state.get("ticket_id")
    review_approved = state.get("review_approved", False)
    attempt_count = state.get("attempt_count", 0)
    max_attempts = config["retry"]["max_attempts"]
    
    logger.info(f"Evaluating retry logic for ticket {ticket_id} - Attempt: {attempt_count}, Approved: {review_approved}")
    
    # If approved, finalize
    if review_approved:
        logger.info(f"Ticket {ticket_id} approved, finalizing response")
        return "finalize"
    
    # If not approved and under max attempts, retry
    if attempt_count < max_attempts:
        logger.info(f"Ticket {ticket_id} rejected, retrying (attempt {attempt_count + 1}/{max_attempts})")
        return "retry"
    
    # If max attempts reached, escalate
    logger.info(f"Ticket {ticket_id} reached max attempts ({max_attempts}), escalating")
    return "escalate"

def update_retry_state(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update state for retry attempt.
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state for retry
    """
    
    ticket_id = state.get("ticket_id")
    attempt_count = state.get("attempt_count", 0)
    draft_response = state.get("draft_response", "")
    reviewer_feedback = state.get("reviewer_feedback", "")
    failed_attempts = state.get("failed_attempts", [])
    
    # Record failed attempt
    failed_attempt = {
        "attempt": attempt_count,
        "draft": draft_response,
        "feedback": reviewer_feedback
    }
    failed_attempts.append(failed_attempt)
    
    logger.info(f"Recording failed attempt {attempt_count} for ticket {ticket_id}")
    
    # Update state for retry
    updated_state = {
        **state,
        "failed_attempts": failed_attempts,
        "processing_step": "retrying"
    }
    
    return updated_state

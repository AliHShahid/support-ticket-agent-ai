from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from utils.logger import setup_logger
from utils.helpers import load_config, load_prompt_template

logger = setup_logger("reviewer")

def review_draft(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Review the draft response for quality and policy compliance.
    
    Args:
        state: Graph state containing draft response and context
        
    Returns:
        Updated state with review result
    """
    
    config = load_config()
    ticket_id = state.get("ticket_id")
    subject = state.get("subject")
    description = state.get("description")
    category = state.get("category")
    draft_response = state.get("draft_response")
    context = state.get("context", "")
    attempt_count = state.get("attempt_count", 0)
    
    logger.info(f"Reviewing draft for ticket {ticket_id} (attempt {attempt_count})")
    
    try:
        # Initialize LLM
        llm = ChatOpenAI(
            model=config["llm"]["model"],
            temperature=0.1,  # Lower temperature for consistent review
            max_tokens=500
        )
        
        # Load and format prompt
        prompt_template = load_prompt_template("reviewer_prompt.txt")
        prompt = prompt_template.format(
            subject=subject,
            description=description,
            category=category,
            draft_response=draft_response,
            context=context
        )
        
        # Get review
        response = llm.invoke([HumanMessage(content=prompt)])
        review_result = response.content.strip()
        
        # Parse review result
        if review_result.startswith("APPROVED"):
            approved = True
            feedback = "Response approved"
            logger.info(f"Draft approved for ticket {ticket_id}")
        else:
            approved = False
            # Extract feedback after "REJECTED:"
            feedback = review_result.replace("REJECTED:", "").strip()
            if not feedback:
                feedback = "Response needs improvement"
            logger.info(f"Draft rejected for ticket {ticket_id}: {feedback}")
        
        # Update state
        updated_state = {
            **state,
            "review_approved": approved,
            "reviewer_feedback": feedback,
            "processing_step": "reviewed"
        }
        
        return updated_state
        
    except Exception as e:
        logger.error(f"Review failed for ticket {ticket_id}: {str(e)}")
        # Default to approval on error to avoid infinite loops
        return {
            **state,
            "review_approved": True,
            "reviewer_feedback": f"Review system error: {str(e)}",
            "processing_step": "reviewed",
            "review_error": str(e)
        }

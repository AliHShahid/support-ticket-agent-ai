from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from utils.logger import setup_logger
from utils.helpers import load_config, load_prompt_template

logger = setup_logger("draft_generator")

def generate_draft(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a draft response based on ticket and context.
    
    Args:
        state: Graph state containing ticket, category, and context
        
    Returns:
        Updated state with draft response
    """
    
    config = load_config()
    ticket_id = state.get("ticket_id")
    subject = state.get("subject")
    description = state.get("description")
    category = state.get("category")
    context = state.get("context", "")
    attempt_count = state.get("attempt_count", 0)
    reviewer_feedback = state.get("reviewer_feedback", "")
    
    logger.info(f"Generating draft for ticket {ticket_id} (attempt {attempt_count + 1})")
    
    try:
        # Initialize LLM
        llm = ChatOpenAI(
            model=config["llm"]["model"],
            temperature=config["llm"]["temperature"],
            max_tokens=config["llm"]["max_tokens"]
        )
        
        # Load and format prompt
        prompt_template = load_prompt_template("generator_prompt.txt")
        
        # Add reviewer feedback if this is a retry
        enhanced_context = context
        if reviewer_feedback:
            enhanced_context += f"\n\nPrevious Reviewer Feedback: {reviewer_feedback}"
        
        prompt = prompt_template.format(
            subject=subject,
            description=description,
            category=category,
            context=enhanced_context
        )
        
        # Generate draft
        response = llm.invoke([HumanMessage(content=prompt)])
        draft_response = response.content.strip()
        
        logger.info(f"Draft generated for ticket {ticket_id} (length: {len(draft_response)} chars)")
        
        # Update state
        updated_state = {
            **state,
            "draft_response": draft_response,
            "processing_step": "draft_generated",
            "attempt_count": attempt_count + 1
        }
        
        return updated_state
        
    except Exception as e:
        logger.error(f"Draft generation failed for ticket {ticket_id}: {str(e)}")
        return {
            **state,
            "draft_response": f"I apologize, but I'm experiencing technical difficulties generating a response. Please contact our support team directly for assistance with your {category.lower()} inquiry.",
            "processing_step": "draft_generated",
            "attempt_count": attempt_count + 1,
            "generation_error": str(e)
        }

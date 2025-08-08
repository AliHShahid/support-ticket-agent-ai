from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from utils.logger import setup_logger
from utils.helpers import load_config, load_prompt_template, save_to_escalation_log

logger = setup_logger("escalator")

def escalate_ticket(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Escalate ticket to human agents and log to CSV.
    
    Args:
        state: Graph state containing failed ticket information
        
    Returns:
        Updated state with escalation message
    """
    
    config = load_config()
    ticket_id = state.get("ticket_id")
    subject = state.get("subject")
    description = state.get("description")
    category = state.get("category")
    failed_attempts = state.get("failed_attempts", [])
    attempt_count = state.get("attempt_count", 0)
    reviewer_feedback = state.get("reviewer_feedback", "")
    
    logger.info(f"Escalating ticket {ticket_id} after {attempt_count} failed attempts")
    
    try:
        # Initialize LLM for escalation message
        llm = ChatOpenAI(
            model=config["llm"]["model"],
            temperature=config["llm"]["temperature"],
            max_tokens=config["llm"]["max_tokens"]
        )
        
        # Prepare failed attempts summary
        attempts_summary = []
        for i, attempt in enumerate(failed_attempts, 1):
            attempts_summary.append(f"Attempt {i}: {attempt['feedback']}")
        
        attempts_text = "\n".join(attempts_summary)
        
        # Load and format escalation prompt
        prompt_template = load_prompt_template("escalation_prompt.txt")
        prompt = prompt_template.format(
            attempts=attempt_count,
            subject=subject,
            description=description,
            category=category,
            failed_attempts=attempts_text,
            reviewer_feedback=reviewer_feedback
        )
        
        # Generate escalation message
        response = llm.invoke([HumanMessage(content=prompt)])
        escalation_message = response.content.strip()
        
        # Prepare escalation data
        escalation_data = {
            "ticket_id": ticket_id,
            "subject": subject,
            "description": description,
            "category": category,
            "failed_attempts": attempt_count,
            "final_error": reviewer_feedback,
            "escalation_message": escalation_message
        }
        
        # Save to escalation log
        log_file = config["escalation"]["log_file"]
        save_to_escalation_log(escalation_data, log_file)
        
        logger.info(f"Ticket {ticket_id} escalated and logged to {log_file}")
        
        # Update state
        updated_state = {
            **state,
            "escalation_message": escalation_message,
            "escalated": True,
            "processing_step": "escalated",
            "final_response": f"This ticket has been escalated to our human support team. Reference ID: {ticket_id}"
        }
        
        return updated_state
        
    except Exception as e:
        logger.error(f"Escalation failed for ticket {ticket_id}: {str(e)}")
        
        # Fallback escalation
        fallback_message = f"Ticket {ticket_id} requires human attention due to automated processing failure."
        
        return {
            **state,
            "escalation_message": fallback_message,
            "escalated": True,
            "processing_step": "escalated",
            "final_response": f"This ticket has been escalated to our human support team. Reference ID: {ticket_id}",
            "escalation_error": str(e)
        }

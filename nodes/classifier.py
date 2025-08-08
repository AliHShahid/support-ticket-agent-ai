from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from utils.logger import setup_logger
from utils.helpers import load_config, load_prompt_template

logger = setup_logger("classifier")

def classify_ticket(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Classify the support ticket into predefined categories.
    
    Args:
        state: Graph state containing ticket information
        
    Returns:
        Updated state with classification result
    """
    
    config = load_config()
    ticket_id = state.get("ticket_id")
    subject = state.get("subject")
    description = state.get("description")
    
    logger.info(f"Classifying ticket {ticket_id}")
    
    try:
        # Initialize LLM
        llm = ChatOpenAI(
            model=config["llm"]["model"],
            temperature=config["llm"]["temperature"],
            max_tokens=100  # Short response for classification
        )
        
        # Load and format prompt
        prompt_template = load_prompt_template("classifier_prompt.txt")
        prompt = prompt_template.format(
            subject=subject,
            description=description
        )
        
        # Get classification
        response = llm.invoke([HumanMessage(content=prompt)])
        category = response.content.strip()
        
        # Validate category
        valid_categories = config["categories"]
        if category not in valid_categories:
            logger.warning(f"Invalid category '{category}' for ticket {ticket_id}, defaulting to 'General'")
            category = "General"
        
        logger.info(f"Ticket {ticket_id} classified as: {category}")
        
        # Update state
        updated_state = {
            **state,
            "category": category,
            "processing_step": "classified"
        }
        
        return updated_state
        
    except Exception as e:
        logger.error(f"Classification failed for ticket {ticket_id}: {str(e)}")
        # Default to General category on error
        return {
            **state,
            "category": "General",
            "processing_step": "classified",
            "classification_error": str(e)
        }

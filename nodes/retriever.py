from typing import Dict, Any, List
from utils.logger import setup_logger
from utils.helpers import load_knowledge_base

logger = setup_logger("retriever")

def retrieve_context(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retrieve relevant context based on ticket category and content.
    
    Args:
        state: Graph state containing ticket and classification info
        
    Returns:
        Updated state with retrieved context
    """
    
    ticket_id = state.get("ticket_id")
    category = state.get("category")
    subject = state.get("subject")
    description = state.get("description")
    reviewer_feedback = state.get("reviewer_feedback", "")
    
    logger.info(f"Retrieving context for ticket {ticket_id} in category: {category}")
    
    try:
        # Load knowledge base for the category
        documents = load_knowledge_base(category)
        
        # Simple retrieval logic - in production, this would use vector similarity
        relevant_docs = []
        
        # Combine search terms
        search_terms = f"{subject} {description} {reviewer_feedback}".lower()
        
        # Score documents based on keyword overlap
        for doc in documents:
            doc_lower = doc.lower()
            score = 0
            
            # Simple keyword matching
            for word in search_terms.split():
                if len(word) > 3 and word in doc_lower:
                    score += 1
            
            if score > 0:
                relevant_docs.append((doc, score))
        
        # Sort by relevance and take top documents
        relevant_docs.sort(key=lambda x: x[1], reverse=True)
        context_docs = [doc for doc, _ in relevant_docs[:3]]
        
        # If no relevant docs found, use first few documents
        if not context_docs:
            context_docs = documents[:2]
        
        context = "\n\n".join(context_docs)
        
        logger.info(f"Retrieved {len(context_docs)} relevant documents for ticket {ticket_id}")
        
        # Update state
        updated_state = {
            **state,
            "context": context,
            "context_docs": context_docs,
            "processing_step": "context_retrieved"
        }
        
        return updated_state
        
    except Exception as e:
        logger.error(f"Context retrieval failed for ticket {ticket_id}: {str(e)}")
        return {
            **state,
            "context": f"Error retrieving context for {category} category. Using general guidance.",
            "context_docs": [],
            "processing_step": "context_retrieved",
            "retrieval_error": str(e)
        }

from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

# Import node functions
from nodes.input_handler import process_input
from nodes.classifier import classify_ticket
from nodes.retriever import retrieve_context
from nodes.draft_generator import generate_draft
from nodes.reviewer import review_draft
from nodes.retry_logic import should_retry, update_retry_state
from nodes.escalator import escalate_ticket

from utils.logger import setup_logger

logger = setup_logger("graph")

class SupportTicketState(TypedDict):
    """State schema for the support ticket resolution graph."""
    
    # Input fields
    ticket_id: str
    subject: str
    description: str
    
    # Processing fields
    category: str
    context: str
    context_docs: list
    draft_response: str
    review_approved: bool
    reviewer_feedback: str
    
    # Control fields
    processing_step: str
    attempt_count: int
    failed_attempts: list
    escalated: bool
    escalation_message: str
    final_response: str
    
    # Error tracking
    classification_error: str
    retrieval_error: str
    generation_error: str
    review_error: str
    escalation_error: str

def create_support_agent_graph() -> CompiledStateGraph:
    """
    Create and compile the support ticket resolution graph.
    
    Returns:
        Compiled LangGraph state graph
    """
    
    logger.info("Creating support agent graph")
    
    # Create the graph
    workflow = StateGraph(SupportTicketState)
    
    # Add nodes
    workflow.add_node("input_handler", process_input)
    workflow.add_node("classifier", classify_ticket)
    workflow.add_node("retriever", retrieve_context)
    workflow.add_node("draft_generator", generate_draft)
    workflow.add_node("reviewer", review_draft)
    workflow.add_node("retry_updater", update_retry_state)
    workflow.add_node("escalator", escalate_ticket)
    
    # Set entry point
    workflow.set_entry_point("input_handler")
    
    # Add edges
    workflow.add_edge("input_handler", "classifier")
    workflow.add_edge("classifier", "retriever")
    workflow.add_edge("retriever", "draft_generator")
    workflow.add_edge("draft_generator", "reviewer")
    
    # Add conditional edge for retry logic
    def route_after_review(state: SupportTicketState) -> Literal["finalize", "retry_updater", "escalator"]:
        """Route based on review result and attempt count."""
        decision = should_retry(state)
        logger.info(f"Routing decision for ticket {state.get('ticket_id')}: {decision}")
        
        if decision == "finalize":
            return "finalize"
        elif decision == "retry":
            return "retry_updater"
        else:  # escalate
            return "escalator"
    
    workflow.add_conditional_edges(
        "reviewer",
        route_after_review,
        {
            "finalize": END,
            "retry_updater": "retry_updater",
            "escalator": "escalator"
        }
    )
    
    # Add retry loop edges
    workflow.add_edge("retry_updater", "retriever")  # Go back to retrieval with feedback
    workflow.add_edge("escalator", END)
    
    # Compile the graph
    compiled_graph = workflow.compile()
    
    logger.info("Support agent graph compiled successfully")
    
    return compiled_graph

def finalize_response(state: SupportTicketState) -> Dict[str, Any]:
    """
    Finalize the response when approved.
    
    Args:
        state: Final state with approved response
        
    Returns:
        Updated state with final response
    """
    
    ticket_id = state.get("ticket_id")
    draft_response = state.get("draft_response")
    
    logger.info(f"Finalizing response for ticket {ticket_id}")
    
    return {
        **state,
        "final_response": draft_response,
        "processing_step": "completed"
    }

# Create the main graph instance
support_agent_graph = create_support_agent_graph()

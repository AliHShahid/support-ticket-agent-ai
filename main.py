#!/usr/bin/env python3
"""
Support Ticket Resolution Agent
Main entry point for the LangGraph-based support agent.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any
import asyncio
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from langgraph_graph.graph import support_agent_graph, SupportTicketState
from utils.logger import setup_logger
from utils.helpers import load_config

# Load environment variables
load_dotenv()

logger = setup_logger("main")

def validate_environment():
    """Validate required environment variables."""
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        sys.exit(1)

async def process_ticket(subject: str, description: str) -> Dict[str, Any]:
    """
    Process a support ticket through the LangGraph agent.
    
    Args:
        subject: Ticket subject line
        description: Detailed ticket description
        
    Returns:
        Final processing result
    """
    
    logger.info(f"Processing new ticket: {subject[:50]}...")
    
    # Create initial state
    initial_state: SupportTicketState = {
        "subject": subject,
        "description": description,
        "ticket_id": "",
        "category": "",
        "context": "",
        "context_docs": [],
        "draft_response": "",
        "review_approved": False,
        "reviewer_feedback": "",
        "processing_step": "initialized",
        "attempt_count": 0,
        "failed_attempts": [],
        "escalated": False,
        "escalation_message": "",
        "final_response": "",
        "classification_error": "",
        "retrieval_error": "",
        "generation_error": "",
        "review_error": "",
        "escalation_error": ""
    }
    
    try:
        # Run the graph
        result = await support_agent_graph.ainvoke(initial_state)
        
        ticket_id = result.get("ticket_id", "unknown")
        final_response = result.get("final_response", "")
        escalated = result.get("escalated", False)
        
        if escalated:
            logger.info(f"Ticket {ticket_id} was escalated to human agents")
        else:
            logger.info(f"Ticket {ticket_id} resolved successfully")
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing ticket: {str(e)}")
        return {
            **initial_state,
            "final_response": "An error occurred while processing your ticket. Please contact support directly.",
            "processing_step": "error",
            "escalation_error": str(e)
        }

def run_interactive_demo():
    """Run an interactive demo of the support agent."""
    
    print("\n" + "="*60)
    print("🎫 SUPPORT TICKET RESOLUTION AGENT")
    print("="*60)
    print("Enter ticket details to see the agent in action!")
    print("Type 'quit' to exit.\n")
    
    while True:
        try:
            # Get ticket input
            print("\n" + "-"*40)
            subject = input("📝 Ticket Subject: ").strip()
            
            if subject.lower() == 'quit':
                break
                
            if not subject:
                print("❌ Subject cannot be empty!")
                continue
            
            description = input("📄 Ticket Description: ").strip()
            
            if not description:
                print("❌ Description cannot be empty!")
                continue
            
            print(f"\n🔄 Processing ticket...")
            print("-"*40)
            
            # Process the ticket
            result = asyncio.run(process_ticket(subject, description))
            
            # Display results
            print(f"\n✅ PROCESSING COMPLETE")
            print(f"🆔 Ticket ID: {result.get('ticket_id', 'N/A')}")
            print(f"📂 Category: {result.get('category', 'N/A')}")
            print(f"🔄 Attempts: {result.get('attempt_count', 0)}")
            print(f"📊 Status: {'ESCALATED' if result.get('escalated') else 'RESOLVED'}")
            
            print(f"\n💬 FINAL RESPONSE:")
            print("-"*40)
            print(result.get('final_response', 'No response generated'))
            
            if result.get('escalated'):
                print(f"\n⚠️  ESCALATION MESSAGE:")
                print("-"*40)
                print(result.get('escalation_message', 'No escalation message'))
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

def run_sample_tickets():
    """Run predefined sample tickets for demonstration."""
    
    sample_tickets = [
        {
            "subject": "Cannot login to my account",
            "description": "I've been trying to log into my account for the past hour but keep getting an 'invalid credentials' error. I'm sure my password is correct. This started happening after I changed my email address yesterday."
        },
        {
            "subject": "Billing charge dispute",
            "description": "I was charged $99.99 on my credit card but I only signed up for the $29.99 plan. I need this resolved immediately as this is affecting my budget."
        },
        {
            "subject": "API integration not working",
            "description": "Our API integration stopped working this morning. We're getting 500 errors on all endpoints. This is affecting our production system and we need urgent help."
        },
        {
            "subject": "Suspicious login activity",
            "description": "I received an email about login attempts from Russia, but I'm in the US and haven't traveled. I'm concerned my account may be compromised. Please help secure my account."
        }
    ]
    
    print("\n" + "="*60)
    print("🎫 RUNNING SAMPLE TICKETS")
    print("="*60)
    
    for i, ticket in enumerate(sample_tickets, 1):
        print(f"\n📋 SAMPLE TICKET {i}/4")
        print(f"Subject: {ticket['subject']}")
        print(f"Description: {ticket['description'][:100]}...")
        print("-"*40)
        
        result = asyncio.run(process_ticket(ticket['subject'], ticket['description']))
        
        print(f"✅ Result: {'ESCALATED' if result.get('escalated') else 'RESOLVED'}")
        print(f"📂 Category: {result.get('category', 'N/A')}")
        print(f"🔄 Attempts: {result.get('attempt_count', 0)}")
        
        if not result.get('escalated'):
            response = result.get('final_response', '')[:200]
            print(f"💬 Response: {response}...")
        
        print("-"*40)

def main():
    """Main entry point."""
    
    # Validate environment
    validate_environment()
    
    # Load configuration
    try:
        config = load_config()
        logger.info("Configuration loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load configuration: {str(e)}")
        sys.exit(1)
    
    # Create necessary directories
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("embeddings", exist_ok=True)
    
    print("🚀 Support Ticket Resolution Agent")
    print("Choose an option:")
    print("1. Interactive Demo")
    print("2. Run Sample Tickets")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            run_interactive_demo()
            break
        elif choice == "2":
            run_sample_tickets()
            break
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()

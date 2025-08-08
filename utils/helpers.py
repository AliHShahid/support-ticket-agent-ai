import yaml
import csv
import os
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd
from datetime import datetime

def load_config(config_path: str = "config/settings.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def load_prompt_template(prompt_name: str) -> str:
    """Load prompt template from file."""
    prompt_path = Path(f"prompts/{prompt_name}")
    with open(prompt_path, 'r') as file:
        return file.read().strip()

def save_to_escalation_log(ticket_data: Dict[str, Any], log_file: str = "data/escalation_log.csv"):
    """Save failed ticket to escalation log."""
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Prepare row data
    row_data = {
        'timestamp': datetime.now().isoformat(),
        'ticket_id': ticket_data.get('ticket_id', 'unknown'),
        'subject': ticket_data.get('subject', ''),
        'description': ticket_data.get('description', ''),
        'category': ticket_data.get('category', ''),
        'failed_attempts': ticket_data.get('failed_attempts', 0),
        'final_error': ticket_data.get('final_error', ''),
        'escalation_message': ticket_data.get('escalation_message', '')
    }
    
    # Check if file exists to determine if we need headers
    file_exists = os.path.exists(log_file)
    
    # Write to CSV
    with open(log_file, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = list(row_data.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(row_data)

def load_knowledge_base(category: str) -> List[str]:
    """Load knowledge base documents for a specific category."""
    kb_path = Path(f"data/knowledge_base/{category.lower()}_docs")
    
    if not kb_path.exists():
        return [f"No specific knowledge base found for {category} category."]
    
    documents = []
    for file_path in kb_path.glob("*.txt"):
        with open(file_path, 'r', encoding='utf-8') as file:
            documents.append(file.read().strip())
    
    return documents if documents else [f"No documents found in {category} knowledge base."]

def create_ticket_id() -> str:
    """Generate a unique ticket ID."""
    return f"TKT-{datetime.now().strftime('%Y%m%d%H%M%S')}"

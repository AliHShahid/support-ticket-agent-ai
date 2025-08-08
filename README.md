# Support Ticket Resolution Agent

AI-powered support ticket resolution system built with LangGraph that automatically classifies, processes, and responds to customer support tickets with multi-step review loops and escalation handling.

## Architecture Overview

This system implements a graph-based workflow that mirrors real-world support operations:

## Quick Start

### Prerequisites

- Python 3.12.0+
- OpenAI API key

### Installation Guidelines 
This project is built using Windows 10

1. **Create virtual environment:**
   \`\`\`bash
   python -m venv venv
   \`\`\`
   \`\`\`bash
   venv\\Scripts\\activate  # Windows
   \`\`\`

2. **Install dependencies:**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Configure environment:**
   Edit .env with your API keys

4. **Run the agent:**
   \`\`\`bash
   python main.py
   \`\`\`

## Core Features

### 1. Intelligent Classification
- Automatically categorizes tickets into: Billing, Technical, Security, General
- Uses LLM-based classification with fallback handling
- Robust error handling and default categorization

### 2. Context-Aware RAG Retrieval
- Category-specific knowledge base retrieval
- Keyword-based document scoring and ranking
- Feedback-driven context refinement for retries

### 3. Multi-Step Review Process
- LLM-based quality assurance and policy compliance checking
- Detailed feedback generation for improvement
- Configurable review criteria and standards

### 4. Intelligent Retry Logic
- Maximum 2 retry attempts with feedback incorporation
- Context refinement based on reviewer feedback
- Automatic escalation after max attempts

### 5. Escalation Management
- Automatic escalation to human agents
- Comprehensive escalation logging to CSV
- Detailed failure analysis and recommendations

## Testing

Run the test suite:
\`\`\`bash
python -m pytest test/ -v
\`\`\`

Individual component tests:
\`\`\`bash
python -m pytest test/test_classifier.py -v
python -m pytest test/test_retriever.py -v
python -m pytest test/test_generator.py -v
\`\`\`

## Monitoring and Logging

### Log Files
- Application logs: \`logs/support_agent_YYYYMMDD.log\`
- Escalation tracking: \`data/escalation_log.csv\`

### Key Metrics
- Processing success rate
- Average attempts per ticket
- Escalation rate by category
- Response quality scores

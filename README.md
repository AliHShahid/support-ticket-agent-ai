# Support Ticket Resolution Agent

AI-powered support ticket resolution system built with LangGraph that automatically classifies, processes, and responds to customer support tickets with multi-step review loops and escalation handling.

# Demo Link
https://drive.google.com/file/d/15-C_yO3R8YMJt-PAhXDY4PSQBGpaSGxP/view?usp=drive_link 

## Architecture Overview

This system implements a graph-based workflow that mirrors real-world support operations:

## Quick Start

### Prerequisites

- Python 3.12.0+
- OpenAI API key

### Installation Guidelines 
This project is built using Windows 10

Step 1: Create a Virtual Environment

python -m venv venv
Activate it:
# Windows
venv\Scripts\activate

Step 2: Install Dependencies

pip install -r requirements.txt

Step 3: Configure Environment Variables
Create a .env file in the project root with the following:

- OPENAI_API_KEY=your_openai_api_key
- LANGCHAIN_API_KEY=your_langchain_api_key
- LANGCHAIN_TRACING_V2=true
- LANGCHAIN_PROJECT=support-ticket-agent
You can get these keys from:

OpenAI Platform

LangSmith / LangChain

Step 4: Run the Agent

python main.py
You’ll see a CLI interface:

Support Ticket Resolution Agent
Choose an option:
1. Interactive Demo
2. Run Sample Tickets
3. Exit

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

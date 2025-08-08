# Support Ticket Resolution Agent

A sophisticated AI-powered support ticket resolution system built with LangGraph that automatically classifies, processes, and responds to customer support tickets with multi-step review loops and escalation handling.

## 🏗️ Architecture Overview

This system implements a graph-based workflow that mirrors real-world support operations:

\`\`\`
Input Ticket → Classification → RAG Retrieval → Draft Generation → Review → 
    ↓                                                                    ↓
Final Response ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
    ↓                                                                    ↓
Escalation (if max retries exceeded) ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← Retry Loop
\`\`\`

## 📁 Project Structure

\`\`\`
support-ticket-agent/
├── data/                               # 🔍 RAG knowledge base and escalation log
│   ├── knowledge_base/
│   │   ├── billing_docs/
│   │   ├── technical_docs/
│   │   ├── security_docs/
│   │   └── general_docs/
│   └── escalation_log.csv              # Escalation tracking
├── embeddings/                         # Vector store directory
├── nodes/                              # Core LangGraph nodes
│   ├── input_handler.py                # Input preprocessing
│   ├── classifier.py                   # Ticket classification
│   ├── retriever.py                    # RAG context retrieval
│   ├── draft_generator.py              # Response generation
│   ├── reviewer.py                     # Quality review
│   ├── retry_logic.py                  # Retry coordination
│   └── escalator.py                    # Escalation handling
├── langgraph_graph/
│   └── graph.py                        # Main graph definition
├── prompts/                            # Centralized prompts
├── config/
│   └── settings.yaml                   # Configuration
├── utils/
│   ├── logger.py                       # Logging utilities
│   └── helpers.py                      # Helper functions
├── test/                               # Test suite
├── .env                                # Environment variables
├── requirements.txt                    # Dependencies
├── README.md                           # This file
└── main.py                             # Entry point
\`\`\`

## 🚀 Quick Start

### Prerequisites

- Python 3.12.0+
- OpenAI API key
- Git

### Installation

1. **Clone the repository:**
   \`\`\`bash
   git clone <repository-url>
   cd support-ticket-agent
   \`\`\`

2. **Create virtual environment:**
   \`\`\`bash
   python -m venv venv
   venv\\Scripts\\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   \`\`\`

3. **Install dependencies:**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **Configure environment:**
   \`\`\`bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   \`\`\`

5. **Run the agent:**
   \`\`\`bash
   python main.py
   \`\`\`

## 🎯 Core Features

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

## 🔧 Configuration

Edit \`config/settings.yaml\` to customize:

\`\`\`yaml
llm:
  provider: "openai"
  model: "gpt-4o-mini"
  temperature: 0.1
  max_tokens: 1000

retry:
  max_attempts: 2

categories:
  - "Billing"
  - "Technical"
  - "Security"
  - "General"
\`\`\`

## 📊 Usage Examples

### Interactive Mode
\`\`\`bash
python main.py
# Choose option 1 for interactive demo
\`\`\`

### Sample Tickets
\`\`\`bash
python main.py
# Choose option 2 to run predefined sample tickets
\`\`\`

### Programmatic Usage
\`\`\`python
from main import process_ticket
import asyncio

result = asyncio.run(process_ticket(
    subject="Cannot login to account",
    description="Getting invalid credentials error after password change"
))

print(f"Category: {result['category']}")
print(f"Response: {result['final_response']}")
print(f"Escalated: {result['escalated']}")
\`\`\`

## 🧪 Testing

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

## 📈 Monitoring and Logging

### Log Files
- Application logs: \`logs/support_agent_YYYYMMDD.log\`
- Escalation tracking: \`data/escalation_log.csv\`

### Key Metrics
- Processing success rate
- Average attempts per ticket
- Escalation rate by category
- Response quality scores

## 🔍 Design Decisions

### 1. Modular Node Architecture
Each processing step is implemented as a separate node for:
- **Maintainability**: Easy to modify individual components
- **Testability**: Isolated testing of each function
- **Reusability**: Nodes can be reused in different workflows
- **Debugging**: Clear separation of concerns

### 2. State-Driven Processing
Using TypedDict for state management provides:
- **Type Safety**: Clear data contracts between nodes
- **Transparency**: Full visibility into processing state
- **Debugging**: Easy to trace data flow and transformations

### 3. Feedback-Driven Retry Logic
The retry mechanism incorporates reviewer feedback to:
- **Improve Context**: Refine retrieval based on specific feedback
- **Learn from Failures**: Each attempt builds on previous learnings
- **Prevent Infinite Loops**: Maximum attempt limits with escalation

### 4. Category-Specific Knowledge Base
Separate knowledge bases for each category enable:
- **Targeted Retrieval**: More relevant context for each ticket type
- **Scalability**: Easy to add new categories and knowledge
- **Maintenance**: Independent updates to category-specific information

## 🚨 Error Handling

The system implements comprehensive error handling:

1. **Graceful Degradation**: Continues processing with fallback responses
2. **Error Logging**: Detailed error tracking for debugging
3. **User Communication**: Clear error messages for end users
4. **Escalation Triggers**: Automatic escalation on critical failures

## 🔐 Security Considerations

- **API Key Management**: Secure environment variable storage
- **Input Validation**: Comprehensive input sanitization
- **Error Information**: Careful error message sanitization
- **Logging Privacy**: No sensitive data in logs

## 📋 Troubleshooting

### Common Issues

1. **OpenAI API Errors**
   - Verify API key in .env file
   - Check API quota and billing status
   - Ensure network connectivity

2. **Classification Failures**
   - Check prompt templates in prompts/ directory
   - Verify model availability and permissions
   - Review input data format

3. **Knowledge Base Issues**
   - Ensure knowledge base files exist in data/knowledge_base/
   - Check file permissions and encoding
   - Verify document content format

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♂️ Support

For questions or issues:
- Create an issue in the GitHub repository
- Review the troubleshooting section
- Check the logs for detailed error information

---

**Built with ❤️ using LangGraph and OpenAI**

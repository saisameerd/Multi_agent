
# Cloning the repository
```
cd ~
git clone https://github.com/murlik1/adk-examples.git
```

# Virtual Environment Setup
```
cd ~ 
python -m pip install virtualenv --break-system-packages
python -m virtualenv venv 
source ./venv/bin/activate
python -m pip install -r ~/adk-examples/ai-adk-nl2sql/requirements.txt
```

# Perform configuration changes
```
nl2sql/.env file to initiate the environment variables
```

# Local Execution
```
cd ~/adk-examples/ai-adk-nl2sql/
adk web
```

# Enhanced Functionality

This nl2sql agent now supports **dual-flow architecture**:

## 1. Original nl2sql Flow
For regular database queries and data analysis:
- Query understanding and analysis
- SQL generation
- Query review and optimization
- Query execution

## 2. Tone Analysis Flow
For conversation sentiment analysis:
- Intent detection (automatically routes to tone analysis)
- Conversation data retrieval from BigQuery
- Tone analysis using Gemini

### Usage Examples:

**Tone Analysis Queries:**
- "Perform tone analysis on conversations from yesterday"
- "Analyze sentiment of chat data from last week"
- "What's the emotional tone of customer conversations this month?"

**Regular nl2sql Queries:**
- "Fetch me count of orders as per status for orders placed on 15-05-2025"
- "Fetch me orders that are in cancelled state on 15-05-2025"
- "Fetch me the products most ordered in 2025"

The agent automatically detects the user's intent and routes to the appropriate workflow.


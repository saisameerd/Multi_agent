
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

This nl2sql agent now supports **triple-flow architecture**:

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

## 3. No-Match Analysis Flow (NEW!)
For Dialogflow CX bot optimization:
- Intent detection (automatically routes to no-match analysis)
- Conversation data retrieval with no-match events
- No-match pattern analysis and recommendations
- Dialogflow CX bot structure analysis (if bot JSON provided)
- CSV generation for Dialogflow CX import (creates downloadable files)

### Usage Examples:

**No-Match Analysis Queries:**
- "Analyze no_match events from last week and generate CSV"
- "Find conversations with maximum no_match events this week"
- "Provide bot improvement suggestions for reducing no_match events"
- "Generate training phrases CSV for Dialogflow CX import"

**Tone Analysis Queries:**
- "Perform tone analysis on conversations from yesterday"
- "Analyze sentiment of chat data from last week"
- "What's the emotional tone of customer conversations this month?"

**Regular nl2sql Queries:**
- "Fetch me count of orders as per status for orders placed on 15-05-2025"
- "Fetch me orders that are in cancelled state on 15-05-2025"
- "Fetch me the products most ordered in 2025"

The agent automatically detects the user's intent and routes to the appropriate workflow.

## Key Features

### No-Match Analysis Capabilities:
- **Intelligent Pattern Detection**: Identifies common no_match patterns in conversation data
- **Bot-Specific Recommendations**: Provides actionable suggestions based on your bot structure
- **CSV Generation**: Creates CSV files with training phrases for Dialogflow CX import
- **Priority Scoring**: Ranks recommendations by potential impact
- **File-Based Output**: Creates downloadable CSV files in the current directory

### Integration with Dialogflow CX:
- **Bot Structure Analysis**: Analyzes your Dialogflow CX bot JSON structure
- **Training Phrase Extraction**: Extracts existing training phrases for optimization
- **Intent Gap Analysis**: Identifies missing intents and coverage gaps
- **Import-Ready CSVs**: Generates CSV files that can be directly imported into Dialogflow CX

## Workflow Architecture

```
User Query → Intent Detection → Workflow Routing
                                    ↓
        ┌─────────────────┬─────────────────┬─────────────────┐
        │                 │                 │                 │
        ▼                 ▼                 ▼                 ▼
   NL2SQL Flow      Tone Analysis    No-Match Analysis    Error Handling
        │                 │                 │
        │                 │                 ├── Conversation Data Retrieval
        │                 │                 ├── No-Match Pattern Analysis
        │                 │                 ├── Bot Structure Analysis
        │                 │                 └── CSV Generation (File Output)
        │                 │
        │                 ├── Conversation Data Retrieval
        │                 └── Tone Analysis
        │
        ├── Query Understanding
        ├── Query Generation
        ├── Query Review
        └── Query Execution
```


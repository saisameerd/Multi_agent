from google.adk.agents.callback_context import CallbackContext
from google.adk.sessions.state import State
from google.adk.tools import ToolContext
import os
from nl2sql.tools.bigquery_tools import bigquery_metdata_extraction_tool

def initialize_state_var(callback_context: CallbackContext):
    # Initialize BigQuery configuration
    PROJECT = os.environ.get("PROJECT")
    BQ_LOCATION = os.environ.get("BQ_LOCATION")
    DATASET =  os.environ.get("DATASET")

    callback_context.state["PROJECT"] = PROJECT
    callback_context.state["BQ_LOCATION"] = BQ_LOCATION
    callback_context.state["DATASET"] = DATASET

    # Initialize BigQuery metadata for nl2sql flow
    bigquery_metadata = bigquery_metdata_extraction_tool(PROJECT=PROJECT,
        BQ_LOCATION=BQ_LOCATION,
        DATASET=DATASET)

    callback_context.state["bigquery_metadata"] = bigquery_metadata

    # Initialize tone analysis flow state variables
    callback_context.state["intent_detection_output"] = ""
    callback_context.state["conversation_data_output"] = ""
    callback_context.state["tone_analysis_output"] = ""
    
    # Initialize nl2sql flow state variables (maintain existing)
    callback_context.state["query_understanding_output"] = ""
    callback_context.state["query_generation_output"] = ""
    callback_context.state["query_review_rewrite_output"] = ""
    callback_context.state["query_execution_output"] = ""

from google.adk.agents import LlmAgent
from nl2sql.sub_agents.conversation_data_retrieval_agent.prompts import CONVERSATION_DATA_RETRIEVAL_INSTRUCTION_STR
from nl2sql.tools.bigquery_tools import bigquery_execution_tool

# LLM Agent for retrieving conversation data from BigQuery
conversation_data_retrieval_agent = LlmAgent(
    name = "conversation_data_retrieval_agent",
    model = "gemini-2.5-flash",
    description = "This agent is responsible for generating and executing BigQuery SQL to retrieve conversation data for tone analysis and no-match analysis",
    instruction = CONVERSATION_DATA_RETRIEVAL_INSTRUCTION_STR,
    tools = [bigquery_execution_tool],
    output_key = "conversation_data_output"
) 
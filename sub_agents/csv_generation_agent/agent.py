from google.adk.agents import LlmAgent
from nl2sql.sub_agents.csv_generation_agent.prompts import CSV_GENERATION_INSTRUCTION_STR
from nl2sql.tools.csv_artifact_tool import csv_artifact_tool

# LLM Agent for generating CSV files for Dialogflow CX import
csv_generation_agent = LlmAgent(
    name = "csv_generation_agent",
    model = "gemini-2.5-flash",
    description = "This agent is responsible for generating CSV files with training phrases that can be imported into Dialogflow CX to reduce no-match events",
    instruction = CSV_GENERATION_INSTRUCTION_STR,
    tools = [csv_artifact_tool],
    output_key = "csv_generation_output"
) 
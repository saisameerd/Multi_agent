from google.adk.agents import LlmAgent
from nl2sql.sub_agents.no_match_analysis_agent.prompts import NO_MATCH_ANALYSIS_INSTRUCTION_STR

# LLM Agent for analyzing no-match events and providing recommendations
no_match_analysis_agent = LlmAgent(
    name = "no_match_analysis_agent",
    model = "gemini-2.5-flash",
    description = "This agent is responsible for analyzing no_match events in conversation data and providing bot-specific recommendations to reduce no_match occurrences",
    instruction = NO_MATCH_ANALYSIS_INSTRUCTION_STR,
    output_key = "no_match_analysis_output"
) 
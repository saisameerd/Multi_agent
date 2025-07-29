from google.adk.agents import LlmAgent
from nl2sql.sub_agents.tone_analysis_agent.prompts import TONE_ANALYSIS_INSTRUCTION_STR

# LLM Agent for analyzing conversation tone and sentiment
tone_analysis_agent = LlmAgent(
    name = "tone_analysis_agent",
    model = "gemini-2.5-flash",
    description = "This agent is responsible for analyzing conversation data to determine the emotional tone or sentiment of each conversation",
    instruction = TONE_ANALYSIS_INSTRUCTION_STR,
    output_key = "tone_analysis_output"
) 
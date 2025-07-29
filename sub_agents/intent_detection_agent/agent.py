from google.adk.agents import LlmAgent
from nl2sql.sub_agents.intent_detection_agent.prompts import INTENT_DETECTION_INSTRUCTION_STR

# LLM Agent for detecting user intent (tone_analysis vs nl2sql)
intent_detection_agent = LlmAgent(
    name = "intent_detection_agent",
    model = "gemini-2.5-flash",
    description = "This agent is responsible for analyzing user queries to determine if they want tone analysis or regular nl2sql functionality",
    instruction = INTENT_DETECTION_INSTRUCTION_STR,
    output_key = "intent_detection_output"
) 
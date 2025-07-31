from google.adk.agents import LlmAgent
from nl2sql.sub_agents.dialogflow_cx_parser_agent.prompts import DIALOGFLOW_CX_PARSER_INSTRUCTION_STR

# LLM Agent for analyzing Dialogflow CX bot structure
dialogflow_cx_parser_agent = LlmAgent(
    name = "dialogflow_cx_parser_agent",
    model = "gemini-2.5-flash",
    description = "This agent is responsible for analyzing Dialogflow CX bot JSON structure and extracting intent information for optimization",
    instruction = DIALOGFLOW_CX_PARSER_INSTRUCTION_STR,
    output_key = "dialogflow_analysis_output"
) 
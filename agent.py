from google.adk.agents import LlmAgent, BaseAgent
from nl2sql.sub_agents.query_understanding_agent.agent import query_understanding_agent
from nl2sql.sub_agents.query_generation_agent.agent import query_generation_agent
from nl2sql.sub_agents.query_review_rewrite_agent.agent import query_review_rewrite_agent
from nl2sql.sub_agents.query_execution_agent.agent import query_execution_agent
from nl2sql.sub_agents.conversation_data_retrieval_agent.agent import conversation_data_retrieval_agent
from nl2sql.sub_agents.tone_analysis_agent.agent import tone_analysis_agent
from nl2sql.sub_agents.intent_detection_agent.agent import intent_detection_agent
from nl2sql.sub_agents.no_match_analysis_agent.agent import no_match_analysis_agent
from nl2sql.sub_agents.dialogflow_cx_parser_agent.agent import dialogflow_cx_parser_agent
from nl2sql.sub_agents.csv_generation_agent.agent import csv_generation_agent
from nl2sql.tools.initialize_state import initialize_state_var

from typing import Dict, Any, List
from typing import AsyncGenerator
from typing_extensions import override
from google.adk.events import Event, EventActions
from google.adk.agents.invocation_context import InvocationContext
from google.adk.tools import ToolContext
import logging

# --- Configure Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Orchestrator Agent
class OrchestratorAgent(BaseAgent):
    intent_detection_agent: LlmAgent
    query_understanding_agent: LlmAgent
    query_generation_agent: LlmAgent
    query_review_rewrite_agent: LlmAgent
    query_execution_agent: LlmAgent
    conversation_data_retrieval_agent: LlmAgent
    tone_analysis_agent: LlmAgent
    no_match_analysis_agent: LlmAgent
    dialogflow_cx_parser_agent: LlmAgent
    csv_generation_agent: LlmAgent

    def __init__(self,
        name:str,
        intent_detection_agent: LlmAgent,
        query_understanding_agent: LlmAgent,
        query_generation_agent: LlmAgent,
        query_review_rewrite_agent: LlmAgent,
        query_execution_agent:LlmAgent,
        conversation_data_retrieval_agent: LlmAgent,
        tone_analysis_agent: LlmAgent,
        no_match_analysis_agent: LlmAgent,
        dialogflow_cx_parser_agent: LlmAgent,
        csv_generation_agent: LlmAgent):
        
        super().__init__(
            name = name,
            intent_detection_agent = intent_detection_agent,
            query_understanding_agent = query_understanding_agent,
            query_generation_agent = query_generation_agent,
            query_review_rewrite_agent = query_review_rewrite_agent,
            query_execution_agent=query_execution_agent,
            conversation_data_retrieval_agent=conversation_data_retrieval_agent,
            tone_analysis_agent=tone_analysis_agent,
            no_match_analysis_agent=no_match_analysis_agent,
            dialogflow_cx_parser_agent=dialogflow_cx_parser_agent,
            csv_generation_agent=csv_generation_agent,
            before_agent_callback=initialize_state_var,
            description = "This is a Orchestrator Agent which executes nl2sql, tone analysis, or no-match analysis workflows based on user intent"
        )

    @override
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        logger.info(f"[{self.name}] - Starting enhanced workflow with intent detection.")
        
        # Step 1: Intent detection using LLM
        async for event in self.intent_detection_agent.run_async(ctx):
            logger.info(f"[{self.name}] - {event.model_dump_json(indent=2, exclude_none=True)}")
            yield event
        
        intent_output = ctx.session.state.get('intent_detection_output', '')
        logger.info(f"[{self.name}] - Intent detection result: {intent_output}")

        if not intent_output:
            logger.error(f"[{self.name}] - No intent detection output")
            return
        
        # Parse intent from LLM output
        if "tone_analysis" in intent_output.lower():
            # Execute tone analysis flow
            async for event in self._execute_tone_analysis_flow(ctx):
                yield event
        elif "no_match_analysis" in intent_output.lower():
            # Execute no-match analysis flow
            async for event in self._execute_no_match_analysis_flow(ctx):
                yield event
        else:
            # Execute original nl2sql flow
            async for event in self._execute_nl2sql_flow(ctx):
                yield event

    async def _execute_nl2sql_flow(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        """Execute the original nl2sql workflow"""
        logger.info(f"[{self.name}] - Executing nl2sql workflow.")

        # First call to query_understanding_agent
        async for event in self.query_understanding_agent.run_async(ctx):
            logger.info(f"[{self.name}] - {event.model_dump_json(indent=2, exclude_none=True)}")
            yield event
        
        query_understanding_output = ""
        if "query_understanding_output" in ctx.session.state:
            query_understanding_output = ctx.session.state['query_understanding_output']
            logger.info(f"[{self.name}] - {query_understanding_output}")

        if query_understanding_output is None or "```json" not in query_understanding_output:
            return
        
        # query generation agent call
        async for event in self.query_generation_agent.run_async(ctx):
            logger.info(f"[{self.name}] - {event.model_dump_json(indent=2, exclude_none=True)}")
            yield event
        
        query_generation_output = ctx.session.state['query_generation_output']
        logger.info(f"[{self.name}] - {query_generation_output}")

        if query_generation_output is None:
            return

        # query review rewrite agent call
        async for event in self.query_review_rewrite_agent.run_async(ctx):
            logger.info(f"[{self.name}] - {event.model_dump_json(indent=2, exclude_none=True)}")
            yield event
        
        query_review_rewrite_output = ctx.session.state['query_review_rewrite_output']
        logger.info(f"[{self.name}] - {query_review_rewrite_output}")

        if query_review_rewrite_output is None:
            return
        
        # query execution agent call
        async for event in self.query_execution_agent.run_async(ctx):
            logger.info(f"[{self.name}] - {event.model_dump_json(indent=2, exclude_none=True)}")
            yield event
        
        query_execution_output = ctx.session.state['query_execution_output']
        logger.info(f"[{self.name}] - {query_execution_output}")

        if query_execution_output is None:
            return

    async def _execute_tone_analysis_flow(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        """Execute the tone analysis workflow"""
        logger.info(f"[{self.name}] - Executing tone analysis workflow.")

        # Step 1: Conversation data retrieval
        async for event in self.conversation_data_retrieval_agent.run_async(ctx):
            logger.info(f"[{self.name}] - {event.model_dump_json(indent=2, exclude_none=True)}")
            yield event
        
        conversation_data_output = ctx.session.state.get('conversation_data_output', '')
        logger.info(f"[{self.name}] - Conversation data retrieved: {len(conversation_data_output)} characters")

        if not conversation_data_output:
            logger.warning(f"[{self.name}] - No conversation data retrieved")
            return

        # Step 2: Tone analysis
        async for event in self.tone_analysis_agent.run_async(ctx):
            logger.info(f"[{self.name}] - {event.model_dump_json(indent=2, exclude_none=True)}")
            yield event
        
        tone_analysis_output = ctx.session.state.get('tone_analysis_output', '')
        logger.info(f"[{self.name}] - Tone analysis completed: {len(tone_analysis_output)} characters")

        if not tone_analysis_output:
            logger.warning(f"[{self.name}] - No tone analysis results")
            return

    async def _execute_no_match_analysis_flow(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        """Execute the no-match analysis workflow"""
        logger.info(f"[{self.name}] - Executing no-match analysis workflow.")

        # Step 1: Conversation data retrieval
        async for event in self.conversation_data_retrieval_agent.run_async(ctx):
            logger.info(f"[{self.name}] - {event.model_dump_json(indent=2, exclude_none=True)}")
            yield event
        
        conversation_data_output = ctx.session.state.get('conversation_data_output', '')
        logger.info(f"[{self.name}] - Conversation data retrieved: {len(conversation_data_output)} characters")

        if not conversation_data_output:
            logger.warning(f"[{self.name}] - No conversation data retrieved")
            return

        # Step 2: No-match analysis
        async for event in self.no_match_analysis_agent.run_async(ctx):
            logger.info(f"[{self.name}] - {event.model_dump_json(indent=2, exclude_none=True)}")
            yield event
        
        no_match_analysis_output = ctx.session.state.get('no_match_analysis_output', '')
        logger.info(f"[{self.name}] - No-match analysis completed: {len(no_match_analysis_output)} characters")

        if not no_match_analysis_output:
            logger.warning(f"[{self.name}] - No no-match analysis results")
            return

        # Step 3: Dialogflow CX structure analysis (if bot JSON is provided)
        if ctx.session.state.get('dialogflow_bot_json'):
            async for event in self.dialogflow_cx_parser_agent.run_async(ctx):
                logger.info(f"[{self.name}] - {event.model_dump_json(indent=2, exclude_none=True)}")
                yield event
            
            dialogflow_analysis_output = ctx.session.state.get('dialogflow_analysis_output', '')
            logger.info(f"[{self.name}] - Dialogflow CX analysis completed: {len(dialogflow_analysis_output)} characters")

        # Step 4: CSV generation (if requested)
        if "csv" in ctx.session.state.get('user_query', '').lower():
            async for event in self.csv_generation_agent.run_async(ctx):
                logger.info(f"[{self.name}] - {event.model_dump_json(indent=2, exclude_none=True)}")
                yield event
            
            csv_generation_output = ctx.session.state.get('csv_generation_output', '')
            logger.info(f"[{self.name}] - CSV generation completed: {len(csv_generation_output)} characters")

            if not csv_generation_output:
                logger.warning(f"[{self.name}] - No CSV generation results")
                return

orchestrator_agent = OrchestratorAgent(name="orchestrator_agent",
    intent_detection_agent=intent_detection_agent,
    query_understanding_agent=query_understanding_agent,
    query_generation_agent=query_generation_agent,
    query_review_rewrite_agent=query_review_rewrite_agent,
    query_execution_agent=query_execution_agent,
    conversation_data_retrieval_agent=conversation_data_retrieval_agent,
    tone_analysis_agent=tone_analysis_agent,
    no_match_analysis_agent=no_match_analysis_agent,
    dialogflow_cx_parser_agent=dialogflow_cx_parser_agent,
    csv_generation_agent=csv_generation_agent
    )

root_agent = orchestrator_agent

"""
Fetch me count of orders as per status for orders placed on 15-05-2025
Fetch me orders that are in cancelled state on 15-05-2025
Fetch me the products most ordered in 2025
Fetch me the top selling product in 2025 as per number of orders placed
Fetch me product with highest available inventory
"""
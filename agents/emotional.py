from agents.base import BaseAgent
from prompts import emotional as prompts


class EmotionalAgent(BaseAgent):
    agent_type = "emotional"
    display_name = "情感输出"
    system_prompt = prompts.SYSTEM_PROMPT
    initial_human_template = prompts.INITIAL_HUMAN_TEMPLATE
    revision_human_template = prompts.REVISION_HUMAN_TEMPLATE
    temperature = 0.75

from agents.base import BaseAgent
from prompts import rational as prompts


class RationalAgent(BaseAgent):
    agent_type = "rational"
    display_name = "理性分析"
    system_prompt = prompts.SYSTEM_PROMPT
    initial_human_template = prompts.INITIAL_HUMAN_TEMPLATE
    revision_human_template = prompts.REVISION_HUMAN_TEMPLATE
    temperature = 0.6

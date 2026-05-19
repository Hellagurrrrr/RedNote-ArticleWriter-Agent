from typing import Type

from agents.base import BaseAgent
from agents.emotional import EmotionalAgent
from agents.rational import RationalAgent

AGENT_REGISTRY: dict[str, Type[BaseAgent]] = {
    EmotionalAgent.agent_type: EmotionalAgent,
    RationalAgent.agent_type: RationalAgent,
}


def list_agents() -> list[tuple[str, str]]:
    return [(cls.agent_type, cls.display_name) for cls in AGENT_REGISTRY.values()]


def get_agent(agent_type: str) -> BaseAgent:
    key = agent_type.strip().lower()
    if key not in AGENT_REGISTRY:
        options = ", ".join(AGENT_REGISTRY.keys())
        raise ValueError(f"未知文案类型 '{agent_type}'，可选：{options}")
    return AGENT_REGISTRY[key]()

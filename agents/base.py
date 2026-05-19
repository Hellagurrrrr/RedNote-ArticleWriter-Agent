from abc import ABC, abstractmethod
from typing import Any

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable

from llm.factory import get_structured_model
from schemas import RedNotePost


INITIAL_FIELD_NAMES = (
    "product_name",
    "product_info",
    "target_audience",
    "selling_points",
    "tone",
    "goal",
)


class BaseAgent(ABC):
    agent_type: str
    display_name: str
    system_prompt: str
    initial_human_template: str
    revision_human_template: str
    temperature: float = 0.7

    def build_chain(self) -> Runnable:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                MessagesPlaceholder("history"),
                ("human", "{user_input}"),
            ]
        )
        model = get_structured_model(RedNotePost, temperature=self.temperature)
        return prompt | model

    def format_initial_message(self, inputs: dict[str, Any]) -> str:
        return self.initial_human_template.format(**inputs)

    def format_revision_message(self, feedback: str, draft: RedNotePost) -> str:
        return self.revision_human_template.format(
            feedback=feedback,
            draft_summary=self.summarize_draft(draft),
        )

    @staticmethod
    def summarize_draft(draft: RedNotePost) -> str:
        titles = "\n".join(f"- {t}" for t in draft.titles)
        return (
            f"推荐标题：\n{titles}\n\n"
            f"目标人群：{draft.target_audience}\n\n"
            f"正文：\n{draft.content}\n\n"
            f"行动引导：{draft.cta}\n\n"
            f"标签：{', '.join(draft.tags)}"
        )

    @staticmethod
    def draft_to_ai_message(draft: RedNotePost) -> AIMessage:
        return AIMessage(content=BaseAgent.summarize_draft(draft))

    def invoke(
        self,
        user_input: str,
        history: list[BaseMessage],
    ) -> RedNotePost:
        chain = self.build_chain()
        return chain.invoke({"history": history, "user_input": user_input})

    @classmethod
    def empty_inputs(cls) -> dict[str, str]:
        return {name: "" for name in INITIAL_FIELD_NAMES}

    @classmethod
    def prompt_for_inputs(cls) -> dict[str, str]:
        """CLI 交互式采集首轮字段。"""
        labels = {
            "product_name": "活动/产品名称",
            "product_info": "产品介绍",
            "target_audience": "目标人群",
            "selling_points": "希望强调的卖点",
            "tone": "文案语气",
            "goal": "转化目标",
        }
        result: dict[str, str] = {}
        for key in INITIAL_FIELD_NAMES:
            label = labels[key]
            value = input(f"{label}：").strip()
            result[key] = value
        return result

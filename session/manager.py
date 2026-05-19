from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import BaseMessage, HumanMessage

from agents.base import BaseAgent
from agents.registry import get_agent
from schemas import RedNotePost


@dataclass
class Session:
    session_id: str
    agent_type: str
    initial_inputs: dict[str, Any] = field(default_factory=dict)
    last_draft: RedNotePost | None = None
    turn_count: int = 0


class SessionManager:
    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}
        self._histories: dict[str, InMemoryChatMessageHistory] = {}

    def create(self, agent_type: str, initial_inputs: dict[str, Any] | None = None) -> Session:
        session = Session(
            session_id=str(uuid4()),
            agent_type=agent_type,
            initial_inputs=initial_inputs or {},
        )
        self._sessions[session.session_id] = session
        self._histories[session.session_id] = InMemoryChatMessageHistory()
        return session

    def get(self, session_id: str) -> Session:
        if session_id not in self._sessions:
            raise KeyError(f"会话不存在：{session_id}")
        return self._sessions[session_id]

    def get_history(self, session_id: str) -> InMemoryChatMessageHistory:
        if session_id not in self._histories:
            raise KeyError(f"会话不存在：{session_id}")
        return self._histories[session_id]

    def generate(self, session_id: str, inputs: dict[str, Any]) -> RedNotePost:
        session = self.get(session_id)
        agent = get_agent(session.agent_type)
        session.initial_inputs = inputs

        user_message = agent.format_initial_message(inputs)
        draft = self._invoke_and_record(session, agent, user_message)
        session.turn_count = 1
        return draft

    def revise(self, session_id: str, feedback: str) -> RedNotePost:
        session = self.get(session_id)
        if session.last_draft is None:
            raise RuntimeError("请先生成首版文案，再进行修改。")

        agent = get_agent(session.agent_type)
        user_message = agent.format_revision_message(feedback, session.last_draft)
        draft = self._invoke_and_record(session, agent, user_message)
        session.turn_count += 1
        return draft

    def _invoke_and_record(
        self,
        session: Session,
        agent: BaseAgent,
        user_message: str,
    ) -> RedNotePost:
        history_store = self.get_history(session.session_id)
        history_messages: list[BaseMessage] = list(history_store.messages)

        draft = agent.invoke(user_message, history_messages)

        history_store.add_message(HumanMessage(content=user_message))
        history_store.add_message(agent.draft_to_ai_message(draft))

        session.last_draft = draft
        return draft

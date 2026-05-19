from typing import Type

from langchain_deepseek import ChatDeepSeek
from pydantic import BaseModel

from config.settings import API_KEY, MODEL_NAME
from schemas import RedNotePost

_base_model: ChatDeepSeek | None = None


def get_base_model(temperature: float = 0.7) -> ChatDeepSeek:
    return ChatDeepSeek(
        model=MODEL_NAME,
        api_key=API_KEY,
        temperature=temperature,
        extra_body={"thinking": {"type": "disabled"}},
    )


def get_structured_model(
    output_schema: Type[BaseModel] = RedNotePost,
    temperature: float = 0.7,
) -> ChatDeepSeek:
    return get_base_model(temperature=temperature).with_structured_output(output_schema)

"""向后兼容：请优先使用 llm.factory.get_structured_model。"""

from llm.factory import get_structured_model
from schemas import RedNotePost

authentic_sharing_model = get_structured_model(RedNotePost)

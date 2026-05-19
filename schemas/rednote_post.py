from typing import List

from pydantic import BaseModel, Field


class RedNotePost(BaseModel):
    """小红书宣传文案结构"""

    titles: List[str] = Field(description="3个小红书风格标题，包含情绪钩子或结果导向")
    target_audience: str = Field(description="这篇文案主要面向的人群")
    pain_points: List[str] = Field(description="目标用户的多个痛点")
    selling_points: List[str] = Field(description="产品/活动的多个核心卖点")
    content: str = Field(description="完整小红书正文")
    cta: str = Field(description="结尾行动引导，例如评论、私信、报名、收藏")
    tags: List[str] = Field(description="适合小红书发布的标签，5-8个")
    risk_notes: List[str] = Field(description="可能过度营销、不真实、需要人工确认的地方")

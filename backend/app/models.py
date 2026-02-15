from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Article(BaseModel):
    title: str
    url: str
    source: str
    published_at: Optional[datetime] = None
    content: Optional[str] = None
    summary: Optional[str] = None

class StoryCluster(BaseModel):
    cluster_id: str
    primary_article: Article
    related_articles: List[Article]
    topic_label: str

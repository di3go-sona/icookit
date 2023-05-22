from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass

class RedditPost(Base):
    __tablename__ = "reddit_posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    url: Mapped[str]
    author: Mapped[str]
    text: Mapped[str]

    def __repr__(self) -> str:
        return f"RedditPost(title={self.title}, text={self.text}, url={self.url}, author={self.author})"
    
class Recipe(Base):
    __tablename__ = "recipes"
    id: Mapped[int] = mapped_column(primary_key=True)
    raw_recipe_id: Mapped[int] = mapped_column(ForeignKey("reddit_posts.id"))
    raw_recipe = relationship("RedditPost", backref="recipes")
    

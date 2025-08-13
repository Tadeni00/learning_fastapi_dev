from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

from .schema import PostBase, CreatePost, UpdatePost
from datetime import datetime
from pydantic import EmailStr, conint
from typing import Optional


class PostModel(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)

    title = Column(String, nullable=False)

    content = Column(String, nullable=False)

    published = Column(Boolean, server_default="TRUE", nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    owner = relationship("UserModel")


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)

    email = Column(String, nullable=False, unique=True)

    password = Column(String, nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    phone_number = Column(String, nullable=True)


class VotesModel(Base):
    __tablename__ = "votes"
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )

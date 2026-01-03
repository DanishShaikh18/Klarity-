# app/db/models.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base


# ===============================
# 1️⃣ Chat Table
# ===============================
class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    messages = relationship("Message", back_populates="chat", cascade="all, delete")
    documents = relationship("Document", back_populates="chat", cascade="all, delete")


# ===============================
# 2️⃣ Message Table
# ===============================
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))

    role = Column(String, nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)

    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationship
    chat = relationship("Chat", back_populates="messages")


# ===============================
# 3️⃣ Document Table
# ===============================
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))

    file_name = Column(String, nullable=False)
    doc_id = Column(String, nullable=False)   # the UUID you store inside Qdrant payload
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    chat = relationship("Chat", back_populates="documents")

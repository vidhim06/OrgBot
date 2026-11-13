
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    func
)
from sqlalchemy.orm import relationship

from src.database.database import Base


class Organisation(Base):
    __tablename__ = "organisations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())

    users = relationship("User", back_populates="organisation")
    documents = relationship("Document", back_populates="organisation")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(30), default="admin")
    is_active = Column(Boolean, default=True)
    organisation_id = Column(
        Integer,
        ForeignKey("organisations.id"),
        nullable=False
    )
    created_at = Column(DateTime, server_default=func.now())

    organisation = relationship("Organisation", back_populates="users")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    pages_processed = Column(Integer, default=0)
    chunks_created = Column(Integer, default=0)
    status = Column(String(30), default="processed")
    organisation_id = Column(
        Integer,
        ForeignKey("organisations.id"),
        nullable=False,
        index=True
    )
    created_at = Column(DateTime, server_default=func.now())

    organisation = relationship("Organisation", back_populates="documents")

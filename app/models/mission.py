from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True)
    cat_id = Column(Integer, ForeignKey("spy_cats.id"), nullable=True)
    complete = Column(Boolean, default=False, nullable=False)

    cat = relationship("SpyCat", back_populates="mission")
    targets = relationship("Target", back_populates="mission", cascade="all, delete-orphan")


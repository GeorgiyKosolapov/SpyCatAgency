from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from app.database import Base


class SpyCat(Base):
    __tablename__ = "spy_cats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    years_of_experience = Column(Integer, nullable=False)
    breed = Column(String, nullable=False)
    salary = Column(Float, nullable=False)

    mission = relationship("Mission", back_populates="cat", uselist=False)


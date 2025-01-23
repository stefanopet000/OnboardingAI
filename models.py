from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Scenario(Base):
    __tablename__ = 'scenarios'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)  # e.g., Authentication, Shopping Cart
    given = Column(String, nullable=False)
    when = Column(String, nullable=False)
    then = Column(String, nullable=False)
    circle = Column(String, nullable=False)      # Changed from team to circle
    last_updated = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'given': self.given,
            'when': self.when,
            'then': self.then,
            'circle': self.circle,  # Changed from team to circle
            'last_updated': self.last_updated.isoformat(),
            'created_by': self.created_by
        } 
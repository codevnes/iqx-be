from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer, func

from app.db.session import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), index=True, unique=True)
    organ_code = Column(String(50), index=True, unique=True)
    isin_code = Column(String(50), index=True, unique=True, nullable=True)
    com_group_code = Column(String(50), index=True, nullable=True)
    icb_code = Column(String(50), index=True, nullable=True)
    organ_type_code = Column(String(50), index=True, nullable=True)
    com_type_code = Column(String(50), index=True, nullable=True)
    organ_short_name = Column(String(100), index=True)
    organ_name = Column(String(255), index=True)
    business_descriptions = Column(Text, nullable=True)
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 
from sqlalchemy import Column, Integer, String, LargeBinary
from app.database import Base

class FileMetaData(Base):
    __tablename__ = 'file_manager'

    id = Column(Integer,primary_key=True,index=True)
    uid = Column(String,unique=True,index=True)
    name = Column(String)
    file_size = Column(Integer)
    file_format = Column(String)
    file_extension = Column(String)
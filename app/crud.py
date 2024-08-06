from sqlalchemy.orm import Session
from app import models, schemas

def create_file_manager(db: Session, file: schemas.FileCreate):
    db_file = models.FileMetaData(
        uid=file.uid,
        name=file.name,
        file_size=file.file_size,
        file_format=file.file_format,
        file_extension=file.file_extension,
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file
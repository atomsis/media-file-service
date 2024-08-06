from  pydantic import BaseModel

class FileCreate(BaseModel):
    uid: str
    name: str
    file_size: int
    file_format: str
    file_extension: str

class FileResponse(FileCreate):
    class Config:
        from_attributes = True

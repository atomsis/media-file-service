import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app import crud, models, schemas, database
from app.cloud_storage import S3Client
from app.file_utils import save_file
import logging

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)

s3_client = S3Client(
    access_key='7665570705c94c37905811b978277ca3',
    secret_key='9e057ecc19764d50abcc28647016a266',
    endpoint_url='https://s3.storage.selcloud.ru',
    bucket_name='media-service'
)
logging.basicConfig(level=logging.INFO)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/upload/')
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
        Обрабатывает загрузку файлов, сохраняет файл в директорию uploads,
        генерирует уникальный идентификатор (UID) для файла и возвращает UID.

        Аргументы:
        file (UploadFile): Файл, загружаемый пользователем.

        Возвращает:
        dict: Словарь с уникальным идентификатором файла (UID).
    """
    try:
        logging.info(f"Начало загрузки файла: {file.filename}")
        file_contents = await file.read()
        file_path = save_file(file.filename, file_contents)

        file_uid = str(uuid.uuid4())
        logging.info(f"Файл сохранен на диске с UID: {file_uid}")

        file_metadata = schemas.FileCreate(
            uid=file_uid,
            name=file.filename,
            file_size=len(file_contents),
            file_format=file.content_type,
            file_extension=file.filename.split('.')[-1]
        )
        db_file = crud.create_file_manager(db, file_metadata)
        logging.info(f"Метаданные файла сохранены в базе данных: {db_file.uid}")

        await s3_client.upload_file(file_path)
        logging.info(f"Файл загружен в облачное хранилище: {file_path}")
        return {'uid': db_file.uid}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get('/file/{uid}')
async def get_file(uid: str, db: Session = Depends(get_db)):
    """
        Получает файл из облачного хранилища по его UID и возвращает его путь и имя.

        Аргументы:
        uid (str): Уникальный идентификатор файла.
        db (Session): Сессия базы данных, полученная через Depends.

        Возвращает:
        dict: Словарь с именем файла и его локальным путем.
    """
    logging.info(f"Запрос на получение файла с UID: {uid}")

    file_metadata = db.query(models.FileMetaData).filter(models.FileMetaData.uid == uid).first()
    if not file_metadata:
        logging.warning(f"Файл с UID {uid} не найден в базе данных")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='File not found')

    file_path = f"./uploads/{file_metadata.name}"
    await s3_client.download_file(file_metadata.name, file_path)
    logging.info(f"Файл успешно скачан с облака и сохранен на диск: {file_path}")
    return {"filename": file_metadata.name, "file_path": file_path}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", reload=True, port=8888)

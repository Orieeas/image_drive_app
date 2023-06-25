import io
import os
import uuid
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from uuid import uuid4
from fastapi.responses import FileResponse



app = FastAPI()
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://user:user@localhost:5432/quiz_questions"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)


Base = declarative_base()


from sqlalchemy.dialects.postgresql import UUID

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True)
    token = Column(String, unique=True)
    records = relationship("Record", back_populates="user")
    images = relationship("Image", back_populates="user")

from sqlalchemy import LargeBinary
class Record(Base):
    __tablename__ = "records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="records")
    url = Column(String)
    file = Column(String)

Base.metadata.create_all(bind=engine)


class CreateUserRequest(BaseModel):
    name: str


import requests

from pydantic import BaseModel
import base64
class AddRecordRequest(BaseModel):
    user_id: str
    token: str
    audio: str




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=dict)
def create_user(request: CreateUserRequest, session=Depends(get_db)):
    user = session.query(User).filter_by(name=request.name).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    token = str(uuid4())
    user_id = str(uuid4())

    user = User(name=request.name, token=token, id=user_id)
    session.add(user)
    session.commit()

    return {"user_id": user_id, "token": token}

class Image(Base):
    __tablename__ = "images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="images")
    url = Column(String)
    file = Column(String)

class AddImageRequest(BaseModel):
    user_id: str
    token: str
    image: str
    base_url: str

@app.post("/images", response_model=dict)
async def add_image(request: AddImageRequest, session=Depends(get_db)):
    user = session.query(User).filter_by(id=request.user_id, token=request.token).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user or token")

    id = str(uuid4())
    filename = str(uuid4())

    image = Image(id=id, filename=filename, user_id=request.user_id, url=f"{request.base_url}/image?id={id}&user={request.user_id}", file=request.image)
    session.add(image)
    session.commit()
    return {"url": image.url}

from PIL import Image as Alien_im
from PIL import Image as Alien_im
from io import BytesIO
from fastapi.responses import StreamingResponse


@app.get("/image")
async def get_image(id: str, user: str, session=Depends(get_db)):
    image = session.query(Image).filter(Image.id == id, Image.user_id == user).first()
    if not image:
        raise HTTPException(status_code=404)

    # Создаем объект изображения из байтов
    return (image.file)

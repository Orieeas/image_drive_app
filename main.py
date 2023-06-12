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
from pydub import AudioSegment


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


class Record(Base):
    __tablename__ = "records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="records")
    url = Column(String)

Base.metadata.create_all(bind=engine)


class CreateUserRequest(BaseModel):
    name: str

import requests
from pydantic import BaseModel
import base64
class AddRecordRequest(BaseModel):
    user_id: str
    token: str
    audio: bytes

    def to_dict(self):
        # Кодируем байты в base64
        audio_base64 = base64.b64encode(self.audio).decode('utf-8')
        # Создаем словарь с данными
        data = {"user_id": self.user_id, "token": self.token, "audio": audio_base64}
        return data


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


@app.post("/records", response_model=dict)
def add_record(request: AddRecordRequest, session=Depends(get_db)):
    # Authenticate user
    user = session.query(User).filter_by(id=request.user_id, token=request.token).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user or token")

    # Convert audio to mp3 format
    audio_wav = AudioSegment.from_file(io.BytesIO(request.audio), format="wav")
    audio_mp3 = io.BytesIO()
    audio_wav.export(audio_mp3, format="mp3")
    audio_mp3.seek(0)

    # Generate unique filename and save record to the database
    filename = str(uuid4()) + ".mp3"
    record = Record(filename=filename, user=user)
    session.add(record)
    session.commit()

    # Save the mp3 file to disk
    filepath = os.path.join("records", filename)
    audio_mp3.seek(0)
    with open(filepath, "wb") as f:
        f.write(audio_mp3.read())

    # Generate URL for the record
    url = f"http://localhost:8000/record?id={str(record.id)}&user={str(user.id)}"

    # Update the record URL in the database
    record.url = url
    session.commit()

    return {"url": url}

@app.post("/records", response_model=dict)
def add_record_1(request: AddRecordRequest, session=Depends(get_db)):
    # Authenticate user
    user = session.query(User).filter_by(id=request.user_id, token=request.token).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user or token")

    # Convert audio to mp3 format
    audio_wav = AudioSegment.from_file(io.BytesIO(request.audio), format="wav")
    audio_mp3 = io.BytesIO()
    audio_wav.export(audio_mp3, format="mp3")
    audio_mp3.seek(0)

    # Generate unique filename and save record to the database
    filename = str(uuid4()) + ".mp3"
    record = Record(filename=filename, user=user)
    session.add(record)
    session.commit()

    # Save the mp3 file to disk
    filepath = os.path.join("records", filename)
    with open(filepath, "wb") as f:
        f.write(audio_mp3.read())

    # Generate URL for the record
    url = f"http://localhost:8000/record?id={str(record.id)}&user={str(user.id)}"

    # Update the record URL in the database
    record.url = url
    session.commit()
    return {"url": url}


@app.get("/record", response_class=FileResponse)
def get_record(id: str, user: str, session=Depends(get_db)):
    # Authenticate user
    user = session.query(User).filter_by(id=user).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")

    # Retrieve the record from the database
    record = session.query(Record).filter_by(id=id, user=user).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    # Return the record file
    filepath = os.path.join("records", record.filename)
    return filepath

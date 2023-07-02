import uuid
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import Column, String, ForeignKey, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from uuid import uuid4
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

app = FastAPI()
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://user:user@localhost:5432/quiz_questions"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True)
    token = Column(String, unique=True)
    records = relationship("Record", back_populates="user")
    images = relationship("Image", back_populates="user")

class Record(Base):
    __tablename__ = "records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="records")
    url = Column(String)
    file = Column(String)

class CreateUserRequest(BaseModel):
    name: str

class AddRecordRequest(BaseModel):
    user_id: str
    token: str
    audio: str

class Image(Base):
    __tablename__ = "images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="images")
    url = Column(String)
    file = Column(String)
    img_mode = Column(String)
    img_size = Column(String)


class AddImageRequest(BaseModel):
    user_id: str
    token: str
    image: str
    base_url: str
    img_mode: str
    img_size: str


async def get_db():
    async with async_session() as session:
        yield session

@app.post("/users", response_model=dict)
async def create_user(request: CreateUserRequest, session=Depends(get_db)):
    user = await session.execute(select(User).where(User.name == request.name))
    user= user.scalar()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    token = str(uuid4())
    user_id = str(uuid4())
    user = User(name=request.name, token=token, id=user_id)
    session.add(user)
    await session.commit()
    return {"user_id": user_id, "token": token}

@app.post("/images", response_model=dict)
async def add_image(request: AddImageRequest, session=Depends(get_db)):
    user = await session.execute(select(User).where(User.id == request.user_id, User.token == request.token))
    user = user.scalar()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user, token or url")

    id = str(uuid4())
    filename = str(uuid4())
    image = Image(id=id, filename=filename, user_id=request.user_id, url=f"{request.base_url}/image?id={id}&user={request.user_id}", file=request.image,img_mode=request.img_mode,img_size=request.img_size)
    session.add(image)
    await session.commit()
    return {"url": image.url}

@app.get("/image")
async def get_image(url: str, user: str, session=Depends(get_db)):
    image = await session.execute(select(Image).where(Image.url == url, Image.user_id == user))
    image = image.scalar()
    if not image:
        raise HTTPException(status_code=404, detail="Invalid user_id or url")

    return {"file": image.file, "img_mode":image.img_mode, "img_size":image.img_size}
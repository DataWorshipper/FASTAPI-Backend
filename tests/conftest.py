import pytest
from fastapi.testclient import TestClient
from app.main import app
from app  import schemas
from app.database import get_db,Base
from app import model
import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
password = quote_plus(os.getenv("DB_PASSWORD"))

client=TestClient(app)

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://postgres:{password}"
    f"@{os.getenv('DB_HOST')}:5432/"
    f"{os.getenv('DB_NAME_TEST')}"
)
engine=create_engine(SQLALCHEMY_DATABASE_URL,echo=True)

TestingSessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    
@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
   
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db]=override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data={"email":"hello123@gmail.com","password":"password123"}
    res=client.post("/users/",json=user_data)
    assert res.status_code==201
    new_user=res.json()
    new_user['password']=user_data['password']
    return  new_user
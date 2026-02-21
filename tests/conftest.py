import pytest
from fastapi.testclient import TestClient
from app.main import app
from app  import schemas,model
from app.database import get_db,Base
from app.oauth2 import create_access_token
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
def test_user2(client):
    user_data={"email":"hello12@gmail.com","password":"password123"}
    res=client.post("/users/",json=user_data)
    assert res.status_code==201
    new_user=res.json()
    new_user['password']=user_data['password']
    return  new_user

@pytest.fixture
def test_user(client):
    user_data={"email":"hello123@gmail.com","password":"password123"}
    res=client.post("/users/",json=user_data)
    assert res.status_code==201
    new_user=res.json()
    new_user['password']=user_data['password']
    return  new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user['id']})
@pytest.fixture
def authorized_client(client,token):
    client.headers={
        **client.headers,"Authorization":f"Bearer {token}"
    }
    return client
    
@pytest.fixture
def test_posts(test_user,session,test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    },
    {
        "title": "4th title",
        "content": "4rd content",
        "owner_id": test_user2['id']
    }
    ]

    def create_post_model(post):
        return model.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(model.Post).all()
    return posts

@pytest.fixture()
def test_vote(test_posts, session, test_user):
    new_vote = model.Vote(post_id=test_posts[0].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()
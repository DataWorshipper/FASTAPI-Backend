from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import time
load_dotenv()
import os
from urllib.parse import quote_plus

password = quote_plus(os.getenv("DB_PASSWORD"))
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://postgres:{password}"
    f"@{os.getenv('DB_HOST')}:5432/"
    f"{os.getenv('DB_NAME')}"
)
engine=create_engine(SQLALCHEMY_DATABASE_URL,echo=True)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close() 
        
while True:
    try:
        conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        cursor_factory=RealDictCursor
    )
        cursor=conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connection to database  failed")
        print("Error: ",error)
        time.sleep(3)
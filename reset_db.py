import os
from sqlalchemy import create_engine, text
from app.database import SQLALCHEMY_DATABASE_URL 
from dotenv import load_dotenv


load_dotenv()

def reset_database():
  
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
  
    host = os.getenv("DB_HOST", "localhost")
    
    query = text("TRUNCATE posts, votes RESTART IDENTITY CASCADE;")
    
    try:
        with engine.connect() as conn:
            print(f"Connecting to host: {host}...")
            conn.execute(query)
            conn.commit()
            print("Successfully cleared posts and votes. Counters reset to 1.")
    except Exception as e:
        print(f"Error resetting database: {e}")

if __name__ == "__main__":
    reset_database()

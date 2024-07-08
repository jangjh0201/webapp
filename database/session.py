from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.config import DATABASE_URL

# MySQL 데이터베이스 연결 설정
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

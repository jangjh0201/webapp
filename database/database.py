import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# release
DATABASE_URL = os.getenv("DATABASE_URL")

# local
# DATABASE_URL = "mysql+pymysql://root:system@localhost:3306/ice_cream_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def create_tables():
    Base.metadata.create_all(bind=engine)


def initialize_tables():
    # 테이블 삭제
    Base.metadata.drop_all(bind=engine)
    # 테이블 생성
    Base.metadata.create_all(bind=engine)

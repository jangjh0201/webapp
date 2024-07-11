import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")
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

    metadata = MetaData(bind=engine)
    metadata.reflect()

    for table in metadata.sorted_tables:
        table.create(bind=engine, checkfirst=True)


# 데이터베이스 연결 설정 시 문자 집합과 정렬 방식 추가
def configure_database():
    with engine.connect() as conn:
        conn.execute(
            "ALTER DATABASE ice_cream_db CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;"
        )
        for table in Base.metadata.tables.values():
            conn.execute(
                f"ALTER TABLE {table.name} CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
            )

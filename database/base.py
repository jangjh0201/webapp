from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy ORM의 선언적(declarative) 매핑 API를 설정하는 데 사용되는 함수입니다. 
# 이 함수는 기본 클래스(Base)를 생성하며, 이 클래스를 상속받아 데이터베이스 테이블과 매핑되는 모델 클래스를 정의할 수 있습니다.
Base = declarative_base()

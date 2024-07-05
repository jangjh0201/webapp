from . import engine, Base
from .models import *

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

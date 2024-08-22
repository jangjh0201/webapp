from sqlalchemy.orm import Session
from database.crud.table import (
    create_table, 
    read_table_by_id,
    read_all_tables, 
    update_table_status, 
    delete_table_by_id,
    delete_all_tables
)
from error.error import (
    TableNotFoundException,    
    TableAlreadyInUseException, 
    TableInUseableException
)

def add_table(db: Session):
    """
    테이블 추가 함수
    Args:
        db: 데이터베이스 세션
    Returns:
        table: 추가된 테이블
    """
    table = create_table(db)
    return table
    
def get_table_by_id(table_id: int, db: Session):
    """
    특정 테이블 조회 함수
    Args:
        db: 데이터베이스 세션
        table_id: 테이블 아이디
    Returns:
        table: 특정 테이블
    """
    table = read_table_by_id(db, table_id)
    if not table:
        raise TableNotFoundException("테이블을 찾을 수 없습니다.")
    return table

def get_all_tables(db: Session):
    """
    모든 테이블 조회 함수
    Args:
        db: 데이터베이스 세션
    Returns:
        tables: 모든 테이블 리스트
    """
    tables = read_all_tables(db)
    
    tables_list = []
    for table in tables:
        tables_list.append({"id": table.id, "status": table.status})
    
    return tables_list
    
def edit_table_status(table_id: int, json_data : dict, db: Session):
    """
    테이블 상태 업데이트 함수
    Args:
        db: 데이터베이스 세션
        table_id: 테이블 아이디
    Returns:
        table: 업데이트된 테이블 리스트
    """
    request_status = json_data.get("status")
    
    # 테이블 조회
    table = get_table_by_id(db, table_id)

    # 테이블 상태가 사용가능(1)일 때,
    if table.status == 1: 
        # 사용요청(0)이 들어오면 사용중(0)으로 변경
        if request_status == 0:
            table = update_table_status(db, table, status=0)
            return get_all_tables(db)
        # 반환요청(1)이 들어오면 사용가능 에러 발생
        else:
            raise TableInUseableException("사용 가능한 테이블입니다.")
    # 테이블 상태가 사용중(0)일 때,
    else:
        # 반환요청(1)이 들어오면 사용가능(1)으로 변경
        if request_status == 1:
            table = update_table_status(db, table, status=1)
            return get_all_tables(db)
        # 사용요청(0)이 들어오면 이미 사용중 에러 발생
        else:
            raise TableAlreadyInUseException("이미 사용 중인 테이블입니다.")
    
def remove_table(table_id: int, db: Session):
    """
    특정 테이블 삭제 함수
    Args:
        db: 데이터베이스 세션
        table_id: 테이블 아이디
    Returns:
        table: 삭제된 테이블
    """
    table = delete_table_by_id(db, table_id)
    return table

def remove_all_tables(db: Session):
    """
    모든 테이블 삭제 함수
    Args:
        db: 데이터베이스 세션
    Returns:
        tables: 삭제된 테이블 리스트
    """
    tables = delete_all_tables(db)
    return tables
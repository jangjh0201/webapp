class TableAlreadyInUseException(Exception):
    """테이블이 이미 사용 중일 때 발생하는 예외"""
    pass

class TableInUseableException(Exception):
    """테이블이 사용 가능할 때 발생하는 예외"""
    pass

class TableNotFoundException(Exception):
    """데이터를 찾을 수 없을 때 발생하는 예외"""
    pass
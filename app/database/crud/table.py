from sqlalchemy.orm import Session
from models.models import Table


def create_table(db: Session):
    table = Table()
    db.add(table)
    db.commit()
    db.refresh(table)
    return table


def read_table_by_id(table_id: int, db: Session):
    return db.query(Table).filter(Table.id == table_id).first()

def read_all_tables(db: Session):
    return db.query(Table).all()

def update_table_status(
    db: Session,
    table: Table,
    status: int = None,
):
    table.status = status
    db.commit()
    db.refresh(table)
    return table

def delete_table_by_id(table_id: int, db: Session):
    table = db.query(Table).filter(Table.id == table_id).first()
    if table:
        db.delete(table)
        db.commit()
    return table


def delete_all_tables(db: Session):
    tables = db.query(Table).all()
    for table in tables:
        db.delete(table)
    db.commit()
    return tables

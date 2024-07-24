from sqlalchemy.orm import Session
from database.crud.robot_log import create_robot_log, read_all_robot_logs


def add_robot_log(json_data: dict, db: Session):
    status_body = json_data.get("OS", {})
    status = status_body.get("status")
    create_robot_log(db, status)


def get_all_logs(db: Session):
    logs = read_all_robot_logs(db)
    return logs

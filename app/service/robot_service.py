from sqlalchemy.orm import Session
from app.database.crud.robot_log import create_robot_log, read_all_robot_logs
from models.models import RobotLog


def add_robot_log(json_data: dict, db: Session):
    status_body = json_data.get("OS", {})
    status = status_body.get("status")
    robot_log = RobotLog(status=status)
    create_robot_log(robot_log)


def show_all_logs(db: Session):
    logs = read_all_robot_logs()
    return logs

from sqlalchemy.orm import Session
from models.models import RobotLog


def create_robot_log(db: Session, status: int):
    robot_log = RobotLog(status=status)
    db.add(robot_log)
    db.commit()
    db.refresh(robot_log)


def read_all_robot_logs(db: Session):
    return db.query(RobotLog).all()


def delete_robot_log(db: Session, order_id: int):
    robot_log = db.query(RobotLog).filter(RobotLog.id == order_id).first()
    if robot_log:
        db.delete(robot_log)
        db.commit()

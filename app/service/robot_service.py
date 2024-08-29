from sqlalchemy.orm import Session
from database.crud.robot_log import create_robot_log, read_all_robot_logs
import cv2
import socket

def add_robot_log(json_data: dict, db: Session):
    """
    로봇 로그 추가 함수
    Args:
        json_data: 로봇 로그 정보
        db: 데이터베이스 세션
    Returns:
        None
    """
    status_body = json_data.get("OS", {})
    status = status_body.get("status")
    create_robot_log(db, status)


def get_all_logs(db: Session):
    """
    모든 로봇 로그 조회 함수
    Args:
        db: 데이터베이스 세션
    Returns:
        logs: 모든 로봇 로그 리스트
    """
    logs = read_all_robot_logs(db)
    return logs


def get_robot_view():
    """
    로봇 카메라 피드 캡처 함수
    Returns:
        frame: 로봇 카메라 피드 프레임
    """
    cap = cv2.VideoCapture(0)
    try:
        while True:
            success, frame = cap.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode(".jpg", frame)
                frame = buffer.tobytes()
                yield (
                    b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
                )
    finally:
        cap.release()

def use_storagy(cmd):
    """
    스토리지 사용 함수
    Args:
        cmd: 스토리지 사용 명령어
    Returns:
        None
    """
    # TCP 소켓 설정
    server_ip = '192.168.0.7'  # 상대방 IP 주소
    server_port = 5001            # 상대방 포트 번호
    
    try:
        # 소켓 생성
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        #     # 서버에 연결
        #     sock.connect((server_ip, server_port))
            
        #     # 명령어 전송
        #     sock.sendall(cmd.encode('utf-8'))
            
        #     # 서버로부터 응답 수신 (옵션)
        #     response = sock.recv(1024).decode('utf-8')
        #     print(f"Server response: {response}")
        print(cmd)
    except ConnectionRefusedError:
        print("Connection refused. The server may be unavailable.")
    except Exception as e:
        print(f"An error occurred: {e}")

    
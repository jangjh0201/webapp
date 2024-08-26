from fastapi import APIRouter, Request, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from database.database import get_db
from service import order_service, robot_service, table_service
from error.error import TableAlreadyInUseException, TableInUseableException, TableNotFoundException

router = APIRouter()
templates = Jinja2Templates(directory="app/resource/templates")


@router.get("/")
def show_home(request: Request):
    """
    홈 페이지 반환 API
    Args:
        request: Request 객체
    Returns:
        홈 페이지 반환 (HTML)
    """
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/order")
def show_order(request: Request, db: Session = Depends(get_db)):
    """
    주문 페이지 반환 API
    Args:
        request: Request 객체
        db: 데이터베이스 세션
    Returns:
        주문 페이지 반환 (HTML)
    """
    ice_creams, toppings, consumables = order_service.get_all_orders(db)
    return templates.TemplateResponse(
        "order.html",
        {
            "request": request,
            "ice_creams": ice_creams,
            "toppings": toppings,
            "consumables": consumables,
        },
    )


@router.post("/order")
def add_order(
    request: Request,
    ice_cream_id: int = Form(...),
    topping_ids: str = Form(None),
    consumable_ids: str = Form(None),
    db: Session = Depends(get_db),
):
    """
    주문 추가 API
    Args:
        request: Request 객체
        ice_cream_id: 아이스크림 ID
        topping_ids: 토핑 ID 리스트
        consumable_ids: 소모품 ID 리스트
        db: 데이터베이스 세션
    Returns:
        주문 완료 시 메인 페이지로 리다이렉트
        주문 실패 시 400 에러 반환
    """
    try:
        order_service.add_order(ice_cream_id, topping_ids, consumable_ids, db)
        return templates.TemplateResponse(
            "index.html", {"request": request, "message": "주문이 완료되었습니다."}
        )
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})


@router.post("/kiosk")
async def add_order_by_kiosk(request: Request, db: Session = Depends(get_db)):
    """
    키오스크 주문 추가 API
    Args:
        request: Request 객체
        db: 데이터베이스 세션
    Returns:
        주문 완료 시 201 반환
        주문 실패 시 400 에러 반환
    """
    try:
        result = await order_service.add_order_by_kiosk(await request.json(), db)
        return JSONResponse(status_code=201, content={"OR": result})
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})


@router.post("/robot")
async def add_robot_log(request: Request, db: Session = Depends(get_db)):
    """
    로봇 로그 추가 API
    Args:
        request: Request 객체
        db: 데이터베이스 세션
    Returns:
        로그 저장 완료 시 201 반환
    """
    robot_service.add_robot_log(await request.json(), db)
    return JSONResponse(status_code=201, content={"message": "로그가 저장되었습니다."})

@router.post("/table")
def add_table(db: Session = Depends(get_db)):
    """
    테이블 추가 API
    Args:
        db: 데이터베이스 세션
    Returns:
        테이블 추가 완료 시 201 반환
    """
    table_service.add_table(db)
    return JSONResponse(status_code=201, content={"message": "테이블이 추가되었습니다."})

@router.get("/table")
def show_tables(db: Session = Depends(get_db)):
    """
    모든 테이블 조회 API
    Args:
        request: Request 객체
        db: 데이터베이스 세션
    Returns:
        테이블 리스트 반환
    """
    tables = table_service.get_all_tables(db)
    
    return JSONResponse(status_code=200, content=tables)


@router.get("/table/{table_id}")
def show_table_by_id(table_id: int, db: Session = Depends(get_db)):
    """
    특정 테이블 조회 API
    Args:
        table_id: 테이블 ID
        db: 데이터베이스 세션
    Returns:
        특정 테이블 반환
    """
    table = table_service.get_table_by_id(db, table_id)
    return JSONResponse(status_code=200, content=table)

@router.patch("/table/{table_id}")
async def change_table_status(table_id: int, request: Request, db: Session = Depends(get_db)):
    """
    테이블 사용 상태 변경 API
    Args:
        table_id: 테이블 ID
        db: 데이터베이스 세션
    Returns:
        테이블 사용 성공 시 200 반환
        테이블 사용 실패 시 400 에러 반환
        테이블을 찾을 수 없을 시 404 에러 반환
        서버 오류 발생 시 500 에러 반환
    """
    try:
        json_data = await request.json()
        request_data = json_data.get("request")
        tables = table_service.edit_table_status(table_id, request_data, db)
        return JSONResponse(status_code=200, content={"TR": tables})
    except TableNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TableInUseableException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except TableAlreadyInUseException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="서버 오류가 발생했습니다.")

@router.post("/test")
async def test_order(request: Request, db: Session = Depends(get_db)):
    """
    주문 추가 테스트 API
    Args:
        request: Request 객체
        db: 데이터베이스 세션
    Returns:
        주문 완료 시 201 반환
        주문 실패 시 400 에러 반환
    """
    try:
        json_data = await request.json()
        order_time = json_data.get("OR", {}).get("order_time")
        result = await order_service.add_order_by_kiosk(json_data, db)
        order_id = result["orderId"]
        order_service.edit_order_time(db, order_id, order_time)
        return JSONResponse(status_code=201, content={"orderId": order_id})
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

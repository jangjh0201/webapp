from fastapi import APIRouter, Request, Form, Depends, HTTPException, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from database.database import get_db
from auth.auth import manager, authenticate_user

router = APIRouter()
templates = Jinja2Templates(directory="app/resource/templates")


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/auth/token")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    access_token = manager.create_access_token(data={"sub": user.username})
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    manager.set_cookie(response, access_token)
    response.set_cookie(key="username", value=user.username)
    return response


@router.get("/logout")
async def logout(response: Response):
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access-token")
    response.delete_cookie(key="username")
    return response

from fastapi import APIRouter, Depends, status, Response, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from models.authorization import UserCreate, Token, User
from services.authorization import AuthService, get_current_user
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    prefix='/authorization',
    tags=['authorization'],
)

@router.post('/sign-up/', response_model=Token, status_code=status.HTTP_201_CREATED)
def sign_up(user_data: UserCreate, auth_service: AuthService = Depends()):
    """Регисртрация нового пользователя и сразу получение токена"""
    return auth_service.register_new_user(user_data)

@router.post('/sign-in/')
def sign_in(auth_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends()):
    """Получение токена (токен зранится в куки)"""
    token = auth_service.authenticate_user(auth_data.username, auth_data.password)
    content = {"message": "True"}
    response = JSONResponse(content=content)
    response.set_cookie("Authorization", value=f"Bearer {token.access_token}", samesite='none', httponly=True)

    return response


@router.get('/user/', response_model=User)
def get_user(user: User = Depends(get_current_user)):
    """Просмотр авторизованного пользователя"""
    return user


@router.get("/sign-out/")
def sign_out_and_remove_cookie(current_user: User = Depends(get_current_user)):
    # Also tried following two comment lines
    # response.set_cookie(key="access_token", value="", max_age=1)
    # response.delete_cookie("access_token", domain="localhost")
    content = {"message": "Tocken closed"}
    response = JSONResponse(content=content)
    response.delete_cookie("Authorization")
    return response


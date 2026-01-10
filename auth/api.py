from starlette.routing import Router
from .model import *
from .service import *

from fastapi import APIRouter,Depends,HTTPException,Request,Form

router = APIRouter(prefix="/auth",tags=["Authentication"])

#全局认证服务实例
auth_service = AuthService()


@router.post("/register",response_model=AuthResponse)
async def register(request: RegisterRequest):
    return await auth_service.register(request)

@router.post("/login",response_model=AuthResponse)
async def login(request: LoginRequest):
    return await auth_service.login(request)

@router.post("/refresh",response_model=RefreshResponse)
async def refresh(request: RefreshRequest):
    return await auth_service.refresh(request)

@router.get("/user",response_model=UserResponse)
async def get_user(user_id:str):
    return await auth_service.get_user(user_id)

@router.post("/logout")
async def logout(user_id:str):
    return await auth_service.logout(user_id)

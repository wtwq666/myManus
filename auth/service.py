import json
from datetime import datetime
from typing import Optional
from fastapi import HTTPException,Request
from .model import *

class AuthService:
    def __init__(self):
        self.token_store = {}

    async def register(self, request: RegisterRequest)->AuthResponse:
        return AuthResponse(
            access_token="register_token",
            refresh_token="register_refresh_token",
            expires_in=3600,
            user=User(
                id="test_id",
                email=request.email,
                name=request.name,
                created_at=datetime.now()
            )
        )
        
    async def login(self, request: LoginRequest)->AuthResponse:
        return AuthResponse(
            access_token="login_token",
            refresh_token="login_refresh_token",
            expires_in=3600,
            user=User(
                id="test_id",
                email=request.email,
                name="test_user",
                created_at=datetime.now()
            )
        )
    
    async def refresh(self, request: RefreshRequest)->RefreshResponse:
        return RefreshResponse(
            access_token="refresh_token",
            refresh_token="refresh_refresh_token",
            expires_in=3600
        )   
    
    async def get_user(self, user_id:str)->UserResponse:
        print("get_user")
        return UserResponse(
            user=User(
                id=user_id,
                email="test@example.com",
                name="testuser",
                created_at=datetime.now()
            )
        )

    async def logout(self, user_id:str)->None:
        print("logout")
        return None

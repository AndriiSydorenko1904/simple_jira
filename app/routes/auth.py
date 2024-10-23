from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.utils import create_access_token, verify_password
from app.schemas import Token
from app.config import TOKEN_TYPE, ACCESS_TOKEN_EXPIRE_MINUTES


auth_router = APIRouter()


@cbv(auth_router)
class Auth:
    db: Session = Depends(get_db)

    @auth_router.post("/token/", response_model=Token)
    def token(self, form_data: OAuth2PasswordRequestForm = Depends()):
        user = self.db.query(User).filter(User.username == form_data.username).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": TOKEN_TYPE.title()},
            )
    
        if not verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": TOKEN_TYPE.title()},
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": TOKEN_TYPE}

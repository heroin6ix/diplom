from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db
from .. import models, schemas
from ..core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):

    db_user = (
        db.query(models.User).filter(models.User.email == form_data.username).first()
    )

    if not db_user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    if not verify_password(form_data.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Неверный пароль")

    token = create_access_token(
        {"sub": str(db_user.id), "email": db_user.email, "role": db_user.role_id}
    )

    return {"access_token": token, "token_type": "bearer"}

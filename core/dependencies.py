from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from .security import SECRET_KEY, ALGORITHM
from ..database import get_db
from .. import models
from sqlalchemy.orm import Session

oath2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Нет токена")
    try:
        token = authorization.split(" ")[1]
    except:
        raise HTTPException(status_code=401, detail="Неверный формат токена")


# def get_current_user(token: str = Depends(oath2_scheme), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Не удалось проверить токен",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     try:
#         paylaod = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id: str = paylaod.get("sub")
#         if user_id is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = db.query(models.User).filter(models.User.Id == int(user_id)).first()
#     if user is None:
#         raise credentials_exception
#     return user

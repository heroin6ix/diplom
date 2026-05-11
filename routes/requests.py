from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..core.dependencies import get_current_user

router = APIRouter(prefix="/requests", tags=["Requests"])


# Создание заявки
@router.post("/", response_model=schemas.RequestResponse)
def create_request(
    request_data: schemas.RequestCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Получаем статус "Новая"
    new_status = (
        db.query(models.RequestStatus)
        .filter(models.RequestStatus.name == "Новая")
        .first()
    )

    # Если статуса нет
    if not new_status:
        raise HTTPException(status_code=500, detail="Статус 'Новая' не найден.")

    # Создаем ORM объект
    new_request = models.Request(
        user_id=current_user.id,
        description=request_data.description,
        device_type=request_data.device_type,
        device_model=request_data.device_model,
        serial_number=request_data.serial_number,
        status_id=new_status.id,
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request


# Получить все заявки
@router.get("/", response_model=list[schemas.RequestResponse])
def get_requests(
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    requests = db.query(models.Request).all()
    return requests


# Получить одну заявку
@router.get("/{request_id}", response_model=schemas.RequestResponse)
def get_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    request = db.query(models.Request).filter(models.Request.id == request_id).first()

    if not request:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    return request


# Обновление заявки
@router.put("/{request_id}", response_model=schemas.RequestResponse)
def update_request(
    request_id: int,
    request_data: schemas.RequestUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    request = db.query(models.Request).filter(models.Request.id == request_id).first()

    if not request:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    # Обновление только переданных полей
    update_data = request_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(request, key, value)
    db.commit()
    db.refresh(request)
    return request


# Удаление заявки
@router.delete("/{request_id}")
def delete_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    request = db.query(models.Request).filter(models.Request.id == request_id).first()

    if not request:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    db.delete(request)
    db.commit()
    return {"message": "Заявка удалена"}

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config.database import Sessionlocal
from config.models import User
from config.schema import UserSignUPModel, UserSignUpResponse

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

auth_router = APIRouter(prefix="/auth", tags=["auth"])


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


@auth_router.post(
    "/signup",
    response_model=UserSignUpResponse,
    status_code=status.HTTP_201_CREATED,
)
def signup(data: UserSignUPModel, db: Session = Depends(get_db)):
    email = data.email.lower() if data.email else None

    conditions = [User.username == data.username]
    if email:
        conditions.append(User.email == email)
    if data.phone_number:
        conditions.append(User.phone_number == data.phone_number)

    if db.query(User).filter(or_(*conditions)).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bunday username, email yoki telefon raqamli foydalanuvchi mavjud",
        )

    new_user = User(
        username=data.username,
        email=email,
        full_name=data.full_name,
        phone_number=data.phone_number,
        password=pwd_context.hash(data.password),  # modelda hashed_password bo'lsa, shunga o'zgartiring
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()  # parallel so'rovlarda ham unique buzilishi mumkin
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Foydalanuvchi allaqachon mavjud",
        )
    except Exception:
        db.rollback()
        logger.exception("Signup xatosi")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return new_user
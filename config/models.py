
from database import Base
from sqlalchemy import Text, Column, Integer , String, ForeignKey, Boolean , DateTime, func , Numeric, Date
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True )
    username = Column(String(40),unique=True,nullable=False)
    email = Column(String(40),unique=True)
    phone_number = Column(String(20),unique=True)
    password = Column(Text, nullable=False)
    is_staff = Column(Boolean, default=False)
    is_active= Column(Boolean, default=False) 
    given_debts = relationship('Qarz',foreign_keys='Qarz.user_to_id', back_populates='user_to') #bergan 
    received_debts = relationship('Qarz',foreign_keys='Qarz.user_by_id',back_populates='user_by') #olgan

    @property
    def berilgan(self):
        return self.given_debts

    @property
    def olingan(self):
        return self.received_debts

    def __repr__(self):
        return f"user >> {self.username}"


class Qarz(Base):
    __tablename__ = "qarzlar"

    VALYUTA_TURI = [
        ("UZS", "uzs"),
        ("USD", "usd"),
    ]

    id = Column(Integer, primary_key=True, index=True)

    
    user_to_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False     # Qarz bergan foydalanuvchi
    )

    
    user_by_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )       # Qarz olgan foydalanuvchi

    miqdor = Column(Numeric(14, 2), nullable=False)

    valyuta = Column(
        ChoiceType(VALYUTA_TURI),
        default="UZS",
        nullable=False
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    qaytarish_muddati = Column(Date, nullable=False)

    description = Column(Text, nullable=True)

    user_to = relationship(
        "User",
        foreign_keys=[user_to_id],
        back_populates="given_debts"
    )

    user_by = relationship(
        "User",
        foreign_keys=[user_by_id],
        back_populates="received_debts"
    )

    

    def __repr__(self):
        return (
            f"Qarz(id={self.id}, "
            f"beruvchi={self.user_to_id}, "
            f"oluvchi={self.user_by_id}, "
            f"miqdor={self.miqdor} {self.valyuta})"
        )
    

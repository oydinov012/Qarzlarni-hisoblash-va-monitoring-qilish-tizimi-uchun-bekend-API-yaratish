
from database import Base
from sqlalchemy import Text, Column, Integer , String, ForeignKey, Boolean , DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True )
    username = Column(String(40),unique=True)
    email = Column(String(40),unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active= Column(Boolean, default=False)


    def __repr__(self):
        return f"user >> {self.username}"


class Qarz(Base):
    __tablename__ = "oldi-berdi"
    VALYUTA_TURI = (
        ("UZS",'uzs'),
        ("USD",'usd')
    )
    id = Column(Integer,primary_key=True)
    user_to_id = Column(Integer, ForeignKey(User.id))  #berilgan
    user_by_id = Column(Integer,ForeignKey(User.id))   #olingan
    miqdor = Column(Integer)
    valyuta = Column(ChoiceType(choices=VALYUTA_TURI),default="UZS")
    created_at =  Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updeated_at =  Column(DateTime(timezone=True),server_default=func.now(),onupdate=True,nullable=False)
    muddat = Column(Integer)

    description = Column(Text) 

    def __repr__(self):
        return f"{self.user_by_id} <<-->> {self.user_to_id} oldi berdi"


    

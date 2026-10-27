from pydantic import BaseModel, ConfigDict



class UserSignUPModel(BaseModel):
    id : int | None = None
    username : str
    email : str
    full_name :str | None=None
    phone_number : str
    password : str 
    two_password: str 
    

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example":{
                "username":"Username",
                "email":"email@gmail.com",
                "full_name":"userfullname",
                "phone_number":"+99897654321",
                "is_staff":False
            }
        }
    )


class QarzModel(BaseModel):
    pass


from datetime import datetime
from pydantic import BaseModel, ConfigDict

class UserSignUpResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Pydantic v1 bo'lsa: class Config: orm_mode = True

    id: int
    username: str
    full_name: str | None = None
    phone_number: str | None = None
    is_active: bool
    created_at: datetime
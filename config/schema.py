from pydantic import BaseModel, ConfigDict



class UserModel(BaseModel):
    id : int | None = None
    username : str
    email : str
    phone_number : str
    password : str 
    is_activ : bool | None = False

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example":{
                "username":"Username",
                "email":"email@gmail.com",
                "phone_number":"+99897654321",
                "is_staff":False
            }
        }
    )


class QarzModel(BaseModel):
    pass
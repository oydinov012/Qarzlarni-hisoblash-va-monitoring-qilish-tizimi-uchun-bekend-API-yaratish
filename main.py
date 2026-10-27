from fastapi import FastAPI
import uvicorn
from config.schema_settings import Settings
from config import locals
from async_fastapi_jwt_auth import AuthJWT
from router.auth import user_auth

@AuthJWT.load_config # type: ignore
def get_config():
    return Settings()

app = FastAPI()
app.include_router(user_auth.auth_router)


@app.get('/')
async def salom():
    return {
        "message":"FastAPI loyihasiga xush kelibsiz",
        "data":[
            {
                "ism":"kimdir",
                "familiya":"nimadir",
                "email":None
            }
        ]
            }



if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=locals.PORT,
        host=locals.HOST,
        reload=locals.RELOAD
    )
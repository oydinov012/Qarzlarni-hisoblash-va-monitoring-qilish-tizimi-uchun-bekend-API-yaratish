from database import Base, engine
from models  import User, Qarz 

def init_db():
    print('modellar yaratilmoda')
    Base.metadata.create_all(bind=engine)
    print('modellar yaratildi')


if __name__ == "__main__":
    init_db()

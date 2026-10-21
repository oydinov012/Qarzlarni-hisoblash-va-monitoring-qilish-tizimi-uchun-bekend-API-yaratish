from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base , sessionmaker

db_owner = 'ilyos'
password = 1234
db_name = 'qarzlar'
engine = create_engine(f"postgresql://{db_owner}:{password}@localhost/{db_name}",echo=True)



Base = declarative_base()

Sessionlocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False)
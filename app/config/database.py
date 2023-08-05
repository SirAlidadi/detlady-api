from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


SQLALCHEMY_DATABASE_URL = "mysql://root:@localhost:3306/detlady"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()
local_session = sessionmaker(bind=engine)

def get_db():
    session = local_session()
    try:
        yield session
    finally:
        session.close()

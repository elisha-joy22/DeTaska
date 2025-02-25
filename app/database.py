from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "postgresql://username:password@localhost/detaska"

engine = create_engine(url=DATABASE_URL, echo= True)

def get_session():
    with Session(engine) as session:
        yield session
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from system.config import settings

engine = create_engine(settings.POSTGRES_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
metadata = MetaData(engine)
test_db_engine = create_engine(settings.POSTGRES_DATABASE_URL + "_test", echo=True)
TestDbSessionLocal = sessionmaker(bind=test_db_engine)


def get_db():
    db = SessionLocal()
    db.begin()
    try:
        yield db
    except Exception as e:
        db.rollback()
        db.close()
        raise e
    finally:
        db.commit()
        db.close()


def get_db_without_commit():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        db.close()
        raise e
    finally:
        db.close()

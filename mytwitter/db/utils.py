import contextlib
import functools

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from mytwitter import constants

engine = create_engine(constants.db_url, echo=True)

SessionClass = sessionmaker(bind=engine, expire_on_commit=False)

@contextlib.contextmanager
def get_temp_session():
    try:
        session = SessionClass()
        yield session
    finally:
        session.commit()
        session.close()

def ensure_session(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        session = kwargs.pop('session', None)
        if not session:
            with get_temp_session() as session:
                kwargs['session'] = session
                return f(*args, **kwargs)
        else:
            kwargs['session'] = session
            return f(*args, **kwargs)
    return wrapper

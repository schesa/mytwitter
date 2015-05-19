from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from mytwitter.db import utils


class BaseModel(object):
    id = Column(Integer, primary_key=True)

    def save():
        session = utils.get_new_session()
        with session.begin():
            session.add(self)

    def _to_dict(self):
        _dict = {col.name: getattr(self, col.name)
                 for col in self.__table__.columns}
        return _dict


DeclarativeBase = declarative_base(cls=BaseModel)


def ModelJsonEncoder(obj):
    if isinstance(obj, BaseModel):
        return obj._to_dict()
    else:
        return json.dumps(obj)

class User(DeclarativeBase):
    __tablename__ = 'users'

    name = Column(String(32))

    def __str__(self):
        return 'User: Name: %s' % self.name

    def __repr__(self):
        return str(self)


class Tweet(DeclarativeBase):
    __tablename__ = 'tweets'

    message = Column(String(255))
    user_id = Column(ForeignKey('users.id'))

    user = relationship("User", backref=backref('tweets'), order_by='User.id')

    def __str__(self):
        return '%(user)s: %(message)s' % {'user': self.user.name,
                                          'message': self.message}

    def __repr__(self):
        return str(self)

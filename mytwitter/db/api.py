from sqlalchemy.orm import joinedload

from mytwitter.db import models
from mytwitter.db import session as session_utils


def initialize():
    session_utils.initialize()


def create_tables():
    models.BaseModel.metadata.create_all(session_utils.engine)


@session_utils.ensure_session
def add_user(name, session=None):
    user = models.User(name=name)
    return user.save()


@session_utils.ensure_session
def add_tweet(user_id, message, session=None):
    tweet = models.Tweet(message=message, user_id=user_id)
    return tweet.save()


@session_utils.ensure_session
def get_users(session=None):
    query = session.query(models.User).\
        options(joinedload(models.User.tweets))
    # You shouldn't use a joinedload in such situations.
    # Alternative syntax:
    # options(joinedload('tweets.user'))
    return query.order_by(models.User.id).all()


@session_utils.ensure_session
def get_user(user_id=None, session=None):
    query = session.query(models.User)
    return query.filter_by(id=user_id).one()


@session_utils.ensure_session
def get_tweets(user_id=None, session=None):
    query = session.query(models.Tweet).options(
                    joinedload(models.Tweet.user))
    if user_id:
        query.filter_by(id=user_id)
    return query.order_by(models.Tweet.id).all()

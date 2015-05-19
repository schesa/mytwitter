from mytwitter import constants
from mytwitter.db import models
from mytwitter.db import utils

from sqlalchemy.orm import subqueryload, joinedload


def create_tables():
    models.DeclarativeBase.metadata.create_all(utils.engine)


@utils.ensure_session
def add_user(name, session=None):
    user = models.User(name=name)
    session.add(user)


@utils.ensure_session
def add_tweet(user_id, message, session=None):
    tweet = models.Tweet(message=message, user_id=user_id)
    session.add(tweet)


@utils.ensure_session
def get_users(session=None):
    query = session.query(models.User).\
        options(joinedload(models.User.tweets)).\
        options(joinedload('tweets.user'))
    return query.order_by(models.User.id).all()


@utils.ensure_session
def get_user(user_id=None, session=None):
    query = session.query(models.User).options(joinedload(models.User.tweets))
    return query.filter_by(id=user_id).one()


@utils.ensure_session
def get_tweets(user_id=None, session=None):
    query = session.query(models.Tweet).options(
                    joinedload(models.Tweet.user))
    if user_id:
        query.filter_by(id=user_id)
    return query.order_by(models.Tweet.id).all()

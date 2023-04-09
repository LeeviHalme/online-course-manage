from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv

db = SQLAlchemy()

# helper to make text-based queries using SQLAlchemy
# returns the query object
def make_query(query: str, params={}):
    if getenv("FLASK_DEBUG"):
        print(query, "-", params)

    return db.session.execute(text(query), params)


# helper to make text-based INSERT queries
# using SQLAlchemy. Returns the query object
def make_insert(query: str, params={}):
    if getenv("FLASK_DEBUG"):
        print(query, "-", params)

    query = db.session.execute(text(query), params)
    db.session.commit()

    return query


# helper to serialize SQLAlchemy Row object
# into a python dict
def serialize_to_dict(row):
    return dict(row._mapping)

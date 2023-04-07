from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

db = SQLAlchemy()

# helper to make text-based queries using SQLAlchemy
# returns the query object
def make_query(query: str, params={}):
    print("query", query, "params", params)

    return db.session.execute(text(query), params)

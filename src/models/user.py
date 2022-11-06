from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.orm.session import Session

from src.models.db import BaseDatabase, database


class User(BaseDatabase):
    __tablename__ = 'user'
    name = Column(String)
    UniqueConstraint(name)

    @staticmethod
    def get_or_create(name) -> Session:
        session = database.connect_db()
        row = session.query(User).filter(User.name == name).first()
        if row:
            session.close()
            # return exsiting data
            return row

        user = User(name=name)
        session.add(user)
        session.commit()
        session.close()

        # return user data including ID
        row = session.query(User).filter(User.name == name).first()
        session.close()
        return row

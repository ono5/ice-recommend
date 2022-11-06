from typing import Union

from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.orm.session import Session

from src.models.db import BaseDatabase, database


class IceCream(BaseDatabase):
    __tablename__ = 'icecream'
    name = Column(String)
    UniqueConstraint(name)

    @staticmethod
    def get(icecream_id: int) -> Union[Session, None]:
        session = database.connect_db()
        row = session.query(IceCream).filter(
            IceCream.id == icecream_id).first()
        if row:
            session.close()
            return row
        return None

    @staticmethod
    def get_or_create(name: str) -> Session:
        session = database.connect_db()
        row = session.query(IceCream).filter(IceCream.name == name).first()
        if row:
            session.close()
            # return exsiting data
            return row

        icrecream = IceCream(name=name)
        session.add(icrecream)
        session.commit()
        session.close()

        # return icrecream data including ID
        row = session.query(IceCream).filter(IceCream.name == name).first()
        session.close()
        return row

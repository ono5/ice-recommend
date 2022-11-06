import random
from typing import Union, List

from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.orm.session import Session

from models.db import BaseDatabase, database


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

    @staticmethod
    def get_icecream_random() -> List[str]:
        session = database.connect_db()
        icecreams = session.query(IceCream).all()
        icecream_list = []
        for ice in icecreams:
            icecream_list.append(ice.name)

        select_icecream_list = []
        # 5個のランダムなアイスを返す
        random_list = [random.randint(0, len(icecream_list)-1) for i in range(5)]
        for r in random_list:
            select_icecream_list.append(icecream_list[r])

        session.close()

        return select_icecream_list





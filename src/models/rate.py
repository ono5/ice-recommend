import logging

import pandas as pd
from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from surprise import SVD, Dataset, NormalPredictor, Reader
from surprise.model_selection import cross_validate

import settings
from models.db import BaseDatabase, database
from models.icecream import IceCream
from models.user import User

logger = logging.getLogger(__name__)


class Rate(BaseDatabase):
    __tablename__ = 'rate'
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"))
    icecream_id = Column(ForeignKey("icecream.id", ondelete="CASCADE"))
    value = Column(Integer)
    UniqueConstraint(user_id, icecream_id)

    @staticmethod
    def update_or_create(user: User, icecream: IceCream, value: int) -> None:
        session = database.connect_db()
        rate = session.query(Rate).filter(
            Rate.user_id == user.id, Rate.icecream_id == icecream.id).first()
        if rate:
            rate.value = value
            session.add(rate)
            session.commit()
            session.close()
            # これがないと下の処理が進み、Insert into エラーが発生してしまうので注意
            return rate

        rate = Rate(user_id=user.id, icecream_id=icecream.id, value=value)
        session.add(rate)
        session.commit()
        session.close()

    @staticmethod
    def recommend_icecream(user: User) -> list:
        if not settings.RECOMMEND_ENGINE_ENABLE:
            session = database.connect_db()
            recommend = [r.name for r in session.query(
                IceCream).all()][:settings.RECCOMEND_ICECREAM_NUM]
            session.close()
            return recommend

        # -------------------------データ作成
        session = database.connect_db()
        # sql -> pandasのデータフレームに変更
        df = pd.read_sql(
            "SELECT user_id, icecream_id, value from rate;", session.bind)
        session.close()

        dataset_colums = ["user_id", "icecream_id", "value"]
        reader = Reader()
        data = Dataset.load_from_df(df[dataset_colums], reader)

        # -------------------------検証
        try:
            # データを評価する
            cross_validate(NormalPredictor(), data, cv=5)
        except ValueError as ex:
            logger.error({"action": "recommend_icecream", "error": ex})
            return None

        # ------------------------アルゴリズム生成
        # トレーニング
        # 機械学習のアルゴリズム
        svd = SVD()
        trainset = data.build_full_trainset()
        svd.fit(trainset)

        # ------------------------予測
        predict_df = df.copy()
        item_id = "icecream_id"
        # 新しいカラムを作成
        predict_df["Predicted_Score"] = predict_df[item_id].apply(
            lambda x: svd.predict(user.id, x).est)
        # scoreの良いもの順にsort
        predict_df = predict_df.sort_values(
            by=["Predicted_Score"], ascending=False)
        # 重複データの削除
        predict_df = predict_df.drop_duplicates(subset=item_id)

        if predict_df is None:
            logger.warning({"action": "recommend_restaurant",
                           "status": "no predict data"})
            return []

        # ------------------------結果をリストにして返す
        recommended_icecreams = []
        for i, row in predict_df.iterrows():
            icecream_id = int(row["icecream_id"])
            icecream = IceCream.get(icecream_id)
            recommended_icecreams.append(icecream.name)

        return recommended_icecreams[:settings.RECCOMEND_ICECREAM_NUM]

import os
from datetime import datetime

import numpy as np
import pandas as pd

from sqlalchemy.orm import Session


class Score:
    def __init__(self):
        dirname = os.path.dirname(__file__)
        self._df = pd.read_csv(dirname + '/../base_data/cs_atts.csv')

    def user_credit_score(self, db: Session, user_id: int):
        from user import UserService
        user_sr = UserService()

        user_info = user_sr.user.find_item_multi(
            id=user_id,
            db=db
        )[0]
        age = int(datetime.now().year - user_info.birth_date.year)
        return self._calc_score_by_info(age=age)

    def _calc_score_by_info(self, age: int, gender: str = None, marital: str = None, degree: str = None):
        person = {
            'age': age,
            # 'gender': gender,
            # 'marital': marital,
            # 'degree': degree
        }
        risk_list = []
        for attribute, value in person.items():
            risk = self.__risk_finder(
                df=self._df,
                attribute=attribute,
                value=value,
                is_interval=isinstance(value, int))
            risk_list.append(risk)
        return self.__score(risk_list)

    @staticmethod
    def __strip_and_split(df):
        df = df['value']
        df = df.str.replace(' ', '')
        df = df.str.split(',')
        return df

    def __risk_finder(self, df, attribute, value, is_interval):
        df = df[df['attribute'] == attribute].reset_index()
        if is_interval:
            interval = self.__strip_and_split(df)
            df[['start', 'end']] = interval.to_list()
            start_mask = (value >= df['start'].astype(int))
            end_mask = (value <= df['end'].astype(int))
            risk = df[start_mask & end_mask].risk.tolist()[0]
        else:
            mask = (df['value'] == value)
            risk = df[mask].risk.tolist()[0]
        return risk

    @staticmethod
    def __score(risk_list):
        score_list = [1 - risk for risk in risk_list]
        score = np.average(score_list)
        return np.round(score, 3)


score_agent = Score()

from pydantic.types import PositiveFloat
from sqlalchemy.orm import Session

from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase
from ..exceptions.crypto_transaction import UserBalanceIsNotEnough
from ..models.crypto_transaction import UasCryptoTransaction, crypto_transaction_crud, GetMultiCryptoTransaction, \
    CreateCryptoTransaction, UpdateCryptoTransaction


class UasCryptoTransactionInterface(InterfaceBase):

    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        self.crud = crypto_transaction_crud

    def increase_balance(
            self,
            user_id: int,
            coin_name: str,
            input_type: str,
            input_unique_id: int,
            amount: int,
            db: Session,
    ) -> UasCryptoTransaction:
        try:
            amount = abs(amount)

            return self.add_item(
                db=db,
                user_id=user_id,
                coin_name=coin_name,
                input_type=input_type,
                input_unique_id=input_unique_id,
                type='increase',
                amount=amount
            )

        except Exception as e:
            db.rollback()
            raise e

    def block_balance(
            self,
            user_id: int,
            coin_name: str,
            input_type: str,
            input_unique_id: int,
            amount: PositiveFloat,
            db: Session,
    ) -> UasCryptoTransaction:
        try:
            amount = abs(amount)
            balance = self.get_balance(db=db, user_id=user_id, coin_name=coin_name)
            if balance - amount < 0:
                raise SystemError("User balance is less than block_amount")
            return self.add_item(
                db=db,
                user_id=user_id,
                coin_name=coin_name,
                input_type=input_type,
                input_unique_id=input_unique_id,
                type='block',
                amount=-amount
            )

        except Exception as e:
            db.rollback()
            raise e

    def unblock_balance(
            self,
            user_id: int,
            coin_name: str,
            input_type: str,
            input_unique_id: int,
            amount: PositiveFloat,
            db: Session,
    ) -> UasCryptoTransaction:
        try:
            amount = abs(amount)
            blocked_amount = self.get_blocked(db=db, user_id=user_id, coin_name=coin_name)
            if blocked_amount - amount < 0:
                raise SystemError("User blocked_amount is not enough")
            return self.add_item(
                db=db,
                user_id=user_id,
                coin_name=coin_name,
                input_type=input_type,
                input_unique_id=input_unique_id,
                type='unblock',
                amount=amount
            )

        except Exception as e:
            db.rollback()
            raise e

    def decrease_balance(
            self,
            user_id: int,
            coin_name: str,
            input_type: str,
            input_unique_id: int,
            amount: PositiveFloat,
            db: Session,
    ) -> UasCryptoTransaction:
        try:
            amount = abs(amount)
            blocked_amount = self.get_blocked(
                db=db,
                user_id=user_id,
                coin_name=coin_name
            )
            if blocked_amount - amount < 0:
                raise SystemError("Blocked amount is not enough to decrease")
            self.unblock_balance(
                db=db,
                user_id=user_id,
                coin_name=coin_name,
                amount=amount,
                input_type=input_type,
                input_unique_id=input_unique_id
            )
            return self.add_item(
                db=db,
                user_id=user_id,
                coin_name=coin_name,
                input_type=input_type,
                input_unique_id=input_unique_id,
                type='decrease',
                amount=-amount
            )

        except Exception as e:
            db.rollback()
            raise e

    def freeze_balance(
            self,
            user_id: int,
            coin_name: str,
            input_type: str,
            input_unique_id: int,
            amount: PositiveFloat,
            db: Session,
    ) -> UasCryptoTransaction:
        amount = abs(amount)
        blocked_amount = self.get_blocked(
            db=db,
            user_id=user_id,
            coin_name=coin_name
        )
        if blocked_amount - amount < 0:
            raise SystemError("Blocked amount is not enough to freeze")
        self.unblock_balance(
            db=db,
            user_id=user_id,
            coin_name=coin_name,
            amount=amount,
            input_type=input_type,
            input_unique_id=input_unique_id
        )
        return self.add_item(
            db=db,
            user_id=user_id,
            coin_name=coin_name,
            input_type=input_type,
            input_unique_id=input_unique_id,
            type='freeze',
            amount=-amount
        )

    def unfreeze_balance(
            self,
            user_id: int,
            coin_name: str,
            input_type: str,
            input_unique_id: int,
            amount: PositiveFloat,
            db: Session,
    ) -> UasCryptoTransaction:
        amount = abs(amount)
        froze_amount = self.get_froze(
            db=db,
            user_id=user_id,
            coin_name=coin_name
        )
        if froze_amount - amount < 0:
            raise SystemError("Froze amount is not enough to unfreeze")
        return self.add_item(
            db=db,
            user_id=user_id,
            coin_name=coin_name,
            input_type=input_type,
            input_unique_id=input_unique_id,
            type='unfreeze',
            amount=amount
        )

    def get_balance(
            self,
            db: Session,
            user_id: int,
            coin_name: str
    ):
        from sqlalchemy.sql import func
        coin_balance = db.query(func.sum(self.crud.model.amount).filter(
            self.crud.model.user_id == user_id, self.crud.model.coin_name == coin_name)
        ).first()[0]
        if coin_balance == 0 or not coin_balance:
            return 0
        else:
            return coin_balance

    def get_blocked(
            self,
            db: Session,
            user_id: int,
            coin_name: str
    ):
        from sqlalchemy.sql import func

        blocked_balance = db.query(func.sum(self.crud.model.amount).filter(
            ((self.crud.model.user_id == user_id) & (self.crud.model.coin_name == coin_name) & (
                    (self.crud.model.type == 'block') | (self.crud.model.type == 'unblock'))))
        ).first()[0]
        if blocked_balance == 0 or not blocked_balance:
            return 0
        else:
            return abs(blocked_balance)

    def get_froze(
            self,
            db: Session,
            user_id: int,
            coin_name: str
    ):
        from sqlalchemy.sql import func

        froze_balance = db.query(func.sum(self.crud.model.amount).filter(
            ((self.crud.model.user_id == user_id) & (self.crud.model.coin_name == coin_name) & (
                    (self.crud.model.type == 'freeze') | (self.crud.model.type == 'unfreeze'))))
        ).first()[0]
        if froze_balance == 0 or not froze_balance:
            return 0
        else:
            return abs(froze_balance)

    def find_blocked_coins(
            self,
            db: Session,
            input_type: str,
            input_unique_id: int,
    ):

        from sqlalchemy.sql import func
        result = db.query(self.crud.model.coin_name, func.sum(self.crud.model.amount)).filter(
            ((self.crud.model.input_type == input_type) & (self.crud.model.input_unique_id == input_unique_id)) &
            ((self.crud.model.type == 'block') | (self.crud.model.type == 'unblock'))
        ).group_by(self.crud.model.coin_name).all()

        dd = {}
        for tpl in result:
            dd.update({tpl[0]: abs(tpl[1])})
        return dd

    def check_user_enough_balance(self, db: Session, amount: float, user_id: int, coin: str):
        user_balance = self.get_balance(
            db=db,
            user_id=user_id,
            coin_name=coin
        )
        if user_balance < amount:
            raise UserBalanceIsNotEnough


crypto_transaction_agent = UasCryptoTransactionInterface(
    crud=crypto_transaction_crud,
    create_schema=CreateCryptoTransaction,
    update_schema=UpdateCryptoTransaction,
    get_multi_schema=GetMultiCryptoTransaction
)

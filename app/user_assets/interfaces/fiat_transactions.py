from pydantic.types import PositiveFloat
from sqlalchemy.orm import Session

from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase
from ..exceptions.crypto_transaction import UserBalanceIsNotEnough
from ..models.crypto_transaction import UasCryptoTransaction
from ..models.fiat_transaction import fiat_transaction_crud, UasFiatTransaction
from ..models.schemas.fiat_transaction import CreateFiatTransaction, UpdateFiatTransaction, GetMultiFiatTransaction


class FiatWalletInterface(InterfaceBase):
    """
        This interface works based on Safe_deletion
    """

    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        self.__crud = fiat_transaction_crud

    def increase_balance(
            self,
            user_id: int,
            input_type: str,
            input_unique_id: int,
            amount: int,
            db: Session,
    ) -> UasFiatTransaction:
        try:
            amount = abs(amount)

            return self.add_item(
                db=db,
                user_id=user_id,
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
            input_type: str,
            input_unique_id: int,
            amount: PositiveFloat,
            db: Session,
    ) -> UasCryptoTransaction:
        try:
            amount = abs(amount)
            balance = self.get_balance(db=db, user_id=user_id)
            if balance - amount < 0:
                raise SystemError("User balance is less than block_amount")
            return self.add_item(
                db=db,
                user_id=user_id,
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
            input_type: str,
            input_unique_id: int,
            amount: PositiveFloat,
            db: Session,
    ) -> UasCryptoTransaction:
        try:
            amount = abs(amount)
            blocked_amount = self.get_blocked(db=db, user_id=user_id)
            if blocked_amount - amount < 0:
                raise SystemError("User blocked_amount is not enough")
            return self.add_item(
                db=db,
                user_id=user_id,
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
            )
            if blocked_amount - amount < 0:
                raise SystemError("Blocked amount is not enough to decrease")
            self.unblock_balance(
                db=db,
                user_id=user_id,
                amount=amount,
                input_type=input_type,
                input_unique_id=input_unique_id
            )
            return self.add_item(
                db=db,
                user_id=user_id,
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
            input_type: str,
            input_unique_id: int,
            amount: PositiveFloat,
            db: Session,
    ) -> UasCryptoTransaction:
        amount = abs(amount)
        blocked_amount = self.get_blocked(
            db=db,
            user_id=user_id,
        )
        if blocked_amount - amount < 0:
            raise SystemError("Blocked amount is not enough to freeze")
        self.unblock_balance(
            db=db,
            user_id=user_id,
            amount=amount,
            input_type=input_type,
            input_unique_id=input_unique_id
        )
        return self.add_item(
            db=db,
            user_id=user_id,
            input_type=input_type,
            input_unique_id=input_unique_id,
            type='freeze',
            amount=-amount
        )

    def unfreeze_balance(
            self,
            user_id: int,
            input_type: str,
            input_unique_id: int,
            amount: PositiveFloat,
            db: Session,
    ) -> UasCryptoTransaction:
        amount = abs(amount)
        froze_amount = self.get_froze(
            db=db,
            user_id=user_id,
        )
        if froze_amount - amount < 0:
            raise SystemError("Froze amount is not enough to unfreeze")
        return self.add_item(
            db=db,
            user_id=user_id,
            input_type=input_type,
            input_unique_id=input_unique_id,
            type='unfreeze',
            amount=amount
        )

    def get_balance(
            self,
            db: Session,
            user_id: int,
    ):
        from sqlalchemy.sql import func
        balance = db.query(func.sum(self.crud.model.amount).filter(
            self.crud.model.user_id == user_id)
        ).first()[0]
        if balance == 0 or not balance:
            return 0
        else:
            return balance

    def get_blocked(
            self,
            db: Session,
            user_id: int,
    ):
        from sqlalchemy.sql import func

        blocked_balance = db.query(func.sum(self.crud.model.amount).filter(
            ((self.crud.model.user_id == user_id) & (
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
    ):
        from sqlalchemy.sql import func

        froze_balance = db.query(func.sum(self.crud.model.amount).filter(
            ((self.crud.model.user_id == user_id) & (
                    (self.crud.model.type == 'freeze') | (self.crud.model.type == 'unfreeze'))))
        ).first()[0]
        if froze_balance == 0 or not froze_balance:
            return 0
        else:
            return abs(froze_balance)

    def check_user_enough_balance(self, db: Session, amount: float, user_id: int):
        user_balance = self.get_balance(
            db=db,
            user_id=user_id,
        )
        if user_balance < amount:
            raise UserBalanceIsNotEnough


fiat_wallet_agent = FiatWalletInterface(
    crud=fiat_transaction_crud,
    create_schema=CreateFiatTransaction,
    update_schema=UpdateFiatTransaction,
    get_multi_schema=GetMultiFiatTransaction
)
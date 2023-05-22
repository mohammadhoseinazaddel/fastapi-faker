import datetime

from sqlalchemy.orm import Session

from finance.models.debt_user import debt_user_crud
from finance.models.schemas.debt_user import DebtUserCreate, DebtUserUpdate, DebtUserGetMulti
from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase


class DebtUserInterface(InterfaceBase):

    def __init__(
            self,
            crud: CRUDBase,
            create_schema,
            update_schema,
            get_multi_schema
    ):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        self.crud = debt_user_crud

    @staticmethod
    def get_due_date(debt_date: datetime = None):
        import jdatetime

        if not debt_date:
            debt_date = datetime.datetime.now()

        persian_debt_date = jdatetime.datetime.fromgregorian(datetime=debt_date)

        # تاریخ سررسید رو طبق صحبتهای شفاهی پنجم ماه شمسی بعد گذاشتم
        day = 5
        month = persian_debt_date.month + 1
        year = persian_debt_date.year

        if month > 12:
            month = 1
            year += 1

        return jdatetime.date(year=year, month=month, day=day).togregorian()

    def get_total_debt(
            self,
            user_id: int,
            db: Session
    ):
        from sqlalchemy.sql import func
        debt_amount = db.query(func.sum(self.crud.model.amount).filter(
            self.crud.model.user_id == user_id)
        ).first()[0]
        if debt_amount == 0 or not debt_amount:
            return 0
        else:
            return debt_amount

    def get_total_debt_of_order(
            self,
            user_id: int,
            order_id: str,
            db: Session
    ):
        try:
            from sqlalchemy.sql import func

            debt_amount = db.query(func.sum(self.crud.model.amount).filter(
                self.crud.model.user_id == user_id,
                self.crud.model.order_id == order_id,
            )
            ).first()[0]

            if debt_amount == 0 or not debt_amount:
                return 0

            if debt_amount < 0:
                raise "debt amount can not be negative"
            else:
                return debt_amount
        except Exception as e:
            raise e

    def decrease_debt(
            self,
            db: Session,
            user_id: int,
            amount: int,
            input_type: str,
            input_unique_id: int,
            order_id: int
    ):
        try:
            amount = abs(amount)
            return self.add_item(
                db=db,
                user_id=user_id,
                amount=-amount,
                input_type=input_type,
                input_unique_id=input_unique_id,
                order_id=order_id
            )

        except Exception as e:
            db.rollback()
            raise e


debt_user_agent = DebtUserInterface(
    crud=debt_user_crud,
    create_schema=DebtUserCreate,
    update_schema=DebtUserUpdate,
    get_multi_schema=DebtUserGetMulti
)

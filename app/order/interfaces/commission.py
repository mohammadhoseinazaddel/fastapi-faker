from sqlalchemy.orm import Session

from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase
from system.dbs.postgre import SessionLocal
from ..models.commission import commission_crud, CreateCommission, UpdateCommission, GetMultiCommission, OrdCommission


class CommissionInterface(InterfaceBase):

    def __init__(
            self,
            crud: CRUDBase,
            create_schema,
            update_schema,
            get_multi_schema
    ):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        self.crud = commission_crud
        self.model = OrdCommission

    def get_current_commission(
            self,
            merchant_id: int,
            category: str,
            db: Session = SessionLocal()
    ) -> OrdCommission:

        commission = self.find_item_multi(
            db=db,
            merchant_id=merchant_id,
            category=category
        ).sort(key=self.model.created_at, reverse=True)

        return commission[0]

    def get_pgw_commission_plus_fee(
            self,
            pgw_amount: int,
            commission_id: int,
            db: Session = SessionLocal()
    ):
        commission = self.find_item_multi(
            db=db,
            id=commission_id
        )[0]

        commission_amount = commission.pgw_commission_constant + commission.pgw_commission_rate * pgw_amount
        fee_amount = commission.pgw_fee_constant + commission.pgw_fee_rate * pgw_amount
        fee_amount *= int(commission.decrease_fee_on_pay_gw_settle)

        return commission_amount + fee_amount

    def get_credit_commission(
            self,
            used_credit: int,
            commission_id: int,
            db: Session = SessionLocal()
    ):
        commission = self.find_item_multi(
            db=db,
            id=commission_id
        )[0]

        return commission.credit_commission_constant + commission.credit_commission_rate * used_credit


commission_agent = CommissionInterface(
    crud=commission_crud,
    create_schema=CreateCommission,
    update_schema=UpdateCommission,
    get_multi_schema=GetMultiCommission
)

import uuid

from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from ext_services.jibit.interfaces.transfer import jibit_transferor_agent
from finance.api.v1.schemas.finance_admin import CqGetSettleDetail
from finance.exceptions.transfer import TransferFailed
from finance.models.schemas.settle_credit import SettleCreditCreate, SettleCreditUpdate, SettleCreditGetMulti
from finance.models.settle_credit import settle_credit_crud, FncSettleCredit
from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase
from system.dbs.postgre import SessionLocal
from system_object import SystemObjectsService


class SettleCreditInterface(InterfaceBase):

    def __init__(
            self,
            crud: CRUDBase,
            create_schema,
            update_schema,
            get_multi_schema
    ):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        self.crud = settle_credit_crud
        self.model = FncSettleCredit

    def get_unsettle_amount(
            # this method update all unsettle records with transfer_id
            self,
            merchant_id: int,
            transfer_id: int,
            db: Session = SessionLocal()

    ) -> int:  # return settlement amount

        model = self.crud.model

        if db.query(model).filter(model.transfer_id == transfer_id).first():
            raise SystemError("The transfer_id can not use for two settlement process")

        records = db.query(model) \
            .filter(model.merchant_id == merchant_id, model.transfer_id == None)

        if not records.all():
            return 0

        records.update({"transfer_id": transfer_id})

        return db.query(
            func.sum(model.amount)
            .filter(model.merchant_id == merchant_id, model.transfer_id == transfer_id)
        ).all()[0][0]

    def merchant_settlement(
            self,
            merchant_id: int,
            db: Session = SessionLocal()
    ):
        from .transfer import transfer_agent
        from .bank_profile import bank_profile_agent

        bank_profile = bank_profile_agent.find_item_multi(
            db=db,
            merchant_id=merchant_id,
            is_default=True
        )[0]

        transfer_record = transfer_agent.add_item(
            db=db,
            bank_profile_id=bank_profile.id,
            type='PAYA',
            transfer_id=str(uuid.uuid4()),
            batch_id=str(uuid.uuid4()),
            merchant_id=merchant_id
        )

        amount = self.get_unsettle_amount(merchant_id=merchant_id, transfer_id=transfer_record.id, db=db)
        if amount <= 0:
            raise SystemError("There merchant orders amount is not enough to settlement.")
        transfer_agent.update_item(db=db, find_by={"id": transfer_record.id}, update_to={"amount": amount})

        #  send money for this settlement by Jibit transferor
        transfer_res = jibit_transferor_agent.send_one_transfer(
            batch_id=transfer_record.batch_id,
            transfer_id=transfer_record.transfer_id,
            destination_IBAN=bank_profile.iban,
            amount=amount,
            description=transfer_record.description if transfer_record.description else "settle"
        )
        if 'submittedCount' in transfer_res and transfer_res['submittedCount'] == 1:
            transfer_agent.update_item(db=db, find_by={"id": transfer_record.id},
                                       update_to={"status": 'settlement_transfer_sent'})
            db.commit()

        else:
            raise TransferFailed

        return transfer_res

    def all_merchants_settle(self, db: Session = SessionLocal()):
        sys_obi_SR = SystemObjectsService()
        merchants = sys_obi_SR.merchant.find_item_multi(db=db)

        for merchant in merchants:
            db_local = SessionLocal()
            db_local.begin()

            try:
                self.merchant_settlement(db=db_local, merchant_id=merchant.id)

            except Exception as e:
                db_local.rollback()
                db_local.close()
                print(e)

            finally:
                db_local.commit()
                db_local.close()

    def get_all_relevant_transfer_ids(
            self,
            merchant_id: int,
            db: Session = SessionLocal()
    ):
        return db.query(self.model.transfer_id).filter(
            and_(self.model.merchant_id == merchant_id, self.model.transfer_id > 0)
        ).group_by(self.model.transfer_id).all()

    def get_settle_credit(self, page_number: int, page_size: int, **kwargs):
        data = {'result': [], 'total_count': None}

        credit_recs = self.crud.get_credit_settle_detail(
            db=kwargs['db'],
            skip=(page_number - 1) * page_size,
            limit=page_size,
            **CqGetSettleDetail(**kwargs).dict()
        )
        credit_result, credit_total_count = credit_recs['query_result'], credit_recs['total_count']
        if credit_result:
            for credit_settle in credit_result:
                settle_id = credit_settle.id
                from order import OrderService
                ord_sr = OrderService()
                order = ord_sr.pay.find_item_multi(
                    db=kwargs['db'],
                    settle_id=settle_id,
                    raise_not_found_exception=False,
                    return_first_obj=True
                )
                data['result'].append(
                    {
                        'id': settle_id,
                        'created_at': credit_settle.created_at,
                        'type': credit_settle.type,
                        'order_id': credit_settle.order_id,
                        'order_uuid': credit_settle.order_uuid,
                        'amount': credit_settle.amount,
                        'merchant_id': credit_settle.merchant_id,
                        'transfer_id': credit_settle.transfer_id,
                        'merchant_order_id': order.merchant_order_id if order else None,
                        'order_amount': order.amount if order else 0
                    }
                )
        data['total_count'] = credit_total_count
        return data

    def decrease_amount(
            self,
            amount: int,
            db: Session,
            order_id: int,
            order_uuid: str,
            type: str,
            merchant_id: int,
    ):
        try:
            amount = abs(amount)
            return self.add_item(
                db=db,
                order_id=order_id,
                amount=-amount,
                order_uuid=order_uuid,
                type=type,
                merchant_id=merchant_id
            )

        except Exception as e:
            db.rollback()
            raise e


settle_credit_agent = SettleCreditInterface(
    crud=settle_credit_crud,
    create_schema=SettleCreditCreate,
    update_schema=SettleCreditUpdate,
    get_multi_schema=SettleCreditGetMulti
)

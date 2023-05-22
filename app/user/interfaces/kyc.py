from sqlalchemy.orm import Session
from datetime import date

from ext_services.jibit.interfaces.identity_validate import jibit_identity_agent
from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase
from system.config import settings
from system.dbs.postgre import SessionLocal

from ..models.kyc import UsrKyc, kyc_crud
from ..models.schemas.kyc import KycCreateSchema, KycUpdateSchema, KycGetMultiSchema


class KycInterface(InterfaceBase):
    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)

        self.crud = crud
        self.model = UsrKyc

    @staticmethod
    def get_identity(national_code: str, georgian_birth_date: date):
        return jibit_identity_agent.get_identity(national_code, georgian_birth_date)

    @staticmethod
    def shahkar_validation(national_code: str, mobile: str):
        return jibit_identity_agent.shahkar_validation(national_code, mobile)



kyc_agent = KycInterface(
    crud=kyc_crud,
    create_schema=KycCreateSchema,
    update_schema=KycUpdateSchema,
    get_multi_schema=KycGetMultiSchema
)

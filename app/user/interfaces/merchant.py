from sqlalchemy.orm import Session

from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase
from ..exceptions.merchant import MerchantNotFound
from ..models.merchant import merchant_crud, UsrMerchant, CreateMerchant, GetMerchantByName
from ..models.schemas.merchant import UpdateMerchant, GetMultiMerchant


class MerchantInterface(InterfaceBase):
    """
    this class work base on safe delete
    """

    def __init__(self, crud: CRUDBase, create_schema, update_schema, get_multi_schema):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        self.model = UsrMerchant
        self._crud = merchant_crud

    def add_merchant(
            self,
            db: Session,
            name: str,
            name_fa: str,
            url: str,
            logo_address: str = None,
            logo_background_color=str
    ) -> UsrMerchant:
        try:
            merchant_item = self._crud.get_by_name(
                db=db,
                obj_in=GetMerchantByName(name=name),
            )
            if merchant_item is None:
                return self._crud.create(
                    db=db,
                    obj_in=CreateMerchant(
                        name=name,
                        url=url,
                        name_fa=name_fa,
                        logo_address=logo_address,
                        logo_background_color=logo_background_color
                    )
                )
            else:
                return merchant_item
        except Exception as e:
            db.rollback()
            raise e

    def get_by_name(self, db: Session, name: str) -> UsrMerchant:
        try:
            merchant_item = self._crud.get_by_name(
                db=db,
                obj_in=GetMerchantByName(name=name)
            )
            if merchant_item is None:
                raise MerchantNotFound
            else:
                return merchant_item
        except Exception as e:
            db.rollback()
            raise e

    def find_by_id(
            self,
            merchant_id: str,
            db: Session
    ):
        try:
            return self._crud.get(db=db, id=merchant_id)
        except MerchantNotFound:
            raise MerchantNotFound


merchant_agent = MerchantInterface(
    crud=merchant_crud,
    create_schema=CreateMerchant,
    update_schema=UpdateMerchant,
    get_multi_schema=GetMultiMerchant
)

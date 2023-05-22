from sqlalchemy.orm import Session

from finance.exceptions.bank_profile import UserAlreadyHaveBankProfile, UserNotVerified
from system.base.crud import CRUDBase
from system.base.interface import InterfaceBase

from finance.models.bank_profile import bank_profile_crud
from finance.models.schemas.bank_profile import BankProfileCreate, BankProfileUpdate, BankProfileGetMulti


class BankProfileInterface(InterfaceBase):

    def __init__(
            self,
            crud: CRUDBase,
            create_schema,
            update_schema,
            get_multi_schema
    ):
        super().__init__(crud, create_schema, update_schema, get_multi_schema)
        self.crud = bank_profile_crud

    def _validate_card_number_and_national_code_should_be_related(
            self,
            card_number,
            national_code,
            birth_date
    ):
        from ext_services.jibit.interfaces.identity_validate import jibit_identity_agent

        validation_card_number_with_national_code = jibit_identity_agent.is_match_card_number_with_national_code(
            card_number=card_number,
            national_code=national_code,
            birth_date=birth_date
        )

        if not validation_card_number_with_national_code['is_valid']:
            from system.base.exceptions import Error
            from fastapi import status

            class CardNumberValidation(Error):
                def __init__(self, ):
                    super().__init__(
                        message="Not valid card number",
                        errors={
                            'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                            'message': validation_card_number_with_national_code['error_message_fa'],
                            'field': '',
                            'type': ''
                        }
                    )

            raise CardNumberValidation

    def create_user_bank_profile(
            self,
            db: Session,
            user_id: int,
            card_number: str,
    ):
        from ext_services.jibit.interfaces.identity_validate import jibit_identity_agent
        from user import UserService

        user_sr = UserService()
        user_obj = user_sr.user.find_item_multi(db=db, id=user_id, return_first_obj=True)

        # get bank profile object from db
        bank_profile_obj = self.find_item_multi(
            db=db,
            raise_not_found_exception=False,
            user_id=user_id
        )

        # user shouldn't have bank profile record
        if bank_profile_obj:
            raise UserAlreadyHaveBankProfile

        # user should verify before
        if not user_obj.verified:
            raise UserNotVerified

        # If there have been any issue it will raise exception, otherwise nothing
        self._validate_card_number_and_national_code_should_be_related(
            card_number=card_number,
            national_code=user_obj.national_code,
            birth_date=user_obj.birth_date
        )

        # convert card number info
        converted_card_number_info_dict = jibit_identity_agent.convert_card_number_to_iban(
            card_number=card_number
        )

        # If there have been any issue by converting it will raise exception, otherwise nothing
        if not converted_card_number_info_dict['is_valid']:
            from system.base.exceptions import Error
            from fastapi import status

            class ConvertCardNumberInfoError(Error):
                def __init__(self, ):
                    super().__init__(
                        message="Not valid card number",
                        errors={
                            'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                            'message': converted_card_number_info_dict['error_message_fa'],
                            'field': '',
                            'type': ''
                        }
                    )
            raise ConvertCardNumberInfoError

        # add bank_profile obj to db
        self.add_item(
            db=db,
            user_id=user_id,
            first_name=user_obj.first_name,
            last_name=user_obj.last_name,
            bank_name=converted_card_number_info_dict['bank_name'],
            iban=converted_card_number_info_dict['iban'],
            account_no=converted_card_number_info_dict['account_number'],
            card_no=card_number,
            merchant_id=user_obj.merchant.id if user_obj.merchant.id else None,
        )
        return {'status': 'success'}


bank_profile_agent = BankProfileInterface(
    crud=bank_profile_crud,
    create_schema=BankProfileCreate,
    update_schema=BankProfileUpdate,
    get_multi_schema=BankProfileGetMulti
)

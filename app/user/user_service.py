import os

from sqlalchemy.orm import Session

from system.base.service import ServiceBase
from system.dbs.postgre import SessionLocal
from system.config import settings
from system.scopes import (
    user_scopes,
    finance_scopes,
    user_asset_scopes,
    order_scopes,
    credit_scopes,
    notification_scopes
)
from system.default_groups import (
    mobile_user_scopes,
    rudimentary_user_scopes,
    full_admin_user_scopes,
    merchant_sys_group_scopes,
    merchant_admin_group_scopes,
)


class UserService(ServiceBase):
    def __init__(self):
        from .interfaces.user import user_agent
        from .interfaces.group import group_agent
        from .interfaces.scope import scope_agent
        from .interfaces.otp import otp_agent
        from .interfaces.merchant import merchant_agent

        self.user = user_agent
        self.group = group_agent
        self.scope = scope_agent
        self.otp = otp_agent
        self.merchant = merchant_agent

    def initiate_scopes(self, db: Session = SessionLocal()):
        try:
            self.scope.create_or_update_scopes_from_dict(scope_dict=user_scopes, db=db)
            self.scope.create_or_update_scopes_from_dict(scope_dict=credit_scopes, db=db)
            self.scope.create_or_update_scopes_from_dict(scope_dict=finance_scopes, db=db)
            self.scope.create_or_update_scopes_from_dict(scope_dict=user_asset_scopes, db=db)
            self.scope.create_or_update_scopes_from_dict(scope_dict=order_scopes, db=db)
            self.scope.create_or_update_scopes_from_dict(scope_dict=order_scopes, db=db)
            self.scope.create_or_update_scopes_from_dict(scope_dict=notification_scopes, db=db)
        except Exception as e:
            raise e

    def initiate_default_groups(self, db: Session = SessionLocal()):
        try:
            self.group.create_or_update_group(
                group_name='mobile',
                scope_name_list=mobile_user_scopes,
                group_desc='گروه کاربران عادی احراز هویت شده',
                db=db
            )

            self.group.create_or_update_group(
                group_name='rudimentary',
                scope_name_list=rudimentary_user_scopes,
                group_desc='گروه کاربران عادی احراز هویت نشده',
                db=db
            )

            self.group.create_or_update_group(
                group_name='merchant_sys',
                scope_name_list=merchant_sys_group_scopes,
                group_desc='گروه کاربران مرچنت سیستمی',
                db=db
            )

            self.group.create_or_update_group(
                group_name='merchant_admin',
                scope_name_list=merchant_admin_group_scopes,
                group_desc='گروه کاربران مرچنت ادمین',
                db=db
            )

            self.group.create_or_update_group(
                group_name='full_admin',
                scope_name_list=full_admin_user_scopes,
                group_desc='گروه کاربران سوپر یوزر',
                db=db
            )

        except Exception as e:
            raise e

    def init_merchant_data(self, db: Session = SessionLocal()):

        try:
            if not self.merchant.find_item_multi(db=db, raise_not_found_exception=False, name='Alibaba'):
                merchant = self.merchant.add_item(
                    db=db,
                    name='Alibaba',
                    name_fa='علی بابا',
                    url='https://www.alibaba.ir/',
                    logo_address=f'{settings.WALLPAY_BASE_URL}/statics/logos/merchants/alibaba.svg',
                    logo_background_color='#FFEBE4',

                )

                from order import OrderService
                order_sr = OrderService()
                # Add commission type to alibaba merchant
                order_sr.commission.add_item(
                    db=db,
                    category='AIRPLANE',
                    title='ALIBABA_AIRPLANE',
                    merchant_id=merchant.id,
                    bank_payment_rate=0,
                    credit_rate=0,
                )

            db.commit()
        except Exception as e:
            raise e

    def initiate_full_admin_user(self, db: Session = SessionLocal()):
        try:
            user = self.user.find_item_multi(
                db=db,
                username=os.environ.get("FIRST_ADMIN_USERNAME", 'admin'),
                raise_not_found_exception=False
            )
            if not user:
                user = self.user.add_item(
                    db=db,
                    username=os.environ.get("FIRST_ADMIN_USERNAME", 'admin'),
                    hashed_pass=self.user.jwt.hash_password(os.environ.get("FIRST_ADMIN_PASSWORD", 'password'))
                )
                db.commit()
            else:
                user = user[0]

            full_admin_group = self.group.find_item_multi(
                db=db,
                name='full_admin'
            )[0]
            self.user.add_to_group(user_id=user.id, group_id=full_admin_group.id, db=db)

            full_admin_merchant = self.merchant.find_item_multi(
                db=db,
                name='Alibaba'
            )[0]
            self.user.add_to_merchant(user_id=user.id, merchant_id=full_admin_merchant.id, db=db)

            db.commit()

        except Exception as e:
            raise e


user_sr = UserService()

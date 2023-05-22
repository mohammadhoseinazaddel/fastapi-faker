from faker.exceptions import UniquenessException
from passlib.context import CryptContext
from sqlalchemy import create_engine, String, and_
from faker import Faker
from system.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, exists
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from system.dbs import tables

fake = Faker()
engine = create_engine(settings.POSTGRES_DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
default_session = Session()
fake_fa = Faker('fa_IR')


# create an engine to connect to the database
class ModelsSeeder:
    def __init__(self, session: Session = default_session):
        self.session = session
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def _hash_password(self, password: str):
        return self.pwd_context.hash(password)

    # generate fake data for the UsrKyc model
    def create_fake_kyc(self, number):
        for _ in range(number):
            kyc = tables.UsrKyc(
                created_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                updated_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                deleted_at=None,
                sabte_ahval_inquired_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                sabte_ahval_track_no=fake.uuid4(),
                sabte_ahval_verified=fake.boolean(),
                shahkar_inquired_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                shahkar_verified=fake.boolean(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                father_name=fake.first_name(),
            )
            self.session.add(kyc)
            try:
                self.session.commit()
            except IntegrityError:
                self.session.rollback()
                continue

    def create_fake_user(self, number):
        for _ in range(number):
            try:
                # Generate a random 10-digit number as a string
                # Generate a random birth year between 1300 and 1399 (Persian calendar)
                birth_year = fake_fa.random_int(min=0, max=99)

                # Generate a random birth month and day
                birth_month = fake_fa.random_int(min=1, max=12)
                birth_day = fake_fa.random_int(min=1, max=31)

                # Generate a random gender digit (1 for male, 2 for female)
                gender_digit = fake_fa.random_element(elements=("1", "2"))

                # Generate a random 6-digit number
                random_number = fake_fa.random_number(digits=6)

                # Combine the components to create a valid Persian national code
                national_code = f"0{gender_digit}{str(birth_year).zfill(2)}" \
                                f"{str(birth_month).zfill(2)}" \
                                f"{str(birth_day).zfill(2)}" \
                                f"{random_number}"
                mobile = fake.phone_number(),
                username = fake.user_name(),
                password = fake.password(),
                kyc_ids = [kyc.id for kyc in self.session.query(tables.UsrKyc.id)]
            except UniquenessException:
                continue
            try:
                existing_user = self.session.query(tables.UsrUser).filter_by(
                    username=username,
                    mobile=mobile,
                    national_code=national_code
                ).one()
                # if you need lot data use below code instance
                # existing_user = self.session.query(UsrUser).filter(or_(
                #     UsrUser.username == username,
                #     UsrUser.mobile == mobile,
                #     UsrUser.national_code == national_code
                # )).first()
                # if the name exists, skip this record and move on to the next one
                continue
            except NoResultFound:
                usr_user = tables.UsrUser(
                    created_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                    updated_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                    deleted_at=None,
                    kyc_id=fake.random_element(elements=kyc_ids),
                    email=fake.email(),
                    mobile=mobile,
                    username=username,
                    hashed_pass=self._hash_password(password[0]),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    father_name=fake.first_name(),
                    gender=fake.random_element(elements=('male', 'female')),
                    national_code=national_code,
                    birth_date=fake.date_of_birth(),
                    profile_image=fake.image_url(),
                    last_login=fake.date_time_between(start_date='-3M', end_date='+3M'),
                    identifier=fake.uuid4(),
                    is_disabled=fake.boolean(),
                    # is_banned=fake.boolean(),
                    verified=fake.boolean(),
                    verified_by=fake.random_element(elements=('sabte_ahval', 'shahkar')),
                    verified_at=fake.date_time_between(start_date='-3M', end_date='+3M')
                )
                self.session.add(usr_user)
                try:
                    self.session.commit()
                except IntegrityError:
                    self.session.rollback()
                    continue

    # generate fake data for the UsrMerchant model
    def create_fake_user_merchant(self, number):
        for _ in range(number):
            try:
                name = fake.unique.company()
                name_fa = fake_fa.unique.company()
                url = fake.url()
                logo_address = fake.image_url()
                logo_background_color = fake.color()
            except UniquenessException:
                continue

            # check if the name already exists in the table
            try:
                existing_merchant = self.session.query(tables.UsrMerchant).filter_by(name=name, name_fa=name_fa).one()
                # if you need lot data use below code instance
                # existing_merchant = self.session.query(UsrMerchant).filter(or_(UsrMerchant.name == name,UsrMerchant.name_fa == name_fa)).first()
                # if the name exists, skip this record and move on to the next one
                continue
            except NoResultFound:
                # if the name does not exist, insert a new record
                usr_merchant = tables.UsrMerchant(
                    created_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                    updated_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                    deleted_at=None,
                    name=name,
                    name_fa=name_fa,
                    url=url,
                    logo_address=logo_address,
                    logo_background_color=logo_background_color
                )
                self.session.add(usr_merchant)
                try:
                    self.session.commit()
                except IntegrityError:
                    self.session.rollback()
                    continue

    # generate fake data for the UsrUserMerchant model
    def create_fake_user_user_merchant(self, number):
        for _ in range(number):
            user_id = self.session.query(tables.UsrUser.id).order_by(func.random()).first()[0]
            merchant_id = self.session.query(tables.UsrMerchant.id).order_by(func.random()).first()[0]
            created_at = fake.date_time_between(start_date='-3M', end_date='+3M')
            updated_at = created_at
            deleted_at = None
            usr_user_merchant = tables.UsrUserMerchants(
                created_at=created_at,
                updated_at=updated_at,
                deleted_at=deleted_at,
                user_id=user_id,
                merchant_id=merchant_id
            )
            self.session.add(usr_user_merchant)

            try:
                self.session.commit()
            except IntegrityError as e:
                self.session.rollback()
                if 'duplicate key value violates unique constraint "user_merchant_unique"' in str(e):
                    # if the error is due to a duplicate record, skip it and move on to the next one
                    continue
                else:
                    # if the error is due to some other reason, raise the error
                    raise e

    def create_fake_fnc_bank_payment(self, number):
        for i in range(number):
            # Generate fake data for FncBankPayment
            user_id = self.session.query(tables.UsrUser.id).order_by(func.random()).first()[0]
            # success_pgw_id = self.session.query(FncPaymentGateway.id).order_by(func.random()).first()[0]
            bank_payment = tables.FncBankPayment(
                created_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                updated_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                deleted_at=None,
                bank_payment_id=None,  # Set to None for simplicity
                type=fake.random_element(elements=('deposit', 'withdrawal')),
                input_type=fake.random_element(elements=('credit', 'debit')),
                input_unique_id=fake.random_number(digits=5),
                user_id=user_id,
                amount=fake.random_int(min=1000, max=100000),
                wage=fake.random_int(min=0, max=1000),
                description=fake.text(),
                expired_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                status=fake.random_element(elements=('pending', 'completed', 'failed')),
                success_pgw_id=None
            )
            self.session.add(bank_payment)
            try:
                self.session.commit()
            except IntegrityError:
                self.session.rollback()
                continue

    def create_fake_fnc_payment_gateway(self, number):
        for i in range(number):
            # Generate fake data for FncPaymentGateway
            user_id = self.session.query(tables.UsrUser.id).order_by(func.random()).first()[0]
            bank_payment_id = None
            if i > 1:
                bank_payment_id = self.session.query(tables.FncBankPayment.id).order_by(func.random()).first()[0]
            payment_gateway = tables.FncPaymentGateway(
                created_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                updated_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                deleted_at=None,
                type=fake.random_element(elements=('credit_card', 'bank_transfer')),
                payment_gateway_id=None,
                bank_payment_id=bank_payment_id,
                amount=fake.random_int(min=1000, max=100000),
                wage=fake.random_int(min=0, max=1000),
                gateway_name=fake.random_element(elements=('paypal', 'stripe', 'braintree')),
                description=fake.text(),
                status=fake.random_element(elements=('pending', 'completed', 'failed')),
                ref_num=fake.uuid4(),
                expired_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                psp_purchase_id=fake.uuid4(),
                psp_switching_url=fake.url(),
                callback_status=fake.random_element(elements=('success', 'failure')),
                psp_status=fake.random_element(elements=('authorized', 'captured', 'refunded')),
                psp_trace_no=fake.random_number(digits=10),
                payer_ip=fake.ipv4(),
                psp_ref_num=fake.uuid4(),
                psp_rrn=fake.random_number(digits=10),
                payer_masked_card_num=fake.credit_card_number(card_type=None),
                psp_name=fake.random_element(elements=('braintree', 'paypal', 'stripe')),
                reversed_at=None,  # Set to None for simplicity
                reverse_status=None,  # Set to None for simplicity
                refund_batch_id=None,  # Set to None for simplicity
                refund_transfer_id=None  # Set to None for simplicity
            )
            self.session.add(payment_gateway)
            try:
                self.session.commit()
            except IntegrityError:
                self.session.rollback()
                continue

    def create_fake_fnc_bank_transaction(self, number):
        for _ in range(number):
            # Generate fake data for FncBankTransaction
            bank_transaction = tables.FncBankTransactions(
                created_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                updated_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
            )
            self.session.add(bank_transaction)
            try:
                self.session.commit()
            except IntegrityError:
                self.session.rollback()
                continue

    def create_fake_fnc_bank_profile(self, number):
        for _ in range(number):
            user_id = self.session.query(tables.UsrUser.id).order_by(func.random()).first()[0]
            merchant_id = self.session.query(tables.UsrMerchant.id).order_by(func.random()).first()[0]
            # Generate fake data for FncBankProfile
            bank_profile = tables.FncBankProfile(
                created_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                updated_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                deleted_at=None,
                user_id=user_id,
                merchant_id=merchant_id,
                is_default=fake.boolean(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                bank_name=fake.random_element(elements=('Bank of America', 'Chase', 'Wells Fargo')),
                account_no=fake.random_number(digits=10),
                iban=fake.iban(),
                card_no=fake.credit_card_number(card_type=None)
            )
            self.session.add(bank_profile)
            try:
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                continue

    def create_fake_fnc_debt_user(self, number):
        for _ in range(number):
            user_id = self.session.query(tables.UsrUser.id).order_by(func.random()).first()[0]
            order_id = self.session.query(tables.OrdPay.id).order_by(func.random()).first()[0]
            # Generate fake data for FncDebtUser
            debt_user = tables.FncDebtUser(
                created_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                updated_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                deleted_at=None,
                user_id=user_id,
                amount=fake.random_int(min=1000, max=100000),
                due_date=fake.date_between(start_date='now', end_date='+1y'),
                input_type=fake.random_element(elements=('credit', 'debit')),
                input_unique_id=fake.random_number(digits=5),
                order_id=order_id
            )
            self.session.add(debt_user)
            try:
                self.session.commit()
            except IntegrityError:
                self.session.rollback()
                continue

    def create_fake_fnc_transfer(self, number):
        for _ in range(number):
            bank_profile_id = self.session.query(tables.FncBankProfile.id).order_by(func.random()).first()[0]
            merchant_id = self.session.query(tables.UsrMerchant.id).order_by(func.random()).first()[0]
            # Generate fake data for FncTransfer
            transfer = tables.FncTransfer(
                created_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                updated_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                deleted_at=None,
                bank_profile_id=bank_profile_id,
                type=fake.random_element(elements=('pgw', 'credit')),
                amount=fake.random_int(min=1000, max=100000),
                description=fake.text(),
                batch_id=fake.uuid4(),
                transfer_id=fake.uuid4(),
                status=fake.random_element(elements=('pending', 'completed', 'failed')),
                ext_service_name=fake.random_element(elements=('zarinpal', 'payline', 'mellat')),
                input_type=fake.random_element(elements=('credit', 'debit')),
                input_unique_id=fake.random_number(digits=5),
                error_message=None,  # Set to None for simplicity
                merchant_id=merchant_id
            )
            self.session.add(transfer)
            try:
                self.session.commit()
            except IntegrityError:
                self.session.rollback()
                continue

    def create_fake_fnc_settle_credit(self, number):
        for _ in range(number):
            order_id = self.session.query(tables.OrdPay.id).order_by(func.random()).first()[0]
            order_uuid = self.session.query(tables.OrdPay.identifier).order_by(func.random()).first()[0]
            merchant_id = self.session.query(tables.UsrMerchant.id).order_by(func.random()).first()[0]
            transfer_id = self.session.query(tables.FncTransfer.id).order_by(func.random()).first()[0]
            settle_credit_type = fake.random_element(elements=('pay', 'reverse', 'refund'))

            # Check if a record with the same order_id and type already exists in the FncSettleCredit table
            if not self.session.query(tables.FncSettleCredit).filter_by(order_id=order_id,
                                                                        type=settle_credit_type).first():
                # Generate fake data for FncSettleCredit
                settle_credit = tables.FncSettleCredit(
                    created_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                    updated_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                    deleted_at=None,
                    order_id=order_id,
                    order_uuid=order_uuid,
                    type=settle_credit_type,
                    merchant_id=merchant_id,
                    amount=fake.random_int(min=1000, max=100000),
                    transfer_id=transfer_id
                )
                self.session.add(settle_credit)
                try:
                    self.session.commit()
                except IntegrityError:
                    self.session.rollback()
                    continue

    def create_fake_fnc_pgw_credit(self, number):
        settle_type = fake.random_element(elements=('pay', 'reverse', 'refund'))

        for _ in range(number):
            order_id_subquery = self.session.query(tables.FncSettlePgw.order_id). \
                filter(tables.FncSettlePgw.type == settle_type)

            order_id = self.session.query(tables.OrdPay.id). \
                filter(~tables.OrdPay.id.in_(order_id_subquery)). \
                order_by(func.random()).first()[0]
            order_uuid = self.session.query(tables.OrdPay.identifier).order_by(func.random()).first()[0]
            merchant_id = self.session.query(tables.UsrMerchant.id).order_by(func.random()).first()[0]
            transfer_id = self.session.query(tables.FncTransfer.id).order_by(func.random()).first()[0]

            # Check if a record with the same order_id and type already exists in the FncSettleCredit table
            if not self.session.query(exists().where(and_(tables.FncSettlePgw.order_id == order_id,
                                                          tables.FncSettlePgw.type == settle_type))).scalar():
                # Generate fake data for FncSettleCredit
                settle_credit = tables.FncSettlePgw(
                    created_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                    updated_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                    deleted_at=None,
                    order_id=order_id,
                    order_uuid=order_uuid,
                    type=settle_type,
                    merchant_id=merchant_id,
                    amount=fake.random_int(min=1000, max=100000),
                    transfer_id=transfer_id
                )
                self.session.add(settle_credit)
                try:
                    self.session.commit()
                except IntegrityError:
                    self.session.rollback()
                    continue

    def create_fake_ord_pgw(self, number):
        for _ in range(number):
            commission_id = self.session.query(tables.OrdCommission.id).order_by(func.random()).first()[0]
            user_id = self.session.query(tables.UsrUser.id).order_by(func.random()).first()[0]
            merchant_id = self.session.query(tables.UsrMerchant.id).order_by(func.random()).first()[0]
            settle_pgw_id = self.session.query(tables.FncSettlePgw.id).order_by(func.random()).first()[0]
            # Generate fake data for OrdPayPgw
            ord_pay = tables.OrdPay(
                created_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                updated_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                deleted_at=None,
                title=fake.text(max_nb_chars=30),
                identifier=fake.uuid4(),
                user_id=user_id,
                type=fake.random_element(elements=('credit_card', 'bank_transfer')),
                amount=fake.pyfloat(min_value=10.0, max_value=1000.0, right_digits=2),
                status=fake.random_element(elements=('SUCCESS', 'WAIT', 'FAIL')),
                action=fake.random_element(elements=('authorize', 'capture', 'refund')),
                paid_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                merchant_order_id=fake.uuid4(),
                merchant_id=merchant_id,
                merchant_user_id=fake.random_number(digits=5),
                merchant_redirect_url=fake.url(),
                settle_id=settle_pgw_id,
                commission_id=commission_id
            )
            self.session.add(ord_pay)
            try:
                self.session.commit()
            except IntegrityError:
                self.session.rollback()
                continue

    def create_fake_ord_credit(self, number):
        for _ in range(number):
            commission_id = self.session.query(tables.OrdCommission.id).order_by(func.random()).first()[0]
            user_id = self.session.query(tables.UsrUser.id).order_by(func.random()).first()[0]
            merchant_id = self.session.query(tables.UsrMerchant.id).order_by(func.random()).first()[0]
            settle_credit_id = self.session.query(tables.FncSettleCredit.id).order_by(func.random()).first()[0]
            # Generate fake data for OrdPayPgw
            ord_pay = tables.OrdPay(
                created_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                updated_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                deleted_at=None,
                title=fake.text(max_nb_chars=30),
                identifier=fake.uuid4(),
                user_id=user_id,
                type=fake.random_element(elements=('credit_card', 'bank_transfer')),
                amount=fake.pyfloat(min_value=10.0, max_value=1000.0, right_digits=2),
                status=fake.random_element(elements=('SUCCESS', 'WAIT', 'FAIL')),
                action=fake.random_element(elements=('authorize', 'capture', 'refund')),
                paid_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                merchant_order_id=fake.uuid4(),
                merchant_id=merchant_id,
                merchant_user_id=fake.random_number(digits=5),
                merchant_redirect_url=fake.url(),
                settle_id=settle_credit_id,
                commission_id=commission_id
            )
            self.session.add(ord_pay)
            try:
                self.session.commit()
            except IntegrityError:
                self.session.rollback()
                continue

    def create_fake_ord(self, number):
        for _ in range(number):
            commission_id = self.session.query(tables.OrdCommission.id).order_by(func.random()).first()[0]
            user_id = self.session.query(tables.UsrUser.id).order_by(func.random()).first()[0]
            merchant_id = self.session.query(tables.UsrMerchant.id).order_by(func.random()).first()[0]
            # settle_credit_id = self.session.query(FncSettleCredit.id).order_by(func.random()).first()[0]
            # Generate fake data for OrdPayPgw
            ord_pay = tables.OrdPay(
                created_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                updated_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                deleted_at=None,
                title=fake.text(max_nb_chars=30),
                identifier=fake.uuid4(),
                user_id=user_id,
                type=fake.random_element(elements=('POST_PAY', 'PAY_IN_FOUR')),
                amount=fake.random_int(min=50000, max=50000000),

                status=fake.random_element(elements=('SUCCESS', 'FAIL', 'FAIL_FILL', 'FAIL_WALLEX', 'FAIL_PAYMENT',
                                                     'WAIT_PROCESS', 'WAIT_WALLEX', 'WAIT_PAYMENT', 'WAIT_COLLATERAL',
                                                     'PROCESS', 'REFUNDED', 'WAIT_IBAN_TO_REFUND', 'REFUNDING')),

                action=fake.random_element(elements=('UNVERIFIED', 'APPROVED', 'REJECTED')),
                paid_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                merchant_order_id=fake.uuid4(),
                merchant_id=merchant_id,
                merchant_user_id=fake.random_number(digits=5),
                merchant_redirect_url=fake.url(),
                settle_id=fake.random_number(digits=2),
                commission_id=commission_id
            )
            self.session.add(ord_pay)
            try:
                self.session.commit()
            except IntegrityError:
                self.session.rollback()
                continue

    def create_fake_ord_fund(self, number):
        for _ in range(number):
            order_id = self.session.query(tables.OrdPay.id).order_by(func.random()).first()[0]
            user_id = self.session.query(tables.UsrUser.id).order_by(func.random()).first()[0]

            # Check if the order_id already exists in the OrdFund table
            if not self.session.query(exists().where(tables.OrdFund.order_id == order_id)).scalar():
                # Generate fake data for OrdFund
                ord_fund = tables.OrdFund(
                    created_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                    updated_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                    deleted_at=None,
                    order_id=order_id,
                    order_amount=fake.random_int(min=1000, max=100000),
                    user_id=user_id,
                    used_free_credit=fake.random_int(min=0, max=10000),
                    used_non_free_credit=fake.random_int(min=0, max=10000),
                    repaid_free_credit=fake.random_int(min=0, max=10000),
                    repaid_non_free_credit=fake.random_int(min=0, max=10000),
                    used_asset_json=None,  # Set to None for simplicity
                    extra_money_to_pay=fake.random_int(min=0, max=10000),
                    need_collateral=fake.boolean(),
                    collateral_confirmed=fake.boolean(),
                    need_wallex_asset=fake.boolean(),
                    wallex_block_request_id=fake.uuid4(),
                    payment_amount=fake.random_int(min=1000, max=100000),
                    payment_id=fake.random_number(digits=5),
                    paid_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                    completely_repaid_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                    fill_percentage=fake.random_int(min=0, max=100)
                )
                self.session.add(ord_fund)
                try:
                    self.session.commit()
                except IntegrityError:
                    self.session.rollback()
                    continue

    def create_fake_ord_commission(self, number):
        for _ in range(number):
            merchant_id = self.session.query(tables.UsrMerchant.id).order_by(func.random()).first()[0]
            # Generate fake data for OrdCommission
            ord_commission = tables.OrdCommission(
                created_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                updated_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                deleted_at=None,
                merchant_id=merchant_id,
                category=fake.random_element(elements=('food', 'clothing', 'electronics')),
                pgw_commission_constant=fake.random_int(min=100, max=1000),
                pgw_commission_rate=fake.pyfloat(min_value=0.01, max_value=0.1, right_digits=2),
                pgw_fee_constant=fake.random_int(min=10, max=100),
                pgw_fee_rate=fake.pyfloat(min_value=0.01, max_value=0.1, right_digits=2),
                credit_commission_constant=fake.random_int(min=100, max=1000),
                credit_commission_rate=fake.pyfloat(min_value=0.01, max_value=0.1, right_digits=2),
                credit_limit=fake.random_int(min=1000, max=10000),
                decrease_fee_on_pay_gw_settle=fake.boolean(),
                decrease_commission_on_refund=fake.boolean()
            )

            self.session.add(ord_commission)
            try:
                self.session.commit()
            except IntegrityError:
                self.session.rollback()
                continue

    def create_fake_fnc_refund(self, number):
        for _ in range(number):
            commission_id = self.session.query(tables.OrdCommission.id).order_by(func.random()).first()[0]
            user_id = self.session.query(tables.UsrUser.id).order_by(func.random()).first()[0]
            merchant_id = self.session.query(tables.UsrMerchant.id).order_by(func.random()).first()[0]
            order_uuid = self.session.query(tables.OrdPay.identifier).order_by(func.random()).first()[0]
            order_id = self.session.query(tables.OrdPay.id) \
                .filter(tables.OrdPay.id.notin_(self.session.query(tables.FncRefund.order_id))) \
                .order_by(func.random()) \
                .first()[0]

            # Check if the order_uuid already exists in the FncRefund table
            if not self.session.query(exists().where(tables.FncRefund.order_uuid == order_uuid)).scalar():
                # Generate fake data for FncRefund
                fnc_refund = tables.FncRefund(
                    created_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                    updated_at=fake.date_time_between(start_date='-3M', end_date='+3M'),
                    deleted_at=None,
                    uuid=fake.uuid4(),
                    order_id=order_id,
                    order_uuid=order_uuid,
                    order_user_id=user_id,
                    merchant_id=merchant_id,
                    merchant_user_id=fake.random_number(digits=5),
                    amount=fake.random_int(min=1000, max=100000),
                    status=fake.random_element(elements=('pending', 'completed', 'failed')),
                    refund_by_debt=fake.random_int(min=0, max=10000),
                    refund_by_rial=fake.random_int(min=0, max=10000)
                )

                self.session.add(fnc_refund)
                try:
                    self.session.commit()
                except IntegrityError:
                    self.session.rollback()
                    continue

    ################## future needed for initialize user seeds ##################
    # commit the session to the database
    #     try:
    #         session.commit()
    #     except Exception as e:
    #         session.rollback()
    #         if 'duplicate key value violates unique constraint "user_merchant_unique"' in str(e):
    #             # if the error is due to a duplicate record, skip it and move on to the next one
    #             pass
    #         else:
    #             # if the error is due to some other reason, raise the error
    #             raise e

    # # generate fake data for the UsrGroup model
    # for _ in range(5):
    #     usr_group = UsrGroup(
    #         created_at=fake.date_time_between(start_date='-30d', end_date='now'),
    #         updated_at=fake.date_time_between(start_date='-30d', end_date='now'),
    #         deleted_at=None,
    #         name=fake.unique.word(),
    #         fa_name=fake.unique.word(),
    #         description=fake.text()
    #     )
    #     session.add(usr_group)
    #
    # # generate fake data for the UsrUserGroups model
    # for _ in range(10):
    #     gp_id = [gp.id for gp in session.query(UsrGroup.id)]
    #     user = session.query(UsrUser.id).order_by(func.random()).first()
    #     group = session.query(UsrGroup).order_by(func.random()).first()
    #     created_at = fake.date_time_between(start_date='-30d', end_date='now')
    #     updated_at = created_at
    #     deleted_at = None
    #     usr_user_groups = UsrUserGroups(
    #         created_at=created_at,
    #         updated_at=updated_at,
    #         deleted_at=deleted_at,
    #         user_id=user.id,
    #         group_id=group.id
    #     )
    #     session.add(usr_user_groups)

    # generate fake data for the UsrScope model
    # for _ in range(5):
    #     usr_scope = UsrScope(
    #         created_at=fake.date_time_between(start_date='-30d', end_date='now'),
    #         updated_at=fake.date_time_between(start_date='-30d', end_date='now'),
    #         deleted_at=None,
    #         name=fake.unique.word(),
    #         fa_name=fake.unique.word(),
    #         description=fake.text(),
    #         module='usr',
    #         interface=fake.unique.word(),
    #         endpoint=fake.unique.url(),
    #         action=fake.unique.word(),
    #     )
    #     session.add(usr_scope)

    # generate fake data for the UsrGroupScope model
    # for _ in range(10):
    #     group = session.query(UsrGroup).order_by(func.random()).first()
    #     scope = session.query(UsrScope).order_by(func.random()).first()
    #     created_at = fake.date_time_between(start_date='-30d', end_date='now')
    #     updated_at = created_at
    #     deleted_at = None
    #     usr_group_scope = UsrGroupScope(
    #         created_at=created_at,
    #         updated_at=updated_at,
    #         deleted_at=deleted_at,
    #         group_id=group.id,
    #         scope_id=scope.id
    #     )
    #     session.add(usr_group_scope)

    # generate fake data for the UsrSession model
    # for _ in range(10):
    #     user = session.query(UsrUser).order_by(func.random()).first()
    #     created_at = fake.date_time_between(start_date='-30d', end_date='now')
    #     updated_at = created_at
    #     deleted_at = None
    #     usr_session = UsrSession(
    #         created_at=created_at,
    #         updated_at=updated_at,
    #         deleted_at=deleted_at,
    #         token=fake.uuid4(),
    #         user_id=user.id,
    #         expire_at=fake.date_time_between(start_date='+30d', end_date='+60d'),
    #         os=fake.user_agent(),
    #         ip=fake.ipv4_public(),
    #         device_model=fake.user_agent(),
    #         device_token=fake.uuid4(),
    #         device_id=fake.uuid4(),
    #     )
    #     session.add(usr_session)

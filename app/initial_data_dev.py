from seeder.models_seeder import ModelsSeeder
from system.dbs.postgre import SessionLocal
from system_object.models.coin import SoCoin


def fake_maker_how_many(fake_kyc_number=10, fake_user=10, fake_user_merchant=10, fake_user_user_merchant=10,
                        fake_fnc_bank_profile=10, fake_fnc_bank_payment=10, fake_fnc_payment_gateway=10,
                        fake_fnc_bank_transaction=10, fake_ord_commission=10, fake_ord=10, fake_ord_fund=10,
                        fake_fnc_transfer=10, fake_fnc_settle_credit=10, fake_fnc_pgw_credit=10,
                        fake_fnc_debt_user=10, fake_fnc_refund=10):
    """
    Generates a specified number of fake records for various tables in the database.

    Parameters:
    fake_kyc_number (int): The number of fake KYC records to generate.
    fake_user (int): The number of fake user records to generate.
    fake_user_merchant (int): The number of fake user-merchant records to generate.
    fake_user_user_merchant (int): The number of fake user-user-merchant records to generate.
    fake_fnc_bank_profile (int): The number of fake bank profile records to generate.
    fake_fnc_bank_payment (int): The number of fake bank payment records to generate.
    fake_fnc_payment_gateway (int): The number of fake payment gateway records to generate.
    fake_fnc_bank_transaction (int): The number of fake bank transaction records to generate.
    fake_ord_commission (int): The number of fake commission records to generate.
    fake_ord (int): The number of fake order records to generate.
    fake_ord_fund (int): The number of fake order fund records to generate.
    fake_fnc_transfer (int): The number of fake transfer records to generate.
    fake_fnc_settle_credit (int): The number of fake settle credit records to generate.
    fake_fnc_pgw_credit (int): The number of fake payment gateway credit records to generate.
    fake_fnc_debt_user (int): The number of fake user debt records to generate.
    fake_fnc_refund (int): The number of fake refund records to generate.

    Returns:
    None
    """
    model_seeder = ModelsSeeder()
    model_seeder.create_fake_kyc(fake_kyc_number)
    model_seeder.create_fake_user(fake_user)
    model_seeder.create_fake_user_merchant(fake_user_merchant)
    model_seeder.create_fake_user_user_merchant(fake_user_user_merchant)

    model_seeder.create_fake_fnc_bank_profile(fake_fnc_bank_profile)

    model_seeder.create_fake_fnc_bank_payment(fake_fnc_bank_payment)
    model_seeder.create_fake_fnc_payment_gateway(fake_fnc_payment_gateway)

    model_seeder.create_fake_fnc_bank_transaction(fake_fnc_bank_transaction)

    model_seeder.create_fake_ord_commission(fake_ord_commission)

    model_seeder.create_fake_ord(fake_ord)

    model_seeder.create_fake_ord_fund(fake_ord_fund)

    model_seeder.create_fake_fnc_transfer(fake_fnc_transfer)
    model_seeder.create_fake_fnc_settle_credit(fake_fnc_settle_credit)
    model_seeder.create_fake_fnc_pgw_credit(fake_fnc_pgw_credit)
    model_seeder.create_fake_fnc_debt_user(fake_fnc_debt_user)
    model_seeder.create_fake_fnc_refund(fake_fnc_refund)

    # model_seeder.create_fake_ord_pgw(10)
    # model_seeder.create_fake_ord_credit(10)


if __name__ == "__main__":
    coin_count = SessionLocal().query(SoCoin.id).count()
    if coin_count == 0:
        fake_maker_how_many(fake_kyc_number=0, fake_user=0, fake_user_merchant=0, fake_user_user_merchant=0,
                            fake_fnc_bank_profile=10, fake_fnc_bank_payment=200, fake_fnc_payment_gateway=200,
                            fake_fnc_bank_transaction=200, fake_ord_commission=10, fake_ord=500, fake_ord_fund=400,
                            fake_fnc_transfer=500, fake_fnc_settle_credit=500, fake_fnc_pgw_credit=500,
                            fake_fnc_debt_user=100, fake_fnc_refund=29)

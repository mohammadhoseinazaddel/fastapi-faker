from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ext_services.wallex.interfaces.pay import wallex_pay_agent
from system.config import settings
from system.dbs.postgre import get_db
from system_object import SystemObjectsService
from user_assets import UserAssetsService
from utils import redirect_no_cache

router = APIRouter()


@router.get("/callback/{uuid}", response_description="wallex pay call back")
def wallex_pay_callback(
        uuid: str,
        success: bool,
        token: str,
        order_id: str,
        state: str,
        db: Session = Depends(get_db)
):
    redirect_response_url = None
    # create redirect response url
    if state == 'pay-order':
        redirect_response_url = \
            settings.WALLPAY_BASE_URL \
            + '/api/v1/order/pay/callback/' \
            + order_id
    try:
        # check wallex pay record exist
        wallex_pay_record = wallex_pay_agent.find_item_multi(db=db, uuid=uuid)[0]
        if wallex_pay_record:
            user_assets_sr = UserAssetsService()
            system_object_sr = SystemObjectsService()
            # check pay request stats
            if success:
                # inquery request for check result
                inquiry_res = wallex_pay_agent.api_inquiry_request(token=token)
                inquiry_status = inquiry_res['result']['status']
                # check transaction is UNVERIFIED and block assets
                if inquiry_status == 'UNVERIFIED':
                    assets = wallex_pay_record.assets
                    for asset in assets:
                        # find coin name from system object coins
                        coin = system_object_sr.coin.find_item_multi(
                            db=db,
                            wallex_symbol=asset['currency']
                        )[0]
                        # add block records to wallex transaction table
                        if asset['amount']:
                            user_assets_sr.wallex_transaction.increase_balance(
                                user_id=wallex_pay_record.user_id,
                                coin_name=coin.name,
                                input_type=wallex_pay_record.input_type,
                                input_unique_id=wallex_pay_record.input_unique_id,
                                amount=asset['amount'],
                                db=db
                            )
                            user_assets_sr.wallex_transaction.block_balance(
                                user_id=wallex_pay_record.user_id,
                                coin_name=coin.name,
                                input_type=wallex_pay_record.input_type,
                                input_unique_id=wallex_pay_record.input_unique_id,
                                amount=asset['amount'],
                                db=db
                            )
                    wallex_pay_agent.update_item(
                        db=db,
                        find_by={'token': token},
                        update_to={'status': wallex_pay_agent.STATUS_UNVERIFIED}
                    )
                else:
                    wallex_pay_agent.update_item(
                        db=db,
                        find_by={'token': token},
                        update_to={'status': wallex_pay_agent.STATUS_REJECTED_BY_SYSTEM}
                    )
            else:
                wallex_pay_agent.update_item(
                    db=db,
                    find_by={'token': token},
                    update_to={'status': wallex_pay_agent.STATUS_REJECTED_BY_USER}
                )
        else:
            raise SystemError('not found wallex pay record')

        return redirect_no_cache(url=redirect_response_url)

    except Exception as e:
        print(e)
        wallex_pay_agent.update_item(
            db=db,
            find_by={'token': token},
            update_to={'status': wallex_pay_agent.STATUS_REJECTED_BY_USER}
        )
        return redirect_no_cache(url=redirect_response_url)

from ext_services.jibit.interfaces.identity_validate import jibit_identity_agent
from ext_services.jibit.payment_gateway.token import (
    jibit_pay_gw_get_token,
    jibit_pay_gw_get_refresh_token
)
from ext_services.jibit.transferor.token import (
    jibit_transferor_get_refresh_token,
    jibit_transferor_get_token
)
from ext_services.sms_ir.sms_ir_interface import sms_ir_agent
from system.celery import app


@app.task
def jibit_identity_validation_refresh_token():
    try:
        jibit_identity_agent.jibit_get_refresh_token()
    except:
        jibit_identity_agent.jibit_get_token()


@app.task
def jibit_payment_gateway_refresh_token():
    try:
        jibit_pay_gw_get_refresh_token()
    except:
        jibit_pay_gw_get_token()


@app.task
def jibit_transferor_refresh_token():
    try:
        jibit_transferor_get_refresh_token()
    except:
        jibit_transferor_get_token()


@app.task
def sms_ir_token():
    try:
        sms_ir_agent.get_token()
    except:
        pass


@app.task
def finnotech_token():
    try:
        # finnotech_sr = FinnotechService()
        # finnotech_sr.token.get_token()
        pass
    except Exception as e:
        raise e

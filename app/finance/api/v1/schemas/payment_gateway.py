from pydantic import BaseModel, Field


class SendPayGwCreateRequest(BaseModel):
    bank_payment_id: int = \
        Field(...,
              title='Send Payment Gateway Request',
              description='Send Payment Gateway Request',
              example=1,
              )


class SendPayGwResponse(BaseModel):
    redirect_url: str = \
        Field(...,
              title='Send Payment Gateway URL',
              description='Send Payment Gateway URL',
              example="http://wwww.test.com/redirect_url",
              )


class PgwCallbackRequest(BaseModel):
    ref_num: str = \
        Field(...,
              title='payment gateway wallpay reference number',
              description='payment gateway wallpay reference number',
              example='aksjdh8-adskjb-87ascjhb-aslckn',
              )
    amount: int = \
        Field(...,
              title='Amount in Rial',
              description='Amount in Rial',
              example=1000,
              )
    psp_purchase_id: str = \
        Field(...,
              title='Psp Purchase Id',
              description='Psp Purchase Id',
              example='sdkjcbkjc987acdjb',
              )
    wage: int = \
        Field(...,
              title='Wage',
              description='Wage',
              example=100,
              )
    payer_ip: str = \
        Field(...,
              title='Payer IP',
              description='Payer IP',
              example='35.98.123.45',
              )
    callback_status: str = \
        Field(...,
              title='Callback Status',
              description='Callback Status',
              example='SUCCESS',
              )
    psp_ref_num: str = \
        Field(...,
              title='Psp reference Number',
              description='Psp reference Number',
              example='SUCCESS',
              )
    payer_masked_card_num: str = \
        Field(...,
              title='Payer Masked Card Number',
              description='Payer Masked Card Number',
              example='603799******6701',
              )
    psp_rrn: str = \
        Field(...,
              title='PSP RNN',
              description='PSP RNN',
              example='89768757654',
              )
    psp_name: str = \
        Field(...,
              title='PSP Name',
              description='PSP Name',
              example='89768757654',
              )



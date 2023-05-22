"""Modules providingFunctions"""
import os
from typing import List, Union

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    """
    we keep wallpay application main setting in this class
    """

    load_dotenv("../../.env")

    APP_NAME: str = "Wallpay Finance Services Application"
    APP_TIME_ZONE: str = os.environ.get("TZ", "Asia/Tehran")
    APP_ENV: str = os.environ.get("APP_ENV", "development")
    WALLPAY_BASE_URL: str = f"{os.environ.get('WALLPAY_BASE_URL', 'http://localhost:8000')}"

    FRONT_BASE_URL: str = f"{os.environ.get('FRONT_BASE_URL', 'http://localhost:3000')}"

    FRONT_FAIL_LANDING_URL: str = f"{FRONT_BASE_URL}/order/failed/"  # + order_uuid
    FRONT_SUCCESS_LANDING_URL: str = f"{FRONT_BASE_URL}/payment/success/"  # + order_uuid
    FRONT_COLLATERAL_CONFIRM_URL: str = f"{FRONT_BASE_URL}/collateral/"  # + order_uuid
    FRONT_ORDER_INFO_URL: str = f"{FRONT_BASE_URL}/order/"  # + order_uuid

    IS_REMOTE_SERVER: str = os.environ.get("IS_REMOTE_SERVER", "False")
    if IS_REMOTE_SERVER == "True":
        WALLPAY_BASE_URL = f"{os.environ.get('WALLPAY_BASE_URL', 'http://localhost:8000')}"

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:8000",
        "http://localhost:8001",
        "http://localhost:8002",
        "http://localhost:80",
        "https://api.dev.wallpay.org",
        "https://api.stage.wallpay.org",
        "https://api.wallpay.org",
        "https://payment.dev.wallpay.org",
        "https://payment.stage.wallpay.org",
        "https://payment.wallpay.org",
        "https://my.dev.wallpay.org",
        "https://my.stage.wallpay.org",
        "https://my.wallpay.org",
        "https://wallpay.surge.sh",
    ]  # type: ignore    # WalPay

    # App Config Data

    LTV_RISK_LABEL: dict = {0.9: "Low-Risk", 0.65: "Medium-Risk", 0.5: "High-Risk"}

    ORDER_EXPIRATION_TIME: int = 20  # type: ignore # minutes
    ORDER_REJECT_TIME: int = 60  # type: ignore # minutes

    # User & Authentication Settings
    ACCESS_TOKEN_SECRET_KEY: str = "4ab5be85c8c56eecdd547f7831979be83de58a6768d10a314f54cda4e4d67ffe789"
    REFRESH_TOKEN_SECRET_KEY: str = "E)H@McQfTjWnZr4t7w!z%C*F-JaNdRgUkXp2s5v8x/A?D(G+KbPeShVmYq3t6w9z$B&E)H@McQfTjWnZr4u7x!A%D*F-JaNdRgUkXp2s5v8y/B?E(H+KbPeShVmYq3t6"
    ACCESS_TOKEN_ALGORITHM: str = "HS256"
    REFRESH_TOKEN_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 2 * 60  # 2 hours
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 30 * 24 * 60  # 1 month
    MINIMUM_TIME_FOR_RENEW_REFRESH_TOKEN: int = 24  # hours

    OTP_TIME_OUT = 120  # sec
    OTP_MIN_TIME_TO_RESEND = 60  # sec

    DEFAULT_MOBILE_USER_USERNAME = "alis"
    DEFAULT_MOBILE_USER_PASSWORD = "Aa123456"
    DEFAULT_MOBILE_USER_MOBILE = "09001001010"

    # Kaveh Negar
    KAVENEGAR_API_KEY = (
        "4D566C7142793154542B3659314B2F306754367862483943777A304D61735A6A79383474644268526559553D"
    )

    # sms_ir
    SMS_IR_BASE_URL = "https://RestfulSms.com"
    SMS_IR_API_KEY = "9t5kKTE23XtBPmqwghjmclkxh+ko4f&()#%!&*@KyoWI+7nHpyMamGRltw"
    SMS_IR_SECRET_KEY = "203d82d1bd679847313978c6"
    SMS_IR_LINE_NUMBER = "30004747478407"
    SMS_IR_TOKEN = "random-skdjh"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    @classmethod
    def assemble_cors_origins(cls, orgin_address: Union[str, List[str]]) -> Union[List[str], str]:
        """
        this method get all valid origins from config list and append them to project config
        """
        if isinstance(orgin_address, str) and not orgin_address.startswith("["):
            return [i.strip() for i in orgin_address.split(",")]
        elif isinstance(orgin_address, (list, str)):
            return orgin_address
        raise ValueError(orgin_address)

    POSTGRES_USERNAME: str = os.environ.get("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB", "walfin")
    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT", "5432")

    POSTGRES_DATABASE_URL: str = (
        f"postgresql+psycopg2://"
        f"{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    # ORDER
    MINIMUM_PAY_ORDER_AMOUNT = 50000  # TMN
    MAXIMUM_PAY_ORDER_AMOUNT = 50000000  # TMN

    # JIBIT Identity Validation Service
    JIBIT_IDEN_VALID_BASE_URL = "https://napi.jibit.ir/ide"
    JIBIT_IDEN_VALID_API_KEY = "jDdJE_xQz6"
    JIBIT_IDEN_VALID_SECRET_KEY = "FX5StQAtmwB8ArGSk0N9z3i17"
    JIBIT_IDEN_VALID_ACCESS_TOKEN = "DKVDFVKKDNFVVKJNDVKJ3476"
    JIBIT_IDEN_VALID_REFRESH_TOKEN = "DKLJFNISDF03480438"

    # JIBIT Payment Gateway Service
    JIBIT_PAY_GW_BASE_URL = "https://napi.jibit.ir/ppg"
    JIBIT_PAY_GW_API_KEY = "D6is3wek10"
    JIBIT_PAY_GW_SECRET_KEY = "rhUAYwfn2TmkSsDjr0bbr49cpzp4Xm7_s2vwqPK7bdtQs3XHQP"
    JIBIT_PAY_GW_ACCESS_TOKEN = "DKVDFVKKDNFVVKJNDVKJ3476-random"
    JIBIT_PAY_GW_REFRESH_TOKEN = "DKLJFNISDF03480438-random"
    JIBIT_PAY_GW_CALLBACK_BASE_URL = WALLPAY_BASE_URL + "/api/v1/jibit/payment_gateway_callback"
    JIBIT_PAY_GW_EXPIRE_TIME = 19 * 60  # seconds

    # JIBIT Tranferor Service
    JIBIT_TRANSFEROR_BASE_URL = "https://napi.jibit.ir/trf"
    JIBIT_TRANSFEROR_API_KEY = "0Pfrq3atcE"
    JIBIT_TRANSFEROR_SECRET_KEY = "IyUwbXYp3YMe4h41drAZLqvKe"
    JIBIT_TRANSFEROR_ACCESS_TOKEN = "fgh-random"
    JIBIT_TRANSFEROR_REFRESH_TOKEN = "df-random"

    # Wallex login
    WALLEX_API_BASE_UERL = "https://api.wallex.ir"
    CALLBACK_URL_FROM_WALLEX_LOGIN = WALLPAY_BASE_URL + "/api/v1/user/login/wallex-callback"
    WALLEX_LOGIN_CLIENT_ID = os.getenv(
        "WALLEX_LOGIN_CLIENT_ID", "83ceb6c9-ee56-4ac2-938c-451f4087d3f1"
    )
    WALLEX_LOGIN_CLIENT_SECRET = os.getenv(
        "WALLEX_LOGIN_CLIENT_SECRET", "iIbrPeZLkjilUisuBgnjXtfG5zB1qZbNWDbBAPKB"
    )
    WALLEX_MAX_SECONDS_FOR_LOGIN = 5  # min

    # Wallex pay
    WALLEX_PAY_API_KEY = os.getenv("WALLEX_PAY_API_KEY", "gXJsQ4FXIllU6iOohlKZ")
    WALLEX_PAY_CALLBACK = WALLPAY_BASE_URL + "/api/v1/user-assets/wallex/callback"

    # Wallex address management
    WALLEX_ADDRESS_MANAGEMENT_BASE_URL = (
        "https://wallpay-address-management-blockchain.k8s.ecoex.ir"
    )
    WALLEX_ADDRESS_MANAGEMENT_USERNAME = "94bHdJPgaSRAJWiioTws85h5wmsHp73Bd8Qn2bsd"
    WALLEX_ADDRESS_MANAGEMENT_PASSWORD = "5hR4OXd6pQv7vUH3AL9E0Mqr84v7uj3iKVNY7jeC"

    # Boton Rabbitmq
    BOTON_HOST = "31.7.66.213"
    BOTON_PORT = "10008"
    BOTON_RABBIT_USERNAME = "wallpay_app"
    BOTON_RABBIT_PASSWORD = "7#L59XjD8^Z2X$qt5xEWto#*"
    BOTON_RABBIT_VHOST = "wallpay"

    # Finnotech
    FINNOTECH_BASE_URL: str = "https://apibeta.finnotech.ir"
    FINNOTECH_CLIENT_ID: str = "wallpay"
    FINNOTECH_CLIENT_SECRET: str = "UPx5rJQtT0Hx1hmM8w0e"
    FINNOTECH_SCOPES = ("credit:back-cheques:get",)  # "scope1;scope2;scope3"
    FINNOTECH_PANEL_NATIONAL_CODE = ("1142332209",)
    FINNOTECH_ACCESS_TOKEN = (
            "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9."
            + "eyJ0b2tlbklkIjoiMzQ1NDlhY2MtNDMxMi00ZjAzLWJiNDU"
            + "tNGI2NmM2NDJjODVlIiwicmVmcmVzaFRva2VuIjoiaDJpVkJ2aUxiN"
            + "UxaYk5VOFhxY0JvalhHMWYxdmtKZXRIU0FYWFJ6aHM5WDQzOW9Ic0tt"
            + "RXZaM1NmMUpSWmc3dEN0Rkt3aURPTUFIY21LUXFkUWtaTmFQazhyWkR0"
            + "R05RemEzUmlzTTBQV0hNdVVxbXdqQnNaWDY5RklZbloxT3dBbXdsNTRlU"
            + "kxvZFRBMVVpaW1Oc3RFSVZzOU9wOGZWd3BHSGptemY4RVpLU3lHRzZoczZ"
            + "aUE5KeUtIakdnNGpZQmZuUVZFdFJidEFFaTI2SURwSHh6TmZIMTJxVG1TZT"
            + "R2eVdwUnRQaWJvTTF0MFRjR21wVDY3VGhHR2dia05sSSIsImNyZWF0aW9uRG"
            + "F0ZSI6IjE0MDExMDAzMDc0NjUzIiwibGlmZVRpbWUiOjg2NDAwMDAwMCwiY2x"
            + "pZW50SWQiOiJ3YWxscGF5IiwidXNlcklkIjoiMTE0MjMzMjIwOSIsImFjdGl2Z"
            + "SI6dHJ1ZSwic2NvcGVzIjpbImNyZWRpdDpiYWNrLWNoZXF1ZXM6Z2V0Il0sInR5"
            + "cGUiOiJDTElFTlQtQ1JFREVOVElBTCIsImNsaWVudEluZm8iOiJoMkt3WlVXY2Qz"
            + "aGZEaDUyZWVYYU5KeFFwVHU2Sk43UTV1OE5DTTZuIiwiYmFuayI6IjA2MiIsImlhd"
            + "CI6MTY3MTg1NTQxMywiZXhwIjoxNjcyNzE5NDEzfQ.cjPjAu9qq8TtN-F4IYMB3CkN"
            + "yuKibX92iAbGNWEFUhl3WmydMSp92izytBPmsBG675aX-73vvlWdzn-qgweMCFex8Bs"
            + "aRGnKKemKG0-AJX89SFDPJXoKNj4fMsjZl1Y3rNZxn3N29nRcFGxDPXqW2neejlwC9EN"
            + "sD4gXOBYuzgtdV2ZC_9VelsT58W0USntWgsiNlx1Ov0AgdqtALfp3NwHEuG5Ghs4NYlF0"
            + "VzyEVDhzPW9boj11ZVQ-hnJCguzlHjYEzmSqtgwD4LA2j6nQ_encTjD-JJaCDyk0RlQ918"
            + "y09NK4FcK2ZdltPCNJW9ctc5ae5mPrpgTEW8HCcyMYZQ"
    )
    FINNOTECH_REFRESH_TOKEN = (
            "h2iVBviLb5LZbNU8XqcBojXG1f1vkJetHSAXXRzhs9X439oHsKmEvZ3Sf1J"
            + "RZg7tCtFKwiDOMAHcmKQqdQkZNaPk8rZDtGNQza3RisM0PWHMuUqmwjBsZX69FIYnZ1OwAmwl54eRLodTA1U"
            + "iimNstEIVs9Op8fVwpGHjmzf8EZKSyGG6hs6ZPNJyKHjGg4jYBfnQVEtRbtAEi26IDpHxzNfH12qTmSe4vy"
            + "WpRtPiboM1t0TcGmpT67ThGGgbkNlI"
    )

    # Finance Bank Payment
    MINIMUM_BANK_PAYMENT_AMOUNT: int = 100000  # Rial
    MAXIMUM_BANK_PAYMENT_AMOUNT: int = 250000000  # Rial

    # Finance Reverse
    MAXIMUM_DIFF_TIME_TO_REVERSE: int = 60  # minute

    # Finance Settlement
    MINIMUM_MERCHANT_SETTLEMENT_AMOUNT: int = 1000000  # Rial

    # Credit Base Settings
    BASE_FREE_CREDIT: int = 3000000  # Rial

    # Firebase token
    FIREBASE_CERTIFICATION: dict = {
        "type": os.environ.get('FIREBASE_TYPE', 'service_account'),
        "project_id": os.environ.get('FIREBASE_PROJECT_ID', 'wallpay-bf458'),
        "private_key_id": os.environ.get('FIREBASE_PRIVATE_KEY_ID', '04899d2998e50cf197e8fe6af813e559582e19a5'),
        "private_key": os.environ.get('FIREBASE_PRIVATE_KEY',
                                      "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCyHKX0XGLmybmv\nNjOztsf5Ob/mTasZI6djWsdPy73Awf14q0S/uCaSc16ol/Zr6i9eNTh4qIFm67vL\n4Zy36al8aqEi/ceFPwIy/HaCBq81VMBJnaFCMTU7VioaCYgKM4wVGD6nMScgxat7\nwnKg7od2/g67dljd0RoRlLgz/WSx4vvkr2FMxyg8FM5MFyqESEUuEHUZ5TlBLz9U\nBf44k/1/TOMP8TSdN2BMDpU2wBGYn2y5FR3Lj5gLetAGwBxGe59o7dOIjQK+BRiX\nrbM1nu9MPamwyrkfOy+wrepiuohgl45QPuFEnZaECe3/RaaHu/emLWYR1FGa6L6m\nt7oD8VIPAgMBAAECggEATpnQ7NUmejW0oWtYhqsXddcz5hUJeDchQ/nIMmE1tI6H\nZsyiMr84GnIaaGljgH0g+UCgUrL+JCbMwe0nBYxy1KqTwMbg2V8Uf96lB72ebXkg\nwHv1MapYlP5x5vqk0+eqnpaL86l/3HkPM7b8ciPBmVQFuVnBXuZLzE1mut7MpKlK\n1IRa0ubO/tNFx4TenBgdzD19WAMR72ct/vTIr15qOPhXoG4OcxjtCFw3l9nq7SaM\nS+rG0PK3a47tctJDPTnaZQGs601O4aM3z0yien7civ8S/XNJGs1bQu3R0gnuP8Vt\nzyMsyJApk7+xOtY+CpvtRzPhlbdXiqxqMT1UZ9wspQKBgQDsQm5uBwBuWcRURtT3\nyRm45SFR0V0DyD1SYoEmDZiys7MAIj0ETVEgshY9TKaFXSRe/JGz1q/Sinzrg1wg\n2HQGJ6hoF8NlkJqguaE/UnSn61MQ6AL7bT6aMpii1PARWek3WcdZvvhfm/QwpsSh\nJpyLUMRxwQc13SmpEgh0FezxOwKBgQDA/nIC6lfSUmz5KDrPd0DIeyoDXVjktg87\n4n7QtGam2jgIH+9M59m/uHqqRwlY1LAZ+DLbu3nY3BoiKFrecy9VCY8VOgnqFsb1\nYLKthwkF8d0lomJb/JeeRCvRWN6jthqTYN8aHoeeO0GPNO8t+VEHOulVqyLlMGD2\nauV05PYVPQKBgQCLzCdBzbzQjydf4uXDlOg2gsY7fpH2WfcHF6hp1uPC4hgJ/Thz\nojheC2KjdQaXpWyPFA43BtLU1wNh7EGIYewNdEvvBBinsW/9qLmkGWtTrShiuZaC\nJbtETKoKt8sxySz5hpMyJJEdKc/NNfDllk5NFUaYNOrKUYqEM1pzLkIc3wKBgENF\nbgBOJyaMzKdcuoMukkpPhCmAFEhEnbLGFGYzO8TVM8rBNuybtG77ouZPtJZeLLQg\nq7mj86j/r6xQXLxFci42EsXXYTVTky5c8mtCMob785X2sEpYFZF5ObzTOWffRgwx\nLBMyqRsilIuSa/yedvwKMONHr/YrkuDSCgFg/dYRAoGBALoQ65SaVrf9OjwpQzm4\nup0Ezmpkf2VtqGi0yIRSRG96Z5/BV/jnQ4XzsTcVC7rn0WLsWkTeIxgba0X9YsXM\nQwp2Lf+Tk0RIJhXDGA7yKmtPbvwMUx6FujXTd9LGuUX+/FCZOpX71XWFooK+41KW\nOL0IF6AEvoiCZl6SUcs7Zh73\n-----END PRIVATE KEY-----\n"),
        "client_email": os.environ.get('FIREBASE_CLIENT_EMAIL',
                                       "firebase-adminsdk-2scgt@wallpay-bf458.iam.gserviceaccount.com"),
        "client_id": os.environ.get('FIREBASE_CLIENT_ID', "114805167358342915910"),
        "auth_uri": os.environ.get('FIREBASE_AUTH_URI', "https://accounts.google.com/o/oauth2/auth"),
        "token_uri": os.environ.get('FIREBASE_TOKEN_URI', "https://oauth2.googleapis.com/token"),
        "auth_provider_x509_cert_url": os.environ.get('FIREBASE_AUTH_PROVIDER_X509_CERT_URL',
                                                      "https://www.googleapis.com/oauth2/v1/certs"),
        "client_x509_cert_url": os.environ.get('FIREBASE_CLIENT_X509_CERT_URL',
                                               "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-2scgt%40wallpay-bf458.iam.gserviceaccount.com")
    }


settings = Settings()

finance_scopes = {
    "finance:payment-gateway:all": {
        "name": 'finance:payment-gateway:all',
        "fa_name": '',
        "description": 'خواندن کلیه رکوردهای درگاه پرداخت',
        "module": 'finance',
        "interface": 'payment_gateway',
        "endpoint": 'all_bank_payments',
        "action": 'get'
    },
    "merchant:sales_monitoring_pgw": {
        "name": 'finance:merchant:sales_monitoring_pgw',
        "fa_name": '',
        "description": '',
        "module": '=',
        "interface": '=',
        "endpoint": '=',
        "action": ''
    },
    "merchant:sales_monitoring_credit": {
        "name": 'finance:merchant:sales_monitoring_credit',
        "fa_name": '',
        "description": '',
        "module": '=',
        "interface": '=',
        "endpoint": '=',
        "action": ''
    },
    "merchant:unsettled": {
        "name": 'finance:merchant:unsettled',
        "fa_name": '',
        "description": '',
        "module": '=',
        "interface": '=',
        "endpoint": '=',
        "action": ''
    },
    "merchant:transfers": {
        "name": 'finance:merchant:transfers',
        "fa_name": '',
        "description": '',
        "module": '=',
        "interface": '=',
        "endpoint": '=',
        "action": ''
    },
    "merchant:transfer_detail": {
        "name": 'finance:merchant:transfer_detail',
        "fa_name": '',
        "description": '',
        "module": '=',
        "interface": '=',
        "endpoint": '=',
        "action": ''
    },

    "finance:refund:refund-detail": {
        "name": "finance:refund:refund-detail",
        "fa_name": "",
        "description": "اطلاعات مربوط به ریفاند",
        "module": "finance",
        "interface": "refund_detail",
        "endpoint": "refund-detail",
        "action": "get"
    },

    "finance:bank-profile:create-user-bank-profile": {
        "name": "finance:bank-profile:create-user-bank-profile",
        "fa_name": "",
        "description": "ایجاد پروفایل بانکی",
        "module": "finance",
        "interface": "create_user_bank_profile",
        "endpoint": "create-user-bank-profile",
        "action": "post"
    },

    "finance:refund:submit-refund-after-add-bank-profile": {
        "name": "finance:refund:submit-refund-after-add-bank-profile",
        "fa_name": "",
        "description": "کاربر بعد از تایید کارت بانکی خود با این ای پی ای میتواند فرایند ریفاند را کامل کند",
        "module": "finance",
        "interface": "submit_refund_after_add_bank_profile",
        "endpoint": "submit-refund-after-add-bank-profile",
        "action": "post"
    },
    "merchant:dashboard": {
        "name": 'finance:merchant:dashboard',
        "fa_name": '',
        "description": '',
        "module": '=',
        "interface": '=',
        "endpoint": '=',
        "action": ''
    },

    "finance:refund:refund": {
        "name": "finance:refund:refund-detail",
        "fa_name": "",
        "description": "",
        "module": "finance",
        "interface": "refund",
        "endpoint": "refund",
        "action": "post"
    },
}

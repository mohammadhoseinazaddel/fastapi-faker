user_asset_scopes = {
    "wallet:asset-detail": {
        "name": "wallet:asset-detail",
        "fa_name": "",
        "description": "خواندن جزییات ولت کاربر",
        "module": "user_asset",
        "interface": "wallet",
        "endpoint": "x",
        "action": "get"
    },

    "wallet:address:deposit": {
        "name": "wallet:address:deposit",
        "fa_name": "",
        "description": "گرفتن ادرس ولت کاربر",
        "module": "user_asset",
        "interface": "wallet",
        "endpoint": "get_deposit_address",
        "action": "get"
    },

    "wallet:address:verify": {
        "name": "wallet:address:verify",
        "fa_name": "",
        "description": "تایید ادرس ولت",
        "module": "user_asset",
        "interface": "wallet",
        "endpoint": "verify_address",
        "action": "get"
    },

    "wallet:withdraw": {
        "name": "wallet:withdraw",
        "fa_name": "",
        "description": "برداشت از ولت",
        "module": "user_asset",
        "interface": "wallet",
        "endpoint": "withdraw_request",
        "action": "post"
    },

}

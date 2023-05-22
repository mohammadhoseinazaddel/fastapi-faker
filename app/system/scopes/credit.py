credit_scopes = {
    "credit:score:me": {
        "name": "credit:score:me",
        "fa_name": "",
        "description": "خواندن کردیت اسکور من",
        "module": "credit",
        "interface": "score",
        "endpoint": "get_user_credit_score",
        "action": "get"
    },

    "credit:info": {
        "name": "credit:info",
        "fa_name": "",
        "description": "خواندن اطلاعات مرتبط با کردیت من",
        "module": "credit",
        "interface": "user",
        "endpoint": "info",
        "action": "get"
    },
    "credit:user:all": {
        "name": "credit:user:all",
        "fa_name": "",
        "description": "خواندن کردیت های یوزر",
        "module": "credit",
        "interface": "user",
        "endpoint": "user_all_credits",
        "action": "get"
    },

}

order_scopes = {
    "fund:DebtDetail": {
        "name": "fund:DebtDetail",
        "fa_name": "",
        "description": "خواندن دیتیل بدهی مربوط به فاند",
        "module": "order",
        "interface": "fund",
        "endpoint": "debt_detail",
        "action": "get"
    },

    "fund:Repay": {
        "name": "fund:Repay",
        "fa_name": "",
        "description": "بازپرداخت فاند",
        "module": "order",
        "interface": "fund",
        "endpoint": "repay",
        "action": "post"
    },

    "fund:get-collateral": {
        "name": "fund:get-collateral",
        "fa_name": "",
        "description": "خواندن وثیقه های فاند",
        "module": "order",
        "interface": "fund",
        "endpoint": "get_collateral",
        "action": "get"
    },

    "order:pay:create": {
        "name": "order:pay:create",
        "fa_name": "",
        "description": "ایجاد سفارش توسط مرچنت",
        "module": "order",
        "interface": "pay",
        "endpoint": "create_order",
        "action": "post"
    },

    "order:pay:process": {
        "name": "order:pay:process",
        "fa_name": "",
        "description": "پردازش سفارش",
        "module": "order",
        "interface": "pay",
        "endpoint": "process_order",
        "action": "post"
    },

    "order:pay:all-orders": {
        "name": "order:pay:all-orders",
        "fa_name": "",
        "description": "خواندن همه سفارش ها",
        "module": "order",
        "interface": "pay",
        "endpoint": "all_orders",
        "action": "get"
    },

    "order:pay:user-orders": {
        "name": "order:pay:user-orders",
        "fa_name": "",
        "description": "خواندن همه سفارش های کاربر",
        "module": "order",
        "interface": "pay",
        "endpoint": "all_user_orders",
        "action": "get"
    },

    "order:pay:my-orders": {
        "name": "order:pay:my-orders",
        "fa_name": "",
        "description": "test",
        "module": "order",
        "interface": "pay",
        "endpoint": "my-orders",
        "action": "get"
    },
    "finance:refund:refund": {
        "name": "finance:refund:refund",
        "fa_name": "",
        "description": "just merchant admin can call this api and the result is the order will refund",
        "module": "order",
        "interface": "refund",
        "endpoint": "refund",
        "action": "post"
    },

    "merchant:all": {
        "name": "order:merchant:all",
        "fa_name": "خریدها",
        "description": "Can view all orders.",
        "module": "order",
        "interface": "merchant",
        "endpoint": "all",
        "action": "get"
    }

}

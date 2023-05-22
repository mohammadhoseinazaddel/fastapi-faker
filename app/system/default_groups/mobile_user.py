mobile_user_scopes = \
    [
        # add MOBILE USER scopes here
        # "user:get",  # Example

        # User APIs
        "user:get",

        # BlockChain APIs
        "wallet:address:deposit",
        "wallet:address:verify",
        "wallet:withdraw",

        "wallet:asset_estimate",
        "wallet:user_asset_list",

        "fund:user_total_debt",
        "fund:processOrder",
        "fund:defaultBlockedCollateral",
        "fund:changeOrderCollateral",
        "fund:user_credit",
        "fund:submitOrder",
        "fund:DebtDetail",
        "fund:Repay",
        "fund:get-collateral"

        # credit
        "credit:score:me",
        "credit:info",

        "order:pay:create",
        "order:pay:process",
        "order:pay:my-orders",
        'wallet:asset-detail',

        # notification
        "notification:notification_center:me",
        "notification:notification_center:seen",

        # finance
        "finance:refund:refund-detail",
        "finance:send_pay_gw",
        "finance:bank-profile:create-user-bank-profile",
        "finance:refund:submit-refund-after-add-bank-profile"

    ]

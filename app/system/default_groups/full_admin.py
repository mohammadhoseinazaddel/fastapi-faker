from typing import List, Dict

from ..scopes import (
    credit,
    finance,
    order,
    user_asset,
    user,
    notification
)


def create_scope_name_list(
    scope: Dict[str, Dict[str, str]],
    module: str = None
) -> List[str]:
    if module:
        return [v["name"] for k, v in scope.items() if k.split(":")[0] == module]
    return [v["name"] for v in scope.values()]

class FullAdminScopes:
    
    def __init__(self) -> None:
        self.credit = create_scope_name_list(credit.credit_scopes)
        self.finance = create_scope_name_list(finance.finance_scopes)
        self.order = create_scope_name_list(order.order_scopes)
        self.user_asset = create_scope_name_list(user_asset.user_asset_scopes)
        self.user = create_scope_name_list(user.user_scopes)
        self.notification = create_scope_name_list(notification.notification_scopes)
        
        
    def aslist(self) -> List[str]:
        return (self.credit +
                self.finance +
                self.order +
                self.user_asset +
                self.user + 
                self.notification)
        
        
full_admin_scopes = FullAdminScopes()


full_admin_user_scopes = full_admin_scopes.aslist()

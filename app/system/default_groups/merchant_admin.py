from typing import List

from ..default_groups.full_admin import create_scope_name_list
from ..scopes import (
    credit,
    finance,
    order,
    user_asset,
    user
)


class MerchantScopes:
    
    def __init__(self) -> None:
        self.credit = create_scope_name_list(credit.credit_scopes, 'merchant')
        self.finance = create_scope_name_list(finance.finance_scopes, 'merchant')
        self.order = create_scope_name_list(order.order_scopes, 'merchant')
        self.user_asset = create_scope_name_list(user_asset.user_asset_scopes, 'merchant')
        self.user = create_scope_name_list(user.user_scopes, 'merchant')
        
        
    def aslist(self) -> List[str]:
        return (self.credit +
                self.finance +
                self.order +
                self.user_asset +
                self.user)
        
        
merhcant_scopes = MerchantScopes()

merchant_admin_group_scopes = merhcant_scopes.aslist()

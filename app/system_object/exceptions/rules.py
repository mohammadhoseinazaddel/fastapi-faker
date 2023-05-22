from system.base.exceptions  import Error
from fastapi import status


#  CRUD exceptions
class RulesNotFound(Error):
    def __init__(self, ):
        super().__init__(
            message="Rules not found.",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'قوانین وجود ندارد',
                'field': '',
                'type': ''
            }
        )

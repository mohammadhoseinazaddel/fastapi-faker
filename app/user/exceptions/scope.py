from system.base.exceptions  import Error
from fastapi import status


#  scope CRUD exceptions
class ScopeExists(Error):
    def __init__(self, ):
        super().__init__(
            message="scope with this name already exists.",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'scope with this name already exists.',
                'field': '',
                'type': 'Scope.Exists'
            }
        )


class GroupNotFound(Error):
    def __init__(self, ):
        super().__init__(
            message="Group Not Found.",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'Group Not Found.',
                'field': '',
                'type': 'Group.NotFound'
            }
        )


class GroupCanNotDelete(Error):
    def __init__(self, ):
        super().__init__(
            message="GroupCanNotDelete",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'group can not be deleted, because some users use it',
                'field': '',
                'type': 'group can not be deleted, because some users use it'
            }
        )
from system.base.exceptions  import Error
from fastapi import status


#  group CRUD exceptions
class GroupExists(Error):
    def __init__(self, ):
        super().__init__(
            message="Group with this name already exists.",
            errors={
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': 'Group with this name already exists.',
                'field': '',
                'type': 'Group.Exists'
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
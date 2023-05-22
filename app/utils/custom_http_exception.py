class CustomHttpException(Exception):
    """
        CUSTOM PARAMS:
            status_code: int,
            message: str,
            field: list,
            type_: str,

        OUR EXCEPTION CLASSES:
            exception_obj: Error() = None
    """

    def __init__(
            self,
            **kwargs,
    ):
        if "exception_obj" not in kwargs.keys():
            list_of_keys = [
                'status_code',
                'message',
                'field',
                'type_'
            ]
            if list_of_keys != list(kwargs.keys()):
                raise Exception('"status_code", "message", "field", "type_" should be sent as argument')
            self.status_code = kwargs['status_code']
            self.detail = {
                "success": "true",
                "errors": [
                    {
                        "code": kwargs['status_code'],
                        "message": kwargs['message'],
                        "field": kwargs['field'],
                        "type": kwargs['type_']
                    }
                ],
                "data": []
            }

        else:
            exception_obj = kwargs['exception_obj']
            self.status_code = exception_obj.errors['code']
            self.detail = {
                "success": "true",
                "errors": [
                    {
                        "code": exception_obj.errors['code'],
                        "message": exception_obj.errors['message'],
                        "field": exception_obj.errors['field'],
                        "type": exception_obj.errors['type']
                    }
                ],
                'data': []
            }

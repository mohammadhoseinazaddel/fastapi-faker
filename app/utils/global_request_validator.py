from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


async def global_request_validator(request, exc):
    """
    Validates the request data and returns a dictionary with the validation results.
    """
    validation_errors = []
    errors = exc.errors()
    for error in errors:
        error_detail = {
            'name': error['loc'][1],
            'msg': error['msg']
        }
        validation_errors.append(error_detail)

    validation_results = {
        "success": False,
        "errors": {
            'type': 'validation-error',
            'msg': 'given data is not valid format',
            'fields': validation_errors
        },
        "data": []
    }
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(validation_results)
    )


global_422_response_model = {
    'description': 'Request Validation Error',
    'content': {
        'application/json': {
            'example': {
                "success": False,
                "errors": {
                    'type': 'error type',
                    'msg': 'error message',
                    'fields': [{'name': 'username', 'msg': 'this field is required'}]
                },
                "data": []
            }
        }
    }
}

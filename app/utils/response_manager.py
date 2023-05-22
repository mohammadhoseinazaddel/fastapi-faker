import traceback
from typing import Dict, Any, ClassVar

import pydantic
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from system.base.exceptions import Error
from .response_model import ResponseModel, ResponseModelList, PaginationModel, PaginationDisableModel, PaginationT


class ResponseManager:
    """
    """

    def __init__(
            self,
            response_model: Any = None,
            request_model: Any = None,
            pagination: bool = False,
            pagination_data: Dict = None,
            is_mock: bool = True,
            is_list: bool = False
    ):
        self.is_list = is_list
        self._response_model = response_model
        self._request_model = request_model
        self._pagination = pagination
        self._pagination_data = pagination_data
        self._is_mock = is_mock
        self._status_code = 200
        self._reset_response_data()

    def _create_mock_response(self):
        schema = self._response_model.schema()
        properties = schema["properties"]
        mock_data = {}
        self._response["data"] = []
        for key, value in properties.items():
            mock_data.update({key: value["example"]})
        self._response["data"].append(mock_data)

    def _reset_response_data(self):
        self._response = {
            "success": True,
            "pagination": {"is_enable": False},
            "errors": None,
            "data": None
        }

    def _pre_response(self):
        self._reset_response_data()
        self.process_pagination()

    def response_model(self) -> ClassVar[ResponseModel]:
        pagination_model: PaginationT = PaginationModel if self._pagination else PaginationDisableModel
        if self.is_list:
            return ResponseModelList[self._response_model, pagination_model]
        else:
            return ResponseModel[self._response_model, pagination_model]

    def request_model(self):
        return self._request_model

    def process_pagination(self):
        if self._pagination:
            self._response["pagination"] = self._pagination_data

    def status_code(self, status_code: int):
        self._status_code = status_code

    def pagination_data(self, total_count: int, current_page: int, page_size: int):
        self._pagination_data = {
            "is_enable": True,
            "total_count": total_count,
            "current_page": current_page,
            "page_size": page_size,
            "total_page": (total_count // page_size) + (1 if total_count % page_size else 0)
        }

    def response(self, data: Any = None):
        self._pre_response()
        if self._is_mock:
            self._create_mock_response()
        else:
            if type(data) is object:
                decode_data = jsonable_encoder(data)
                self._response["data"] = self._response_model(**decode_data).dict()
            if type(data) is dict:
                self._response["data"] = self._response_model(**data).dict()
            if type(data) is list:
                self._response['data'] = []
                for dict_ in data:
                    validated_dict = self._response_model(**dict_).dict()
                    self._response['data'].append(validated_dict)

        return JSONResponse(
            status_code=self._status_code,
            content=jsonable_encoder(self._response)
        )

    def exception(self, e):
        self._reset_response_data()
        self._response["success"] = False

        error_base = {
            'type': 'system-error',
            'msg': 'server internal error',
            'fields': []
        }
        self.status_code(500)
        if isinstance(e, Error):
            error_base['type'] = e.errors['type'] if 'type' in e.errors else ''
            error_base['msg'] = e.errors['message']
            self.status_code(e.errors['code'])
        elif isinstance(e, pydantic.ValidationError):
            for error in e.raw_errors:
                print(error)
        else:
            traceback.print_exc()

        self._response["errors"] = error_base

        return JSONResponse(
            status_code=self._status_code,
            content=jsonable_encoder(self._response)
        )

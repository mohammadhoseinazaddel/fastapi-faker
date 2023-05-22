from typing import List, Generic, TypeVar, Optional

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')
PaginationT = TypeVar('PaginationT')


class PaginationModel(BaseModel):
    is_enable: bool = \
        Field(default=True,
              title='Is enable pagination',
              description='Is enable pagination'
              )
    total_page: Optional[int] = \
        Field(default=0,
              title='Total page',
              description='Total page'
              )
    total_count: Optional[int] = \
        Field(default=0,
              title='Total count',
              description='Total count'
              )
    current_page: Optional[int] = \
        Field(default=1,
              title='Current page',
              description='Current page'
              )
    page_size: Optional[int] = \
        Field(default=10,
              title='Page size',
              description='Page size'
              )


class PaginationDisableModel(BaseModel):
    is_enable: bool = \
        Field(default=False,
              title='Is enable pagination',
              description='Is enable pagination'
              )


class ErrorModelFields(BaseModel):
    pass


class ErrorModel(BaseModel):
    message: str = \
        Field(...,
              title='Error Message',
              description='Error message',
              example='Bad Request'
              )
    type: str = \
        Field(...,
              title='Error Type',
              description='Error type',
              example='string'
              )

    fields: List[ErrorModelFields]


class ResponseModel(GenericModel, Generic[DataT, PaginationT]):
    success: bool = True
    pagination: PaginationT
    errors: ErrorModel = None
    data: Optional[DataT]

    class Config:
        exclude = True


class ResponseModelList(GenericModel, Generic[DataT, PaginationT]):
    success: bool = True
    pagination: PaginationT
    errors: ErrorModel = None
    data: Optional[List[DataT]]

    class Config:
        exclude = True

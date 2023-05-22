import datetime
from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy import exc
from sqlalchemy.orm import Session
from system.base.crud import CRUDBase
from system.base.exceptions import Error
from system.base.mixins import InterfaceLifeCycle

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
GetMultiSchemaType = TypeVar("GetMultiSchemaType", bound=BaseModel)


class InterfaceBase(InterfaceLifeCycle):

    def __init__(
            self,
            crud: CRUDBase,
            create_schema,
            update_schema,
            get_multi_schema=None,
            exceptions=False

    ):
        # self._open_session = OpenSession.open_session()
        self.crud = crud
        self.create_schema = create_schema
        self.update_schem = update_schema
        self.get_multi_schema = get_multi_schema

    def add_item(self, db: Session, **kwargs):
        try:
            return self.crud.create(obj_in=self.create_schema(**kwargs), db=db)
        except exc.IntegrityError as e:
            class BaseAlreadyExistsException(Error):
                def __init__(self, model_name=self.crud.model.__name__):
                    super().__init__(
                        # message=f"{model_name} already exists",
                        message=e.orig,
                        errors={
                            'code': 422,
                            'type': 'validation-error',
                            'message': 'آیتم درخواستی شما در حال حاضر وجود دارد',
                        }
                    )

            raise BaseAlreadyExistsException
        except Exception as e:
            raise e

    def find_item_multi(
            self,
            db: Session,
            raise_not_found_exception=True,
            soft_delete: bool = True,
            return_first_obj=False,
            **kwargs):
        try:
            filter_obj_dict = self.get_multi_schema(**kwargs).dict()
            for key in kwargs.keys():
                if key not in filter_obj_dict.keys() and key not in ['order_by', 'limit', 'skip']:
                    raise SystemError(f'can not find {key} in get multi schema')
            if soft_delete:
                objects = self.crud.get_multi(
                    db=db,
                    filter_obj=self.get_multi_schema(deleted_at__isnull=True, **kwargs),
                    order_by=kwargs['order_by'] if 'order_by' in kwargs.keys() else None,
                    skip=kwargs['skip'] if 'skip' in kwargs.keys() else None,
                    limit=kwargs['limit'] if 'limit' in kwargs.keys() else None,
                )
            else:
                objects = self.crud.get_multi(
                    db=db,
                    filter_obj=self.get_multi_schema(**kwargs),
                    order_by=kwargs['order_by'] if 'order_by' in kwargs.keys() else None,
                    skip=kwargs['skip'] if 'skip' in kwargs.keys() else None,
                    limit=kwargs['limit'] if 'limit' in kwargs.keys() else None,
                )

            if not objects and raise_not_found_exception:
                class BaseNotFoundException(Error):
                    def __init__(self, model_name=self.crud.model.__name__):
                        super().__init__(
                            message=f"{model_name} object not found",
                            errors={
                                'code': 404,
                                'message': 'آیتم درخواستی شما وجود ندارد',
                            }
                        )

                raise BaseNotFoundException
            db.flush()

            if return_first_obj and objects:
                return objects[0]
            return objects
        except Exception as e:
            raise e

    def update_item(self, db: Session, find_by: dict, update_to: dict):
        return self.crud.update_v2(
            db=db,
            filter_obj=self.get_multi_schema(**find_by),
            obj_in=self.update_schem(**update_to)
        )

    def delete_item(self, db: Session, find_by: dict, hard_delete=False):
        if hard_delete:
            self.crud.remove(db=db, filter_obj=self.get_multi_schema(**find_by))

        else:
            self.update_item(db=db, find_by=find_by, update_to={'deleted_at': datetime.datetime.now()})

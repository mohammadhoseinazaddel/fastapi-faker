from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, Literal

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
GetMultiSchemaType = TypeVar("GetMultiSchemaType", bound=BaseModel)


class CRUDBase(
    Generic[
        ModelType,
        CreateSchemaType,
        UpdateSchemaType,
        GetMultiSchemaType
    ]
):

    def __init__(
            self,
            model: Type[ModelType],
    ):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self._query: Session.query

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def _execute_query(self, action_name: str, *args, **kwargs):
        """
            This method execute your query based on your action like all(), remove() or ...
        """
        return getattr(self._query, action_name)(*args, **kwargs)

    def _prepare_get_multi_query(
            self,
            db: Session,
            filter_obj: GetMultiSchemaType = None,
            order_by: (str, Literal['asc', 'desc']) = None,
            skip: int = None,
            limit: int = None
    ) -> Session.query:
        try:
            query = db.query(self.model)
            if filter_obj:
                for key, value in filter_obj.dict().items():
                    if value is not None:
                        if "__isnull" in key:
                            attr = getattr(self.model, str(key).replace("__isnull", ""))
                            if value == True:
                                query = query.filter(attr == None)
                            if value == False:
                                query = query.filter(attr != None)
                        elif "__gt" in key:
                            attr = getattr(self.model, str(key).replace("__gt", ""))
                            query = query.filter(attr > value)
                        elif "__gte" in key:
                            attr = getattr(self.model, str(key).replace("__gte", ""))
                            query = query.filter(attr >= value)
                        elif "__lt" in key:
                            attr = getattr(self.model, str(key).replace("__lt", ""))
                            query = query.filter(attr < value)
                        elif "__lte" in key:
                            attr = getattr(self.model, str(key).replace("__lte", ""))
                            query = query.filter(attr <= value)
                        else:
                            attr = getattr(self.model, key)
                            query = query.filter(attr == value)
            if order_by:
                if order_by[1] == 'desc':
                    attr = getattr(self.model, order_by[0])
                    query = query.order_by(desc(attr))
                if order_by[1] == 'asc':
                    attr = getattr(self.model, order_by[0])
                    query = query.order_by(asc(attr))

            if skip and limit:
                return query.offset(skip).limit(limit)
            return query

        except Exception as e:
            raise e

    def get_multi(
            self,
            db: Session,
            filter_obj: GetMultiSchemaType = None,
            order_by: (str, Literal['asc', 'desc']) = None,
            skip: int = 0,
            limit: int = 100
    ) -> List[ModelType]:
        self._query = self._prepare_get_multi_query(
            db=db,
            filter_obj=filter_obj,
            order_by=order_by,
            skip=skip,
            limit=limit
        )
        return self._execute_query(action_name='all')

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        try:
            obj = self.model(**obj_in.dict())
            db.add(obj)
            db.flush()
            obj = db.query(self.model).filter(self.model.id == obj.id).first()
            return obj
        except Exception as e:
            raise e

    def update(
            self,
            db: Session,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_obj, key, value)

        db.add(db_obj)
        db.flush()
        return db_obj

    def _prepare_update_query(
            self,
            db: Session,
            filter_obj: GetMultiSchemaType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> Session.query:
        return self._prepare_get_multi_query(
            db=db,
            filter_obj=filter_obj
        )

    def update_v2(
            self,
            db: Session,
            filter_obj: GetMultiSchemaType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ):
        self._query = self._prepare_update_query(db=db, filter_obj=filter_obj, obj_in=obj_in)
        return self._execute_query(
            'update',
            {**obj_in.dict(exclude_unset=True)},
        )

    def _prepare_remove_query(self, db: Session, filter_obj: GetMultiSchemaType) -> bool:
        return self._prepare_get_multi_query(db=db, filter_obj=filter_obj)

    def remove(
            self,
            db: Session,
            filter_obj: GetMultiSchemaType,
    ):
        self._query = self._prepare_remove_query(db=db, filter_obj=filter_obj)
        self._execute_query(action_name='delete')

    def _create_db_obj(self, obj_in):
        obj_in_data = jsonable_encoder(obj_in)
        return self.model(**obj_in_data)

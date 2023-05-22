from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query
from pydantic import BaseModel
from typing import List, Any

from system.base.crud import CRUDBase
from .schemas.pay import GetMultiOrdPay, CreatePayOrderSchema, UpdatePayOrder
from .pay import OrdPay


class OrderCRUD(CRUDBase[OrdPay, CreatePayOrderSchema, UpdatePayOrder, GetMultiOrdPay]):
    
    def get_orders_query_set(self,
        db: Session,
        user_id: int = None,
        order_id: int = None,
        type: str = None,
        commission_id: int = None,
        status: str = None,
        merchant_id: int = None,
        created_at_gte: datetime = None,
        created_at_lte: datetime = None
    ):

        query = db.query(self.model).filter(
            self.model.deleted_at == None
        )

        if user_id:
            query = query.filter(self.model.user_id == user_id)
        if order_id:
            query = query.filter(self.model.id == order_id)
        if merchant_id:
            query = query.filter(self.model.merchant_id == merchant_id)
        if type:
            query = query.filter(self.model.type == type)
        if commission_id:
            query = query.filter(self.model.commission_id == commission_id)
        if status:
            query = query.filter(self.model.status == status)
        if created_at_gte:
            query = query.filter(self.model.created_at >= created_at_gte)
        if created_at_lte:
            query = query.filter(self.model.created_at <= created_at_lte)
            
        return query


    def get_orders(self,
        db: Session,
        user_id: int = None,
        order_id:int = None,
        type: str = None,
        commission_id: int = None,
        status: str = None,
        merchant_id: int = None,
        created_at_gte: datetime = None,
        created_at_lte: datetime = None,
        limit: int = None,
        skip: int = None
    ):

        query = self.get_orders_query_set(
            db,
            user_id,
            order_id,
            type,
            commission_id,
            status,
            merchant_id,
            created_at_gte,
            created_at_lte
        )
            
        total_count = query.count()

        if limit:
            query = query.limit(limit)
        if skip:
            query = query.offset(skip)
            
        result = []
        for order_row in query.all():
            
            result.append({
                "id": order_row.id,
                "title": order_row.title,
                "created_at": order_row.created_at,
                "amount": order_row.amount,
                "type": order_row.type,
                "commission": order_row.commission.category,
                "status": order_row.status
            })
            
        return {"query_result": result, "total_count": total_count}


order_crud = OrderCRUD(OrdPay)

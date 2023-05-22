from datetime import datetime, timedelta

from sqlalchemy.orm.session import Session
from sqlalchemy.sql import func

from system.base.mixins import InterfaceLifeCycle

from ..models.settle_credit import FncSettleCredit
from ..models.settle_pgw import FncSettlePgw


class MerchantDashboardInterface(InterfaceLifeCycle):
    @staticmethod
    def summary(user_id: int, db: Session) -> dict:
        """Get daily and monthly settlements summary.

        Args:
            user_id (int): Merchant ID
            db (Session): DataBase Session

        Returns:
            MerchantDashboardSummaryResponse
        """

        from user import UserService
        user_sr = UserService()
        user = user_sr.user.find_by_id(user_id=user_id, db=db)

        today = datetime.now()
        yesterday = today - timedelta(days=1)
        a_month_ago = today - timedelta(days=30)

        credit_queryset = db.query(
            FncSettleCredit.created_at,
            FncSettleCredit.merchant_id,
            func.sum(FncSettleCredit.amount).label("amount"),
        ).filter(
            FncSettleCredit.merchant_id == user.merchant.id
        ).filter(
            FncSettleCredit.created_at <= today
        ).group_by(
            FncSettleCredit.created_at,
            FncSettleCredit.merchant_id
        )

        credit_queryset_daily = credit_queryset.filter(
            FncSettleCredit.created_at >= yesterday
        )

        credit_queryset_daily_settled = credit_queryset_daily.filter(
            FncSettleCredit.transfer_id != None
        )

        credit_daily_settled = credit_queryset_daily_settled.first().amount if credit_queryset_daily_settled.first() else 0

        credit_queryset_daily_unsettled = credit_queryset_daily.filter(
            FncSettleCredit.transfer_id == None
        )

        credit_daily_unsettled = credit_queryset_daily_unsettled.first().amount if credit_queryset_daily_unsettled.first() else 0

        credit_queryset_monthly = credit_queryset.filter(
            FncSettleCredit.created_at >= a_month_ago
        )

        credit_queryset_monthly_settled = credit_queryset_monthly.filter(
            FncSettleCredit.transfer_id != None
        )

        credit_monthly_settled = credit_queryset_monthly_settled.first().amount if credit_queryset_monthly_settled.first() else 0

        # credit_queryset_monthly_unsettled = credit_queryset_monthly.filter(
        #     FncSettleCredit.transfer_id == None
        # )

        # credit_monthly_unsettled = credit_queryset_monthly_unsettled.first().amount if credit_queryset_monthly_unsettled.first() else 0

        pgw_queryset = db.query(
            FncSettlePgw.created_at,
            FncSettlePgw.merchant_id,
            func.sum(FncSettlePgw.amount).label("amount"),
        ).filter(
            FncSettlePgw.merchant_id == user.merchant.id
        ).filter(
            FncSettlePgw.created_at <= today
        ).group_by(
            FncSettlePgw.created_at,
            FncSettlePgw.merchant_id
        )

        pgw_queryset_daily = pgw_queryset.filter(
            FncSettlePgw.created_at >= yesterday
        )

        pgw_queryset_daily_settled = pgw_queryset_daily.filter(
            FncSettlePgw.transfer_id != None
        )

        pgw_daily_settled = pgw_queryset_daily_settled.first().amount if pgw_queryset_daily_settled.first() else 0

        pgw_queryset_daily_unsettled = pgw_queryset_daily.filter(
            FncSettlePgw.transfer_id == None
        )

        pgw_daily_unsettled = pgw_queryset_daily_unsettled.first().amount if pgw_queryset_daily_unsettled.first() else 0

        pgw_queryset_monthly = pgw_queryset.filter(
            FncSettlePgw.created_at >= a_month_ago
        )

        pgw_queryset_monthly_settled = pgw_queryset_monthly.filter(
            FncSettlePgw.transfer_id != None
        )

        pgw_monthly_settled = pgw_queryset_monthly_settled.first().amount if pgw_queryset_monthly_settled.first() else 0

        # pgw_queryset_monthly_unsettled = pgw_queryset_monthly.filter(
        #     FncSettlePgw.transfer_id == None
        # )

        # pgw_monthly_unsettled = pgw_queryset_monthly_unsettled.first().amount if pgw_queryset_monthly_unsettled.first() else 0

        result = {
            "credit": {
                "daily": credit_daily_settled,
                "monthly": credit_monthly_settled
            },
            "pgw": {
                "daily": pgw_daily_settled,
                "monthly": pgw_monthly_settled
            },
            "unsettled": {
                "credit": credit_daily_unsettled,
                "pgw": pgw_daily_unsettled
            }
        }

        return result

    @staticmethod
    def plot(user_id: int, start_time: datetime, end_time: datetime, db: Session) -> dict:
        """Get daily settlements plot.

        Args:
            user_id (int): Merchant ID
            start_time (datetime): Plot Start Time (inclusive). datetime object gets truncated to date object.
            end_time (datetime): Plot Start Time (inclusive). datetime object gets truncated to date object.
            db (Session): DataBase Session

        Returns:
            MerchantDashboardPlotResponse
        """
        from pydantic import BaseModel
        from user import UserService
        user_sr = UserService()
        user = user_sr.user.find_by_id(user_id=user_id, db=db)

        class PaymentPlotRow(BaseModel):
            time: datetime
            credit: int
            pgw: int

        credit_plot_queryset = db.query(
            func.date_trunc('day', FncSettleCredit.created_at).label('created_at'),
            FncSettleCredit.merchant_id,
            func.sum(FncSettleCredit.amount).label("amount"),
        ).filter(
            FncSettleCredit.merchant_id == user.merchant.id
        ).filter(
            func.date_trunc('day', FncSettleCredit.created_at) >= func.date_trunc('day', start_time)
        ).filter(
            func.date_trunc('day', FncSettleCredit.created_at) <= func.date_trunc('day', end_time)
        ).group_by(
            func.date_trunc('day', FncSettleCredit.created_at),
            FncSettleCredit.merchant_id
        ).order_by(
            func.date_trunc('day', FncSettleCredit.created_at)
        )

        pgw_plot_queryset = db.query(
            func.date_trunc('day', FncSettlePgw.created_at).label('created_at'),
            FncSettlePgw.merchant_id,
            func.sum(FncSettlePgw.amount).label("amount"),
        ).filter(
            FncSettlePgw.merchant_id == user.merchant.id
        ).filter(
            func.date_trunc('day', FncSettlePgw.created_at) >= func.date_trunc('day', start_time)
        ).filter(
            func.date_trunc('day', FncSettlePgw.created_at) <= func.date_trunc('day', end_time)
        ).group_by(
            func.date_trunc('day', FncSettlePgw.created_at),
            FncSettlePgw.merchant_id
        ).order_by(
            func.date_trunc('day', FncSettlePgw.created_at)
        )

        credit_plot = credit_plot_queryset.all()
        pgw_plot = pgw_plot_queryset.all()
        start_day = start_time.date()
        end_day = end_time.date()
        credit_index = 0
        pgw_index = 0

        plot = []
        
        if end_day - timedelta(days=366) > start_day:
            end_day = start_day - timedelta(days=366)

        while start_day <= end_day:
            plot_row = PaymentPlotRow(time=datetime.combine(start_day, datetime.min.time()), credit=0, pgw=0)

            try:
                if (
                    credit_plot and
                    start_day == credit_plot[credit_index].created_at.date()
                ):
                    plot_row.credit = credit_plot[credit_index].amount
                    credit_index += 1
            except IndexError:
                pass
            
            try:
                if (
                    pgw_plot and
                    start_day == pgw_plot[pgw_index].created_at.date()
                ):
                    plot_row.pgw = pgw_plot[pgw_index].amount
                    pgw_index += 1
            except IndexError:
                pass
            
            start_day += timedelta(days=1)
            plot.append(plot_row.dict())

        return {
            "plot": plot
        }


merchant_dashboard_agent = MerchantDashboardInterface()

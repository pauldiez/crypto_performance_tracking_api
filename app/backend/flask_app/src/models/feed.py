from src.app import db
from .base import BaseModel
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy import func as SA_FUNC, cast as SA_CAST, types as SA_TYPES, Index
import datetime


class CryptoSymbols():
    ALQO = "ALQO"


class FeedModel(db.Model, BaseModel):
    __tablename__ = 'feed'

    # define crypto symbols
    CRYPTO_SYMBOLS = (CryptoSymbols.ALQO,)

    # define ENUM
    CRYPTO_SYMBOLS_ENUM = ENUM(*CRYPTO_SYMBOLS, name="symbol")

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(CRYPTO_SYMBOLS_ENUM, index=True, nullable=False)
    data = db.Column(db.JSON())
    totals = db.Column(db.JSON())
    date_added = db.Column(db.DateTime(), default=datetime.datetime.utcnow, index=True)

    Index("symbol_date_added_index", symbol, date_added)

    @staticmethod
    def get_custom_date_data(crypto_symbol, start_date, end_date, ):

        # set date format
        date_format = "%Y-%m-%d"

        # parse dates
        start_date = datetime.datetime.strptime(start_date, date_format)
        end_date = datetime.datetime.strptime(end_date, date_format)

        # get start_date and end_date difference in days
        delta = end_date - start_date

        # if 30 days or under the process by day
        if int(delta.days) <= 30:
            # create subquery
            subquery = db.session.query(
                SA_FUNC.max(FeedModel.date_added)).filter(
                FeedModel.symbol == crypto_symbol,
                FeedModel.date_added >= start_date,
                FeedModel.date_added <= end_date).group_by(
                SA_FUNC.date_part('day', FeedModel.date_added)).subquery()

        # if a year or under process then by month
        elif int(delta.days) < 365:
            # create subquery
            subquery = db.session.query(
                SA_FUNC.max(FeedModel.date_added)).filter(
                FeedModel.symbol == crypto_symbol,
                FeedModel.date_added >= start_date,
                FeedModel.date_added <= end_date).group_by(
                SA_FUNC.date_part('month', FeedModel.date_added)).subquery()

        # if a year or over then process by year
        elif int(delta.days) >= 365:
            # create subquery
            subquery = db.session.query(
                SA_FUNC.max(FeedModel.date_added)).filter(
                FeedModel.symbol == crypto_symbol,
                FeedModel.date_added >= start_date,
                FeedModel.date_added <= end_date).group_by(
                SA_FUNC.date_part('year', FeedModel.date_added)).subquery()

        # process query
        feed_models = db.session.query(
            FeedModel).filter(FeedModel.date_added.in_(subquery)).order_by(
            FeedModel.date_added)

        # return models
        return feed_models

    @staticmethod
    def get_all_data(crypto_symbol):

        # search for earliest date
        feed_model = db.session.query(
            SA_CAST(SA_FUNC.min(FeedModel.date_added), SA_TYPES.Date).label("date_added")).filter(
            FeedModel.symbol == crypto_symbol).first()

        # set start date with earliest
        date_start = feed_model.date_added

        # build subquery
        subquery = db.session.query(
            SA_FUNC.max(FeedModel.date_added)).filter(
            FeedModel.symbol == crypto_symbol,
            FeedModel.date_added >= date_start
        ).group_by(
            SA_CAST(FeedModel.date_added, SA_TYPES.Date)).subquery()

        # process query
        feed_models = db.session.query(
            FeedModel).filter(FeedModel.date_added.in_(subquery)).order_by(
            FeedModel.date_added).limit(100)

        # return models
        return feed_models

    @staticmethod
    def get_last_year_data(crypto_symbol):

        # set today's date
        today = datetime.date.today()

        # set date 1 year ago from today
        date_1_year_ago = today - datetime.timedelta(year=1)

        # build subquery
        subquery = db.session.query(
            SA_FUNC.max(FeedModel.date_added)).filter(
            FeedModel.symbol == crypto_symbol,
            FeedModel.date_added >= date_1_year_ago).group_by(
            SA_CAST(FeedModel.date_added, SA_TYPES.Date)).subquery()

        # process query
        feed_models = db.session.query(
            FeedModel).filter(FeedModel.date_added.in_(subquery)).order_by(
            FeedModel.date_added)

        # return models
        return feed_models

    @staticmethod
    def get_last_30_days_data(crypto_symbol):

        # set today's date
        today = datetime.date.today()

        # set date 30 days from today
        date_30_days_ago = today - datetime.timedelta(days=30)

        # build subquery
        subquery = db.session.query(
            SA_FUNC.max(FeedModel.date_added)).filter(
            FeedModel.symbol == crypto_symbol,
            FeedModel.date_added >= date_30_days_ago).group_by(
            SA_CAST(FeedModel.date_added, SA_TYPES.Date)).subquery()

        # process query
        feed_models = db.session.query(
            FeedModel).filter(FeedModel.date_added.in_(subquery)).order_by(
            FeedModel.date_added)

        # return models
        return feed_models

    @staticmethod
    def get_last_7_days_data(crypto_symbol):

        # set today's date
        today = datetime.date.today()
        date_7_days_ago = today - datetime.timedelta(days=7)

        # build subquery
        subquery = db.session.query(
            SA_FUNC.max(FeedModel.date_added)).filter(
            FeedModel.symbol == crypto_symbol,
            FeedModel.date_added >= date_7_days_ago).group_by(
            SA_CAST(FeedModel.date_added, SA_TYPES.Date)).subquery()

        # process query
        feed_models = db.session.query(
            FeedModel).filter(FeedModel.date_added.in_(subquery)).order_by(
            FeedModel.date_added)

        # return models
        return feed_models

    @staticmethod
    def get_last_24_hours(crypto_symbol):

        # get today's date
        today = datetime.date.today()

        # get date 12 hours ago
        date_24_hours_ago = today - datetime.timedelta(hours=24)

        # process query
        result = FeedModel.query.filter(FeedModel.symbol == crypto_symbol,
                                        FeedModel.date_added >= date_24_hours_ago
                                        ).first()
        feed_models = [result]

        # return models
        return feed_models

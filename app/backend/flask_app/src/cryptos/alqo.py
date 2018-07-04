from src.cryptos.base import BaseCrypto
from src.app import db
from src.models.feed import CryptoSymbols
from src.schemas import FeedSchema
import requests
import logging
import datetime


class ALQO(BaseCrypto):
    SYMBOL_NAME = "ALQO"
    URL = "https://explorer.alqo.org/api/richlist/"

    @staticmethod
    def fetch_live_data():

        response = requests.get(ALQO.URL)
        if response.status_code != 200:
            message = "Error fetching live %s feed - Status code %d - Message %s" % (
                ALQO.SYMBOL_NAME, response.status_code, response.reason)
            logging.error(message)
            return {'errors': message}

        # return data
        return response.json()

    @staticmethod
    def process_data_with_totals(data):

        if 'errors' in data:
            return data['errors']

        if 'richlistBalance' not in data:
            message = "Error finding results in %s response - Status code %s" % (
                ALQO.SYMBOL_NAME)
            logging.error(message)
            return {'errors': message}

        totals = ALQO.calculate_totals(data['richlistBalance'])

        # build feed db row
        data = {"symbol": CryptoSymbols.ALQO,
                "data": data['richlistBalance'],
                "totals": totals}

        # load request data into feed schema
        feed_schema = FeedSchema().load(data, db.session)

        # check for errors - if errors notify admin
        if feed_schema.errors:
            message = ",".join(feed_schema.errors)
            logging.error(message)
            return {'errors': message}

        # get feed model
        new_feed_model = feed_schema.data

        # deserialize feed model
        feed_data = FeedSchema().dump(new_feed_model).data

        # modify non db properties (we don't have to do this, but otherwise, these the properties below would be null)
        feed_data.pop('id')
        feed_data['date_added'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # return data
        return feed_data

    @staticmethod
    def save_data_to_db(data):

        if 'errors' in data:
            return data['errors']

        # load request data into feed schema
        feed_schema = FeedSchema().load(data, db.session)

        # check for errors - if errors notify admin
        if feed_schema.errors:
            message = ",".join(feed_schema.errors)
            logging.error(message)
            return {'errors': message}

        # get feed model
        new_feed_model = feed_schema.data

        # save model
        new_feed_model.save()

        # return data
        return True

    @staticmethod
    def calculate_totals(results):
        # calculate totals
        totals = {"balance": 0}
        for row in results:
            totals['balance'] += float(row['balance'])

        return totals

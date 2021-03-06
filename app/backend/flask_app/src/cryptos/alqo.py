from src.cryptos.base import AbstractBaseCrypto
from src.app import db
from src.models.feed import CryptoSymbols
from src.schemas import FeedSchema
import requests
import logging
import datetime


class ALQO(AbstractBaseCrypto):
    """ALQO Crypto class. This class is used to fetch, process and store
    currency data.
    """

    SYMBOL_NAME = "ALQO"
    FETCH_URL = "https://explorer.alqo.org/api/richlist/"

    @staticmethod
    def fetch_live_data():
        """Fetch live crypto currency data"""

        response = requests.get(ALQO.FETCH_URL)
        if response.status_code != 200:
            message = "Error fetching live %s feed - Status code " \
                      "%d - Message %s" % (ALQO.SYMBOL_NAME,
                                           response.status_code, response.reason)
            logging.error(message)
            return {'errors': message}

        return response.json()

    @staticmethod
    def process_data_with_totals(data):

        if 'errors' in data:
            return data['errors']

        # Check if we have correct data we are looking for
        if 'richlistBalance' not in data:
            message = "Error finding results in %s response - Status code %s" % (
                ALQO.SYMBOL_NAME)
            logging.error(message)
            return {'errors': message}

        totals = ALQO.calculate_totals(data['richlistBalance'])

        # Build feed db row
        data = {"symbol": CryptoSymbols.ALQO,
                "data": data['richlistBalance'],
                "totals": totals}

        # Load request data into feed schema
        feed_schema = FeedSchema().load(data, db.session)

        # Check for errors
        if feed_schema.errors:
            message = ",".join(feed_schema.errors)
            logging.error(message)
            return {'errors': message}

        # Get feed model
        new_feed_model = feed_schema.data

        # Deserialize feed model
        feed_data = FeedSchema().dump(new_feed_model).data

        # Modify non db properties (we don't have to do this,
        # but otherwise, these the properties below would be null).
        feed_data.pop('id')
        feed_data['date_added'] = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")

        # Return data
        return feed_data

    @staticmethod
    def save_data_to_db(data):
        """Save data to database"""

        if 'errors' in data:
            return data['errors']

        # Load request data into feed schema
        feed_schema = FeedSchema().load(data, db.session)

        # Check for errors
        if feed_schema.errors:
            message = ",".join(feed_schema.errors)
            logging.error(message)
            return {'errors': message}

        # Get feed model
        new_feed_model = feed_schema.data

        # Save model
        new_feed_model.save()

        # Return data
        return True

    @staticmethod
    def calculate_totals(results):
        """Calculate totals for result set"""

        totals = {'balance': 0}
        for row in results:
            totals['balance'] += float(row['balance'])

        return totals

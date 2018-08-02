from src.app import auth
from flask_restful import Resource
from src.tasks import fetch_and_process_crypto_data
from src.models import FeedModel
from src.schemas import FeedSchema
from src.resources import ResponseDataBuilder
from src.cryptos import CryptoFactoryMethod
from flask import request
import datetime
from dateutil.parser import parse


class FeedCollectionResource(Resource):
    @auth.login_required
    def get(self, crypto_symbol):
        """GET request for feed collection resource

        :param crypto_symbol:
        :return object: request object
        """

        # Convert crypto to uppercase
        crypto_symbol = crypto_symbol.upper()

        if crypto_symbol not in FeedModel.CRYPTO_SYMBOLS:
            return {'errors': "Invalid crypto symbol. "
                              "Valid crypto symbols are the following: [%s]"
                              % ",".join(FeedModel.CRYPTO_SYMBOLS)}, \
                   400, {"content-type": "application/json"}

        # Get request params
        live = request.args.get('live')
        date_string = request.args.get('date_string')

        # Throw an error to educate users of misuse of params
        if live and date_string:
            return {
                       'errors': "Parameter 'live' cannot be set to true (live=1) "
                                 "when using 'date_string'"}, \
                   400, {"content-type": "application/json"}

        # Determine whether to process live feed or by past dates
        if live or date_string is None:
            # Process live feed request
            return _process_live_feed_request(crypto_symbol)

        elif date_string:
            # Process date_string feed requests
            return _process_date_string_request(crypto_symbol, date_string)

    def post(self, crypto_symbol):
        """POST request for feed collection resource

        :param crypto_symbol:
        :return object: request object
        """

        # Fetch and process crypto currency data and queue to Celery
        # background process.
        results = fetch_and_process_crypto_data.apply_async(
            args=[crypto_symbol], queue="high_priority")

        # Check for errors
        if "errors" in results:
            return {'errors': results["errors"]}, 400, {
                "content-type": "application/json"}

        # Return json data request
        return results, 201, {"content-type": "application/json"}


def _process_live_feed_request(crypto_symbol):
    """Process live feed request

    :param crypto_symbol:
    :return object: request object
    """
    # Instantiate crypto class
    crypto_object = CryptoFactoryMethod.generate_object(crypto_symbol)

    # Fetch live data
    results = crypto_object.fetch_live_data()
    results = crypto_object.process_data_with_totals(results)

    # Check for errors
    if "errors" in results:
        return {'errors': "%s" % results['errors']}, 400, {
            "content-type": "application/json"}

    # Build and structure response data - eg: metadata, data etc..
    response_data = ResponseDataBuilder(results,
                                        process_totals=True).get_response()

    # return json data request
    return response_data, 200, {"content-type": "application/json"}


def _process_date_string_request(crypto_symbol, date_string):
    """Process date string request

    :param crypto_symbol:
    :param date_string:
    :return list: feed models:
    """
    # Set allowed date string params
    allowed_date_strings = ['last_24_hours', 'last_7_days', 'last_30_days',
                            'last_year', 'all', 'custom']

    # Validate allowed date_string params
    if date_string not in allowed_date_strings:
        return {
                   "errors": "Invalid date_string parameter. "
                             "The date_string parameter must be one "
                             "of the following options [%s] " % ",".join(
                       allowed_date_strings)
               },
        400,
        {"content-type": "application/json"}

    else:
        date_format = ''
        if date_string == 'last_24_hours':
            date_format = '%Y-%m-%d'
            feed_models = FeedModel.get_last_24_hours(crypto_symbol)
            feed_collection_data = FeedSchema(many=True).dump(feed_models).data

        elif date_string == 'last_7_days':
            date_format = '%Y-%m-%d'
            feed_models = FeedModel.get_last_7_days_data(crypto_symbol)
            feed_collection_data = FeedSchema(many=True).dump(feed_models).data

        elif date_string == 'last_30_days':
            date_format = '%Y-%m-%d'
            feed_models = FeedModel.get_last_30_days_data(crypto_symbol)
            feed_collection_data = FeedSchema(many=True).dump(feed_models).data

        elif date_string == 'last_year':
            date_format = '%Y-%m'
            feed_models = FeedModel.get_last_year_data(crypto_symbol)
            feed_collection_data = FeedSchema(many=True).dump(feed_models).data

        elif date_string == 'all':
            date_format = '%Y-%m-%d'
            feed_models = FeedModel.get_all_data(crypto_symbol)
            feed_collection_data = FeedSchema(many=True).dump(feed_models).data

        elif date_string == 'custom':

            # Get request params
            start_date = request.args.get('start_date', False)
            end_date = request.args.get('start_end', False)

            feed_collection_data = _process_custom_dates(crypto_symbol,
                                                         start_date, end_date)

            # Set date format
            date_format = "%Y-%m-%d"

            # Parse dates
            start_date = datetime.datetime.strptime(start_date, date_format)
            end_date = datetime.datetime.strptime(end_date, date_format)

            # Get start_date and end_date difference in days and set date
            # format based on num of day difference.
            delta = end_date - start_date
            if int(delta.days) <= 30:
                date_format = "%Y-%m-%d"
            elif int(delta.days) < 365:
                date_format = "%Y-%m"
            elif int(delta.days) >= 365:
                date_format = "%Y"
            else:
                date_format = "%Y"

        response = ResponseDataBuilder()
        totals = response.process_totals(feed_collection_data)
        response.set_totals(totals)

        # Structure data by day
        data = []
        for row in feed_collection_data:
            date_index = parse(row['date_added']).strftime(date_format)
            data.append({date_index: row})

        # Build and structure response data - eg: metadata, data etc..
        response.set_data(data)
        response_data = response.get_response()

        # Return json data request
        return response_data, 200, {"content-type": "application/json"}


def _process_custom_dates(crypto_symbol, start_date, end_date):
    """ Process custom dates

    :param crypto_symbol:
    :param start_date:
    :param end_date:
    :return list: feed models:
    """
    # Validate required params
    errors = None
    if start_date == False or end_date == False:
        errors = {"errors": "If date_string parameter is set to 'custom', "
                            "parameter 'start_date' and end_date' need to be set."
                            " (format: yyyy-mm-day )'"}

    # Validate start date
    try:
        datetime.datetime.strptime(start_date, '%Y-%m-%d')
    except ValueError:
        errors = {
            "errors": "Incorrect start date format, should be YYYY-MM-DD"}

    # Validate end date
    try:
        datetime.datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        errors = {
            "errors": "Incorrect start date format, should be YYYY-MM-DD"}

    # Check for errors
    if errors:
        return errors

    # Get custom date data
    feed_models = FeedModel.get_custom_date_data(crypto_symbol, start_date,
                                                 end_date)

    # Deserialize feed models
    feed_collection_data = FeedSchema(many=True).dump(feed_models).data

    return feed_collection_data

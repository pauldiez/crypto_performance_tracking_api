from src.app import auth
from flask_restful import Resource
from src.tasks import fetch_and_process_crypto_data
from src.models import FeedModel
from src.schemas import FeedSchema
from src.resources import ResponseDataBuilder
from src.cryptos import CryptoFactory
from flask import request
import datetime
from dateutil.parser import parse


class FeedCollectionResource(Resource):
    # uncomment below to turn authorization
    # @auth.login_required
    def get(self, crypto_symbol):

        # convert to uppercase
        crypto_symbol = crypto_symbol.upper()

        if crypto_symbol not in FeedModel.CRYPTO_SYMBOLS:
            return {'errors': "Invalid crypto symbol. "
                              "Valid crypto symbols are the following: [%s]" % ",".join(FeedModel.CRYPTO_SYMBOLS)}, \
                   400, {"content-type": "application/json"}

        # get request params
        live = request.args.get('live')
        date_string = request.args.get('date_string')

        # throw an error to educate users of misuse of params
        if live and date_string:
            return {'errors': "Parameter 'live' cannot be set to true (live=1) when using 'date_string'"}, 400, {
                "content-type": "application/json"}

        # determine whether to process live feed or by past dates
        if live or date_string is None:
            # process live feed request
            return process_live_feed_request(crypto_symbol)

        elif date_string:
            # process date_string feed requests
            return process_date_string_request(crypto_symbol, date_string)

    def post(self, crypto_symbol):

        # fetch and process crypto currency data, queue to Celery background process
        results = fetch_and_process_crypto_data.apply_async(args=[crypto_symbol], queue="high_priority")

        return True
        # check for errors
        if "errors" in results:
            return {'errors': results["errors"]}, 400, {"content-type": "application/json"}

        # return json data request
        return results, 201, {"content-type": "application/json"}


def process_live_feed_request(crypto_symbol):
    # instantiate crypto class
    crypto_object = CryptoFactory.generate_object(crypto_symbol)

    # fetch live data
    results = crypto_object.fetch_live_data()
    results = crypto_object.process_data_with_totals(results)

    # check for errors
    if "errors" in results:
        return {'errors': "%s" % results['errors']}, 400, {"content-type": "application/json"}

    # build and structure response data - eg: metadata, data etc..
    response_data = ResponseDataBuilder(results, process_totals=True).get_response()

    # return json data request
    return response_data, 200, {"content-type": "application/json"}


def process_date_string_request(crypto_symbol, date_string):
    # set allowed date string params
    allowed_date_strings = ['last_24_hours', 'last_7_days', 'last_30_days', 'last_year', 'all', 'custom']

    # validate allowed date_string params
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

            # get request params
            start_date = request.args.get('start_date', False)
            end_date = request.args.get('start_end', False)

            feed_collection_data = process_custom_dates(crypto_symbol, start_date, end_date)

            # set date format
            date_format = "%Y-%m-%d"

            # parse dates
            start_date = datetime.datetime.strptime(start_date, date_format)
            end_date = datetime.datetime.strptime(end_date, date_format)

            # get start_date and end_date difference in days and set date format based on num of day difference
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

        # structure data by day
        data = []
        for row in feed_collection_data:
            date_index = parse(row['date_added']).strftime(date_format)
            data.append({date_index: row})

        # build and structure response data - eg: metadata, data etc..
        response.set_data(data)
        response_data = response.get_response()

        # return json data request
        return response_data, 200, {"content-type": "application/json"}


def process_custom_dates(crypto_symbol, start_date, end_date):
    # validate required params
    errors = None
    if start_date == False or end_date == False:
        errors = {"errors": "If date_string parameter is set to 'custom', "
                            "parameter 'start_date' and end_date' need to be set."
                            " (format: yyyy-mm-day )'"}

    # validate start date
    try:
        datetime.datetime.strptime(start_date, '%Y-%m-%d')
    except ValueError:
        errors = {"errors": "Incorrect start date format, should be YYYY-MM-DD"}

    # validate end date
    try:
        datetime.datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        errors = {"errors": "Incorrect start date format, should be YYYY-MM-DD"}

    # check for errors
    if errors:
        return errors, 400, {"content-type": "application/json"}

    # get custom date data
    feed_models = FeedModel.get_custom_date_data(crypto_symbol, start_date, end_date)

    # deserialize feed models
    feed_collection_data = FeedSchema(many=True).dump(feed_models).data

    return feed_collection_data

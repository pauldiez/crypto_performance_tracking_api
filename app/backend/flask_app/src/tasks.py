from celery.utils.log import get_task_logger
from flask_mail import Message
from src.app import celery, db, Config
from src.library.email import MailErrorException
from src.library.email import send_email
from src.models import FeedModel
from src.cryptos import CryptoFactoryMethod

logger = get_task_logger(__name__)


@celery.task(bind=True,
             queue='high_priority',
             default_retry_delay=300,
             max_retries=3)
def fetch_and_process_crypto_data(self, crypto_symbol):
    """Fetch and process crypto data.

    :param self:
    :param crypto_symbol:
    :return:
    """

    # Get crypto object
    crypto_object = CryptoFactoryMethod.generate_object(crypto_symbol)

    # Fetch live crypto data
    results = crypto_object.fetch_live_data()

    # If errors send an email out
    if "errors" in results:
        subject = "Error fetching live %s feed" % crypto_symbol
        message = "%s" % (results['errors'])
        recipients = [Config.EMAILS['ADMIN'][0][1]]

        # setup email message
        email = Message(subject=subject,
                        sender=Config.EMAILS['ADMIN'][0][1],
                        recipients=recipients)
        email.body = message
        send_email(email)

        return False

    results = crypto_object.process_data_with_totals(results)

    # if errors send an email out
    if "errors" in results:
        subject = "Error fetching live AQLO feed"
        message = "%s" % (results['errors'])
        recipients = [Config.EMAILS['ADMIN'][0][1]]

        # setup email message
        email = Message(subject=subject,
                        sender=Config.EMAILS['ADMIN'][0][1],
                        recipients=recipients)
        email.body = message
        send_email(email)

        return False

    crypto_object.save_data_to_db(results)

    logger.debug(results)

    return results

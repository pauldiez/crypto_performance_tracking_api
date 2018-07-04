from celery.utils.log import get_task_logger
from flask_mail import Message
from src.app import celery, db, Config
from src.library.email import MailErrorException
from src.library.email import send_email
from src.emails import generate_hello_user_email
from src.models import FeedModel
from src.cryptos import CryptoFactory

logger = get_task_logger(__name__)


@celery.task(bind=True, queue='high_priority', default_retry_delay=300, max_retries=3)
def fetch_and_process_crypto_data(self, crypto_symbol):
    # instantiate crypto class
    crypto_object = CryptoFactory.generate_object(crypto_symbol)

    # fetch live crypto data
    results = crypto_object.fetch_live_data()

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

    results = crypto_object.process_data_with_totals(results)

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

    # save data to db
    crypto_object.save_data_to_db(results)

    logger.debug(results)

    # return results
    return results


@celery.task(bind=True, queue='high_priority', auto_retry=[MailErrorException], default_retry_delay=300, max_retries=3)
def send_welcome_email(self, user_data):
    """
    Send confirmation email

    :param self:
    :param feed_data: feed data
    :return: boolean
    """

    # generate confirmation email
    email = generate_hello_user_email(user_data)

    try:
        # send email
        send_email(email)
    except MailErrorException as error:
        try:
            logger.error(
                "Mail background worker Error: %s - will retry (attempts %d )" % (str(error), self.request.retries))
            self.retry(error)
        except self.MaxRetriesExceededError:
            logger.error(
                "Mail background worker task fails: %s - after %d attempts" % (str(error), self.request.retries))

    # return
    return True


@celery.task(queue='high_priority')
def log(message):
    """Print some log messages"""
    logger.debug(message)
    logger.info(message)
    logger.warning(message)
    logger.error(message)
    logger.critical(message)


@celery.task(queue='high_priority')
def print_feeds():
    """Print all feeds in DB"""
    for feed in FeedModel.query.all():
        logger.debug(feed.totals)

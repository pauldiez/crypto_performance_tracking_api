from src.app import Config, mail
from src.library.exceptions import MailErrorException
from smtplib import SMTPAuthenticationError, SMTPServerDisconnected, \
    SMTPException
import logging


def send_email(message):
    """
    Send email wrapper

    Example

    subject = "Please confirm your %s account" % Config.APP_NAME
    recipient_name = "Glen Garry Jr"
    recipients = [recipient_name, 'glengarry.jr@gmail.com']

    # setup message message
    message = Message(subject=subject,
                               sender='some-admin@somewebsite.com',
                               recipients=[recipients])
    message.body = render_template("message/welcome.txt", **template_vars)
    message.html = render_template("message/welcome.html", **template_vars)

    # send message
    mail.send(message)

    :param message: CustomEmailMessage object
    :return:
    """
    try:

        # Parse recipients emails to a string
        if isinstance(message.recipients, list):
            for recipient in message.recipients:
                if isinstance(recipient, list):
                    message_string = "%s, %s" % (recipient, message_string)
                elif isinstance(recipient, str):
                    message_string = recipient
        elif isinstance(message.recipients, str):
            message_string = message.recipients

        # If we are in a development environment we don't want to send real
        # messages out to the public. So we do some data massaging to
        # prevent that.

        # If dev mode, modify emails and subject
        if Config.FLASK_ENV == Config.ENVIRONMENTS.DEVELOPMENT.value:
            message.subject = "[DEV MODE] %s - %s" % (
                message.subject, message_string)
            logging.info("Sending message to %s - Subject: %s - " % (
                message_string, message.subject))

            message.recipients = [Config.EMAILS['DEV'][0]]
            logging.debug("Hijacking recipient email to admin email %s - " % (
                ', '.join(message.recipients)))
            logging.debug("Message body: %s" % message.body)

        # Send message
        mail.send(message)

        logging.info("Sent messages to %s - Subject: %s - " % (
            message_string, message.subject))

        return True

    except SMTPAuthenticationError as error:
        logging.error("SMTP Authentication Error: %s - code %d" % (
            error.smtp_error, error.smtp_code))
        raise MailErrorException('SMTP Authentication Error') from error

    except SMTPServerDisconnected as error:
        logging.error("SMTP Server Disconnected: %s" % error.args)
        raise MailErrorException('SMTP Server Disconnected') from error

    except SMTPException as error:
        logging.error("SMTP Exception: %s" % error.args)
        raise MailErrorException('SMTP Error') from error

    return False

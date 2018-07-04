from flask import render_template
from flask_mail import Message
from src.config import Config


def generate_hello_user_email(user_data):
    """
    Generate hello world email

    :param user_data: user data
    :return: object: flask email message object
    """
    subject = "Hello %s, welcome to %s" % (user_data['name'], Config.APP_NAME)

    recipient = [user_data['name'], user_data['email']] #[name, email]

    # set email template vars
    template_vars = {"user_data": user_data, "app_name": Config.APP_NAME }

    # setup email message
    email = Message(subject=subject,
                    sender=Config.EMAILS['MARKETING'][0],
                    recipients=[recipient])

    email.body = render_template("email/welcome.txt", **template_vars)
    email.html = render_template("email/welcome.html", **template_vars)

    # return email
    return email
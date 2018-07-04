from src.app import db, create_app
from celery.utils.log import get_task_logger
from celery.signals import task_prerun, task_postrun
from src.config import Config, CeleryConfig


"""
For guideline and example explanations refer to link below 
https://pawelzny.com/python/celery/2017/08/14/celery-4-tasks-best-practices/
"""

logger = get_task_logger(__name__)
app = create_app(Config)
celery = app.celery

# NOTE the key to this task working properly is to import the "celery" object

@task_prerun.connect
def celery_prerun(*args, **kwargs):
    """

    :param args:
    :param kwargs:
    :return:
    """
    with app.app_context():
       pass


@task_postrun.connect
def close_session(*args, **kwargs):
    """

    :param args:
    :param kwargs:
    :return:
    """

    #Flask SQLAlchemy will automatically create new sessions for you from
    # a scoped session factory, given that we are maintaining the same app
    # context, this ensures tasks have a fresh session (e.g. session errors
    # won't propagate across tasks)
    db.session.remove()
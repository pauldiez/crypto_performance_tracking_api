import pendulum
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from src.config import Config
from src.app import celery
from src.tasks import log, fetch_and_process_crypto_data
from src.models.feed import CryptoSymbols

"""
For guideline and example explanations refer to link below 
https://pawelzny.com/python/celery/2017/08/14/celery-4-tasks-best-practices/

For Crontab schedule guidelines
http://docs.celeryproject.org/en/2.0-archived/getting-started/periodic-tasks.html
"""


# NOTES
# The key to this task working properly is to import the "celery" object
# Second, this script only 'schedules' tasks, and sends it to the celery queue.
# It doesn't execute the tasks. The task "worker" script has to be running to execute the scheduled tasks
# (Which are schedules from this script from this script)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls print_users every 10 seconds.
    #sender.add_periodic_task(5.0, some_function_to_call.s(some_param), name='execute some function every 5 seconds')

    # Calls log('Logging Stuff') every 30 seconds
    #sender.add_periodic_task(10.0, log.s('THIS IS A TEST'), name='Log every 10 seconds')

    # Executes everyday, every 12 hours
    sender.add_periodic_task(crontab(hour="*/12"), fetch_and_process_crypto_data.s(CryptoSymbols.ALQO), name="Process and store %s data-set every 12 hours" % CryptoSymbols.ALQO)




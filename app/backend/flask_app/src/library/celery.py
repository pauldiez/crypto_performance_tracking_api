from celery import Celery
from src.config import Config, CeleryConfig


class CeleryWrapper(Celery):
    """This is a class that wraps around the native Celery
    class which allows us to create convenience functions.
    """

    def init_app(self, app):
        """A convenience function to configure the celery object after it was
         been instantiated.

        :param app:
        :return:
        """
        self.conf.update(app.config)
        TaskBase = self.Task

        class ContextTask(TaskBase):
            abstract = True

            def __call__(self, *args, **kwargs):
                with app.app_context(), app.test_request_context(
                        base_url='%s://%s:%s' % (
                                Config.PREFERRED_URL_SCHEME,
                                Config.APP_HOST_IP,
                                Config.APP_HOST_PORT)):
                    return TaskBase.__call__(self, *args, **kwargs)

        self.Task = ContextTask
        self.app = app
        self.config_from_object(CeleryConfig)

        return True

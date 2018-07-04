from abc import ABC, abstractmethod


class BaseCrypto(object):

    @staticmethod
    @abstractmethod
    def fetch_live_data(results):
        raise Exception("%s, %s needs to implemented" % (__class__, __name__))

    @staticmethod
    @abstractmethod
    def calculate_total(results):
        raise Exception("%s, %s needs to implemented" % (__class__, __name__))

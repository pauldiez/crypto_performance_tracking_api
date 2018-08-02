from abc import abstractmethod


class AbstractBaseCrypto(object):
    """Abstract Base Crypto class"""

    @classmethod
    @abstractmethod
    def fetch_live_data(cls, results):
        """Fetch live crypto currency data"""
        raise Exception("%s, %s needs to implemented" % (__class__, __name__))

    @classmethod
    @abstractmethod
    def calculate_totals(cls, results):
        """Calculate totals"""
        raise Exception("%s, %s needs to implemented" % (__class__, __name__))

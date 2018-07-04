class BaseCrypto(object):

    @staticmethod
    def fetch_live_data(results):
        raise Exception("%s, %s needs to implemented" % (__class__, __name__))

    @staticmethod
    def calculate_total(results):
        raise Exception("%s, %s needs to implemented" % (__class__, __name__))
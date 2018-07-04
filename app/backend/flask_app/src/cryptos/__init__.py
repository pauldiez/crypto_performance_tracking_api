from .alqo import BaseCrypto
import importlib


class CryptoFactory(object):

    @staticmethod
    def generate_object(crypto_symbol, *args, **kwargs):
        try:
            # set module name to where we want to import our crypto classes
            module_name = crypto_symbol.lower()
            # set crypto class name
            crypto_class_name = crypto_symbol.upper()

            # set crypto module path
            crypto_module = importlib.import_module("." + module_name, package='src.cryptos')

            # get crypto class
            crypto_class = getattr(crypto_module, crypto_class_name)

            # instantiate crypto class
            crypto_class_instance = crypto_class(*args, **kwargs)

        except (AttributeError, ModuleNotFoundError):
            raise ImportError('{} is not part of our crypto platform!'.format(crypto_symbol))
        else:
            if not issubclass(crypto_class, BaseCrypto):
                raise ImportError(
                    "We currently don't have {}, but you are welcome to send in the request for it!".format(
                        crypto_class))

        # return crypto class
        return crypto_class_instance

from .alqo import AbstractBaseCrypto
import importlib


class CryptoFactoryMethod(object):
    """A factory method pattern class to used to instantiate our
    crypto objects"""

    @classmethod
    def generate_object(cls, crypto_symbol, *args, **kwargs):
        """Return crypto object based on crypto symbol passed in"""

        try:
            # Determine correct crypto module to import
            module_name = crypto_symbol.lower()
            crypto_module = importlib.import_module("." + module_name,
                                                    package='src.cryptos')
            crypto_class = getattr(crypto_module, crypto_symbol.upper())
            crypto_class_instance = crypto_class(*args, **kwargs)

        except (AttributeError, ModuleNotFoundError):
            raise ImportError(
                '%s is not part of our crypto platform yet.'
                % crypto_symbol.upper())
        else:
            if not issubclass(crypto_class, AbstractBaseCrypto):
                raise ImportError(
                    "We currently don't have %s, please send in the request "
                    "for it." % crypto_class)

        # return crypto class
        return crypto_class_instance

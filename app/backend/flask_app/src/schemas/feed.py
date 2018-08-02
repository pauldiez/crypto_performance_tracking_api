-
from flask_marshmallow import exceptions
from src.models import FeedModel
from src.app import mm


class FeedSchema(mm.ModelSchema):
    """FeedSchema data validation"""

    class Meta:
        model = FeedModel

        # You only need this line if you only want to serialize specific
        # fields from the model object.
        fields = ('id', 'symbol', 'data', 'totals', 'date_added')

    def validate_symbol(self, symbol):
        """Validate crypto currency symbol

        :param symbol:
        :return sting: crypto currency symbol
        """
        if symbol not in FeedModel.CRYPTO_SYMBOLS:
            raise exceptions.ValidationError('Invalid Symbol')

    symbol = mm.Str(required=True, allow_none=False, validate=validate_symbol)

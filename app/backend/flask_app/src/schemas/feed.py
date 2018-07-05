-from flask_marshmallow import exceptions
from src.models import FeedModel
from src.app import mm



class FeedSchema(mm.ModelSchema):
    class Meta:
        model = FeedModel
        fields = ('id', 'symbol', 'data', 'totals', 'date_added') #you only need this line if you only want to serialize specific fields from the model object

    def validate_symbol(symbol):
        if symbol not in FeedModel.CRYPTO_SYMBOLS:
            raise exceptions.ValidationError('Invalid Symbol')

    symbol = mm.Str(required=True, allow_none=False, validate=validate_symbol)

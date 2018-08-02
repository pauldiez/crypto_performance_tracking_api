from passlib.context import CryptContext
from src.config import Config

"""passlib library settings override
Import the CryptContext class, used to handle all hashing.
https://passlib.readthedocs.io/en/stable/lib/passlib.apps.html#custom-applications
"""

pwd_context = CryptContext(
    # Replace this list with the hash(es) you wish to support.
    # options ["bcrypt", "pbkdf2_sha256", "des_crypt"]
    schemes=Config.ENCRYPTION_TYPE_PRIORITIES,

    # Automatically mark all but first hasher in list as deprecated.
    # (this will be the default in Passlib 2.0)
    deprecated="auto",

    # Optionally, set the number of rounds that should be used.
    # Appropriate values may vary for different schemes,
    # and the amount of time you wish it to take.
    # Leaving this alone is usually safe, and will use passlib's defaults.
    ## pbkdf2_sha256__rounds = 29000,
)

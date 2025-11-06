import logging
from enum import Enum

logger = logging.getLogger(__name__)


class Environment(Enum):
    """Enum class for the accepted enviroments.

    Args:
        Enum (_type_): _description_

    Returns
    -------
        _type_: _description_
    """

    LOCAL = "local"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"

    @classmethod
    def _is_valid_environment(cls, value: str) -> bool:
        return value in cls._value2member_map_

    @classmethod
    def check_value(cls, value: str):
        """Validate if the enviroment is a accepted enviroment.

        Args:
            value (str): _description_
        """
        if not cls._is_valid_environment(value=value):
            message_error = f"{value} is not a valid environment value."
            logger.error(message_error)


class EnvPrefix(str, Enum):
    """Prefix for the config env determined by the enviroment selected.

    Args:
        str (_type_): _description_
        Enum (_type_): _description_
    """

    LOCAL = "LOCAL_"
    DEVELOPMENT = "DEV_"
    STAGING = "STG_"
    PRODUCTION = "PROD_"
    TESTING = "TEST_"

from pydantic_settings import SettingsConfigDict

from core.utils.environment import EnvPrefix

from .base import Settings


class ProductionSettings(Settings):
    """Production enviroment settings class.

    Args:
        Settings (_type_): _description_
    """

    model_config = SettingsConfigDict(env_prefix=EnvPrefix.PRODUCTION)

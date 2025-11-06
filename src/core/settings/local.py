from pydantic_settings import SettingsConfigDict

from core.settings import Settings
from core.utils.environment import EnvPrefix


class LocalSettings(Settings):
    """Local enviroment settings class.

    Args:
        Settings (_type_): _description_
    """

    model_config = SettingsConfigDict(env_prefix=EnvPrefix.LOCAL)

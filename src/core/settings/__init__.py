from logging.config import dictConfig
from typing import ClassVar

# import sentry_sdk
import structlog
from pydantic import BaseModel
# from sentry_sdk.integrations.fastapi import FastApiIntegration

from .base import ENVIRONMENT, Environment, Settings
from .development import DevelopmentSettings
from .local import LocalSettings
from .production import ProductionSettings
from .staging import StagingSettings
from .testing import TestingsSettings

log = structlog.get_logger()


class LogConfig(BaseModel):
    """Set base settings model for Logs.

    Args:
        BaseModel (_type_): _description_
    """

    LOG_FORMAT: str = "%(levelprefix)s \033[36m\033[1m[%(asctime)s | %(name)s:%(lineno)d]: \033[0m%(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: dict = {
        "": {"handlers": ["default"], "level": LOG_LEVEL},
    }


log_config_dict = LogConfig().__dict__
dictConfig(LogConfig().model_dump())


class SettingsManager:
    """
    Manages the settings based on the provided environment.

    Attributes
    ----------
        environment (str): The specified environment.
        settings (Settings): The settings corresponding to the environment.

    Class Attributes:
        SETTINGS_CLASS_DICT (dict): Mapping of environment values to their respective settings classes.
    """

    SETTINGS_CLASS_DICT: ClassVar = {
        Environment.LOCAL.value: LocalSettings,
        Environment.DEVELOPMENT.value: DevelopmentSettings,
        Environment.STAGING.value: StagingSettings,
        Environment.PRODUCTION.value: ProductionSettings,
        Environment.TESTING.value: TestingsSettings,
    }

    def __init__(self, environment):
        """
        Initialize the SettingsManager for the given environment.

        Parameters
        ----------
            environment (str): The specified environment.
        """
        self.environment = environment
        self.settings = self._get_settings()
        self._initialize_settings()

    def _initialize_settings(self):
        """
        Perform environment-specific actions or initializations.

        For specific environment configurations, you can add conditions
        inside this method.

        Example:
            For the LOCAL environment, you might want to enable detailed debug logging.
            This could be done as:
                if self.environment == Environment.LOCAL:
                    self._enable_debug_logging()

            Where `_enable_debug_logging` is a method that sets up a logging configuration
            for finer-grained debugging.
        """

    def _get_settings(self):
        """
        Fetch the settings class based on the environment.

        Returns
        -------
            Settings: An instance of the settings class corresponding to the environment.

        Raises
        ------
            ValueError: If the environment value is unrecognized.
        """
        try:
            settings_class = self.SETTINGS_CLASS_DICT[self.environment]
        except KeyError:
            raise ValueError(f"Unrecognized environment value: {self.environment}")  # noqa: B904, TRY200
        return settings_class()


settings: Settings = SettingsManager(environment=ENVIRONMENT).settings

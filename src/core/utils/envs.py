from pathlib import Path

from core.utils.logs import logger

BASEDIR = Path(__file__).resolve().parent.parent.parent

enviroments = {
    "local": "local",
    "development": "dev",
    "staging": "stg",
    "production": "prd",
    "testing": "test",
}


def get_envs_files_path(environment: str):
    """Get envs files from the path.

    Args:
        environment (str): _description_

    Returns
    -------
        _type_: _description_
    """
    logger.info(f"Environment: {environment}")
    suffix = enviroments[environment]
    env_file_name = f"envs/.env.{suffix}"
    return Path.joinpath(BASEDIR, env_file_name)

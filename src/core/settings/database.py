import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from core.settings import settings

logger = logging.getLogger(__name__)

application_name = settings.PROJECT_NAME.replace(" ", "-").lower()

Base = declarative_base()


if settings.ENVIRONMENT.value in ["local", "testing"]:
    engine = create_engine(
        settings.POSTGRESQL_URL.unicode_string(),
        connect_args={
            "application_name": application_name,
            "options": f"-c timezone={settings.TIME_ZONE}",
        },
        client_encoding="utf8",
    )
else:
    # For Cloud SQL connection
    engine = create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            query={"unix_sock": f"{settings.INSTANCE_UNIX_SOCKET}/.s.PGSQL.5432"},
        ),
        connect_args={"application_name": application_name},
        client_encoding="utf8",
    )


def get_session():
    """Get session sqlalchemy in an generator format.

    Yields
    ------
        _type_: _description_
    """

    if settings.ENVIRONMENT.value in ["local", "testing"]:
        engine = create_engine(
            settings.POSTGRESQL_URL.unicode_string(),
            connect_args={
                "application_name": application_name,
                "options": f"-c timezone={settings.TIME_ZONE}",
            },
            client_encoding="utf8",
        )
    else:
        # For Cloud SQL connection
        engine = create_engine(
            sqlalchemy.engine.url.URL.create(
                drivername="postgresql+pg8000",
                username=settings.DB_USER,
                password=settings.DB_PASSWORD,
                database=settings.DB_NAME,
                query={"unix_sock": f"{settings.INSTANCE_UNIX_SOCKET}/.s.PGSQL.5432"},
            ),
            connect_args={"application_name": application_name},
            client_encoding="utf8",
        )
    try:
        session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
        yield session
    except Exception as e:  # noqa: BLE001
        logger.error(str(e))  # noqa: TRY400
        session.rollback()
    finally:
        session.close()
        engine.dispose()

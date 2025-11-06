# Standard Library
import json
import logging

# Third Party Stuff
from fastapi import status as status_codes
from fastapi.exceptions import ResponseValidationError
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from core.utils.exceptions import (
    NotFoundError,
    PlatformNotValidError,
)
from core.utils.responses import envelope_error_response

logger = logging.getLogger(__name__)


class CatcherExceptionsMiddleware(BaseHTTPMiddleware):
    """Return envelope_response format error exceotion.

    Args:
        BaseHTTPMiddleware (_type_): _description_
    """

    def __init__(self, app):
        super().__init__(app)


    async def dispatch(self, request: Request, call_next):  # pragma no cover  # noqa: D102, C901
        try:
            response = await call_next(request)
        except ValidationError as exc:
            message = ""
            for error in exc.errors():
                message += f"{error['msg']}: {error['loc'][0]}. "
            response = envelope_error_response(
                errors=[{"error": f"{message}"}],
                status=status_codes.HTTP_400_BAD_REQUEST,
            )
            exc = str(json.loads(response.body))
            logger.warning(f"⚠️ ➡️ {exc}")
        except ResponseValidationError as e:
            response = envelope_error_response(
                errors={
                    "error": "Ha ocurrido un error procesando tu solicitud.",
                    "error_detail": f"{e}",
                },
                status=status_codes.HTTP_400_BAD_REQUEST,
            )
            logger.warning(f"⚠️ ➡️ {e}")
        except PlatformNotValidError as e:
            exc_msg = str(e).split("|")
            response = envelope_error_response(
                errors={
                    "error": exc_msg[0],
                    "error_detail": exc_msg[1],
                },
                status=status_codes.HTTP_404_NOT_FOUND,
            )
            logger.warning(f"⚠️ ➡️ {e}")
        except NotFoundError as e:
            exc_msg = str(e).split("|")
            response = envelope_error_response(
                errors={
                    "error": exc_msg[0],
                    "error_detail": exc_msg[1],
                },
                status=status_codes.HTTP_404_NOT_FOUND,
            )
            logger.warning(f"⚠️ ➡️ {e}")
        except Exception as exc:  # noqa: BLE001
            logger.error(f"Exception error: {exc}")  # noqa: TRY400
            response = envelope_error_response(
                errors=[{"error": f"Ha ocurrido un error en el servidor. {exc!s}"}],
                status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            msg = f"❌ ➡️ {exc}"
            logger.error(msg=msg, exc_info=(type(exc), exc, exc.__traceback__))  # noqa: TRY400

        return response

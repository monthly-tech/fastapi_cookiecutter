import structlog

logger: structlog = structlog.get_logger(__name__)


def loghead(message: str = "", separator: str = "-", n: int = 20) -> None:  # pragma: no cover
    """Format a message with a separator and logs it using the `logger` function.

    Args:
        message (str, optional): _description_. Defaults to "".
        separator (str, optional): _description_. Defaults to "-".
        n (int, optional): _description_. Defaults to 20.
    """
    message_len = len(message)
    if message_len >= n:
        n = 20

    s = separator * n
    message_format = f"{s} {message} {s}"

    logger.info(message_format)

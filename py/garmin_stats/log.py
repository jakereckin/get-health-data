import logging
import os
import time
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


# ============================================================================
def log_time(func):


    def wrapper(*arg, **kw):
        start = time.perf_counter()
        res = func(*arg, **kw)
        end = time.perf_counter()
        my_time = round(end-start, 2)
        logging.info(msg=f'Exection time for {func.__name__}: {my_time} seconds')
        return res
    return wrapper


# ============================================================================
def end_log() -> None:
    logging.info(msg='__RUN END__\n')
    return None


# ============================================================================
def log_exception(exception) -> None:
    logging.error(msg=exception, exc_info=True)
    return None


# ============================================================================
def start_log() -> None:
    logging.info(msg='__RUN START__')
    return None

# ============================================================================
def log_info(msg: str) -> None:
    logging.info(msg=msg)
    return None

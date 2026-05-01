import logging
import os
import time
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


LOG = logging.getLogger(name=__name__)


# ============================================================================
def setup_log() -> None:
    parent_path = Path(__file__).parent.parent.parent
    LOG_FILE_NAME = os.path.join(parent_path, 'log/process_log.log')

    file_handler = TimedRotatingFileHandler(
        filename=LOG_FILE_NAME, when='midnight', interval=1, backupCount=10
    )

    logging.basicConfig(
        handlers=[file_handler], format='%(asctime)s %(message)s',
        level=logging.INFO, datefmt='%m/%d/%Y %H:%M'
    )

    return None


# ============================================================================
def log_time(func):
    def wrapper(*arg, **kw):
        start = time.perf_counter()
        res = func(*arg, **kw)
        end = time.perf_counter()
        my_time = round(end-start, 2)
        LOG.info(msg=f'Exection time for {func.__name__}: {my_time} seconds')
        return res
    return wrapper


# ============================================================================
def end_log() -> None:
    LOG.info(msg='__RUN END__\n')
    return None


# ============================================================================
def log_exception(exception) -> None:
    LOG.error(msg=exception, exc_info=True)
    return None


# ============================================================================
def start_log() -> None:
    LOG.info(msg='__RUN START__')
    return None

# ============================================================================
def log_info(msg: str) -> None:
    LOG.info(msg=msg)
    return None

import datetime
import logging

import os
from pytz import UTC

from krk.config import RESULT_FOLDER

l = logging.getLogger(__name__)


def write_file(content, filename):
    if not is_path(filename):
        path = os.path.join(RESULT_FOLDER, filename)
    else:
        path = filename
    l.info("Writing file %s", path)
    with open(path, "wb") as f:
        f.write(content)
    return path


def is_path(filename):
    try:
        return filename.index("/") > -1
    except ValueError:
        return False


def ensure_dt(t):
    """
    Ensure t is proper offset-aware datetime

    :param t:
    :return:
    """

    if isinstance(t, int) or isinstance(t, float):
        # Todo: A more robust checking for millisecond timestamp,
        # i.e. if the timestamp convert to a very large year,
        # it is probably in millisecond format.
        d = datetime.fromtimestamp(t, tz=UTC)
        return d
    return t

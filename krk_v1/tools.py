import logging

import os

from krk_v1 import RESULT_FOLDER

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
        r = filename.index("/") > -1
        return True
    except ValueError:
        return False

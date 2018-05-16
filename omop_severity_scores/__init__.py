"""Init."""

import sys
import os.path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import userpaths
from fleming_lib import paths  # noqa: E402, F401

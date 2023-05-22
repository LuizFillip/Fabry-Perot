from .core import FPI, resample_and_interpol, load_FPI
from .base import running_avg

import settings as s

s.config_labels()
from .plotting import *
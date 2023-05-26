from .core import FPI, load_FPI
from .base import  process_day
from .fpi_utils import date_from_filename
import settings as s

s.config_labels()
from .plotting import *
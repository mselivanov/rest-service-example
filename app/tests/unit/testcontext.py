import sys
from os.path import realpath, dirname, join, expanduser


application_path = realpath(expanduser(join(dirname(__file__), "..", "..")))
sys.path.append(application_path)

import customersvc.models.customer_models as model


try:
    import supervisely
except ImportError:
    import sys

    import sly_sdk as supervisely

    sys.modules["supervisely"] = supervisely

from src.main import app

app.run
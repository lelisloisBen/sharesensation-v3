from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import importlib
import os

db = SQLAlchemy()
ma = Marshmallow()

MODELS_DIRECTORY = "database\model"
EXCLUDE_FILES = ["__init__.py"]

def import_models():
    for dir_path, dir_names, file_names in os.walk(MODELS_DIRECTORY):
        for file_name in file_names:
            if file_name.endswith("py") and file_name not in EXCLUDE_FILES:
                file_path = os.path.join(dir_path, file_name)
                file_path_wo_ext, _ = os.path.splitext(file_path)
                module_name = file_path_wo_ext.replace(os.sep, ".")
                importlib.import_module(module_name)

import_models()

def init_app(app):
    db.init_app(app)
    db.create_all(app=app)

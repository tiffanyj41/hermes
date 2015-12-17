"""Global helper functions"""

import os 
import json
from pyspark.sql.types import StructType


def is_filepath_valid(filepath):
    return True if os.path.isfile(filepath) else False

def get_schema(schema_path):
    if not schema_path:
        return None
    with open(schema_path, "r") as schema_file:
        return StructType.fromJson(json.load(schema_file))

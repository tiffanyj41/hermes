"""Global helper functions"""

import imp
import importlib
import inspect
import json
import md5
import os
import traceback 

from pyspark.sql.types import StructType

from hermesglobals import Globals

def is_filepath_valid(filepath):
    return True if os.path.isfile(filepath) else False

def get_schema(schema_path):
    if not schema_path:
        return None
    with open(schema_path, "r") as schema_file:
        return StructType.fromJson(json.load(schema_file))

def load_modules_in_dir(dir_path):
    try:
        try:
            for root, dirs, files in os.walk(dir_path):
                for filename in files:
                    if filename.endswith(".py"):
                        # current_file == module
                        thisfilepath = os.path.join(root, filename)
                        thisfile = open(thisfilepath, "rb")
                        # use md5.new to generate unique module identifier
                        # in case there are two modules of the same name
                        # assumption: no subdirectory within dir_path 
                        module = imp.load_source(md5.new(thisfilepath).hexdigest(), thisfilepath, thisfile)
                        yield module
                        thisfile.close()
        finally:
            try: thisfile.close()
            except: pass
    except ImportError as err:
        Globals.logger.error(err, exc_info=True)
        raise
    except Exception as err:
        Globals.logger.error(err, exc_info=True)
        raise

# return generator of direct descendants
def get_direct_subclasses(module, cls):
    try:
        for name, obj in inspect.getmembers(module):
            # 1. check that obj is a class 
            if inspect.isclass(obj):
                # 2. check that obj is a direct descendant of class
                if cls in obj.__bases__:
                    yield obj
                else:
                    # WARNING: assumption that there is only one class of the same name in all of the modules
                    for objparent in obj.__bases__:
                        if objparent.__name__ == cls.__name__:
                            yield obj
    except Exception as err:
        Globals.logger.error(err, exc_info=True)

# return generator of descendants including non-direct ones
def get_non_direct_subclasses(module, cls):
    try:
        for name, obj in inspect.getmembers(module):
            # 1. check that obj is a class 
            if inspect.isclass(obj):
                # 2. check that obj is a direct descendant of class
                if issubclass(obj, cls):
                    yield obj
                else:
                    # WARNING: assumption that there is only one class of the same name in all of the modules
                    for objparent in obj.__bases__:
                        if objparent.__name__ == cls.__name__:
                            yield obj
    except Exception as err:
        Globals.logger.error(err, exc_info=True)




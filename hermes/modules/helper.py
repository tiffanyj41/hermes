"""Global helper functions"""

import imp
import importlib
import inspect
import json
import md5
import os
import traceback 
import zipfile
import zipimport

from pyspark.sql.types import StructType

from hermesglobals import Globals

def is_filepath_valid(filepath):
    return True if os.path.isfile(filepath) else False

def get_schema(schema_path):
    if not schema_path:
        return None
    with open(schema_path, "r") as schema_file:
        return StructType.fromJson(json.load(schema_file))

def load_modules_in_zip(zipfile_path, which_dir):
    try:
        try:
            zh = zipfile.ZipFile(zipfile_path)
            zi = zipimport.zipimporter(zipfile_path)
            for name in zh.namelist():
                if os.path.basename(os.path.dirname(name)) == which_dir:
                    module = zi.load_module(os.path.splitext(name)[0])
                    yield module
        finally:
            try: zh.close()
            except: pass
    except Exception as err:
        Globals.logger.error(err, exc_info=True)
        raise


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

# check whether checkcls is the cls or direct subclass of cls
def is_direct_subclass(obj, cls):
    # 1. make sure that checkcls is a class object
    checkcls = obj
    if not inspect.isclass(obj):
        checkcls = obj.__class__
    # 2. check if checkcls == cls; if it is, return True
    # 3. check if cls is a direct parent of checkcls
    return type(checkcls) == type(cls) or cls in checkcls.__bases__ 

# check whether checkcls it the cls or non-direct subclass of cls
def is_non_direct_subclass(checkcls, cls):
    # 1. make sure that checkcls is a class object
    checkcls = obj
    if not inspect.isclass(obj):
        checkcls = obj.__class__
    # 2. check if checkcls == cls; if it is, return True
    # 3. check if checkcls ia  subclass of cls
    return type(checkcls) == type(cls) or issubclass(checkcls, cls) 


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




import os
import importlib

# This loads all the files and imports all the  class in the directory during the startup
package_dir = os.path.dirname(__file__)

# Loads all the class defined in "actions" directory, so that it can be accessed dynamically
for filename in os.listdir(package_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]

        importlib.import_module(f".{module_name}", package=__name__)

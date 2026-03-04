import sys

# This is bad practice, we are doing this to make testing easier.
# Do not ship something like this!
from molecular_test_common import *

if not append_import_directory():
    sys.exit(1)
else:
    import molaccesspy
    
    sys.path.append(f"{TestData.script_directory}/{TestData.depth_traversal_string}/apps")

    import molaccessd
    from molaccessd import cli

if __name__ == "__main__":
    cli.main()

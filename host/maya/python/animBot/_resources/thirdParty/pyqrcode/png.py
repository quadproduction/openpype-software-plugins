import sys

_ = int(sys.version_info[0])

if _ == 2:
    from .png2 import *

if _ == 3:
    from .png3 import *

# since we are not compiling pyc, it should be just fine to separate only 2 versions

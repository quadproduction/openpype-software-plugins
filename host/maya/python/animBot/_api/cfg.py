
import sys
_ = int("%s%s" % (sys.version_info[0], sys.version_info[1]))
        
            
if _ == 27:    
    from .__hybrid__.cfg27 import *
            
if _ == 37:    
    from .__hybrid__.cfg37 import *
            
if _ == 39:    
    from .__hybrid__.cfg39 import *
            
if _ == 310:    
    from .__hybrid__.cfg310 import *

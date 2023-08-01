
import sys
_ = int("%s%s" % (sys.version_info[0], sys.version_info[1]))
        
            
if _ == 27:    
    from .__hybrid__.attributeSpaceSwitcherUI27 import *
            
if _ == 37:    
    from .__hybrid__.attributeSpaceSwitcherUI37 import *
            
if _ == 39:    
    from .__hybrid__.attributeSpaceSwitcherUI39 import *
            
if _ == 310:    
    from .__hybrid__.attributeSpaceSwitcherUI310 import *

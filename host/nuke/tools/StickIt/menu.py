''' Add this to your menu.py '''
import nuke

# Hagbarth Tools
toolbar = nuke.toolbar("Nodes")
m = toolbar.addMenu("Hagbarth Tools", icon="h_tools.png")
m.addCommand(
    "StickIt",
    "nuke.createNode(\"h_stickit\")",
    icon="h_stickit.png"
)

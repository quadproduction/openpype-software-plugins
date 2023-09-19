import nuke

def run():

    import sys
    if sys.version_info >= (3, ):
        from importlib import reload

    path = "/prod/rolex/repos/td-films/main/td_tools"

    if not path in sys.path:
        sys.path.append(path)

    from nuke.shelf_scripts import layer_splitter
    reload(layer_splitter)

    layer_splitter.run_script()

print('Loading rolex_tools...')
rlx_tools = nuke.menu('Nodes').addMenu('Rolex_tools')
rlx_tools.addCommand('Layer_splitter', 'run()')

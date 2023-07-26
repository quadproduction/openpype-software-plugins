import logging

from maya import cmds


logger = logging.getLogger(__name__)


def snap():
    """
    this awesome function, snap an object to an other.
    """

    # get selection
    sels = cmds.ls(sl=True, l=True)

    if sels:
        if len(sels) == 2:
            cmds.parentConstraint(
                sels[0],
                sels[1],
                skipTranslate="none",
                skipRotate="none",
                maintainOffset=False
            )
            cmds.scaleConstraint(sels[0], sels[1], maintainOffset=False)
            cmds.delete(sels[1], constraints=True)
        else:
            logging.error("Can't snap")
            return
    else:
        logging.error("Can't snap")
        return

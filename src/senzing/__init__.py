# Tricky code:
# Because the filenames are the same as class names in many instances,
# the __all__ list needs to be constructed from the files before the
# classes are imported.   For that reason, there is a 2-step process:
#   1) Use the "names" as filenames to access the "__all__" attribute.
#   2) Use the "names" as class names.

# Step 1: Import the files so that the __all__ attribute will work with the "name" (e.g. g2config, g2configmgr)

from . import (
    g2config,
    g2configmgr,
    g2diagnostic,
    g2engine,
    g2engineflags,
    g2exception,
    g2hasher,
    g2product,
)

import_lists = [
    g2config.__all__,
    g2configmgr.__all__,
    g2diagnostic.__all__,
    g2engine.__all__,
    g2engineflags.__all__,
    g2exception.__all__,
    g2hasher.__all__,
    g2product.__all__,
]

__all__ = []
for import_list in import_lists:
    __all__.extend(import_list)

# Step 2: Overwrite the "name" that did point to the file in step #1 to now point to the class.
# Each of the submodules must have the having an __all__ variable defined for the "*" to work.

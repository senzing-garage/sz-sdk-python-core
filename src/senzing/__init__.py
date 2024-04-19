# Tricky code:
# Because the filenames are the same as class names in many instances,
# the __all__ list needs to be constructed from the files before the
# classes are imported.   For that reason, there is a 2-step process:
#   1) Use the "names" as filenames to access the "__all__" attribute.
#   2) Use the "names" as class names.

# Step 1: Import the files so that the __all__ attribute will work with the "name" (e.g. szconfig, szconfigmgr)

from typing import List

from . import (
    szconfig,
    szconfigmanager,
    szdiagnostic,
    szengine,
    szengineflags,
    szerror,
    szhasher,
    szproduct,
)

import_lists = [
    szconfig.__all__,
    szconfigmanager.__all__,
    szdiagnostic.__all__,
    szengine.__all__,
    szengineflags.__all__,
    szerror.__all__,
    szhasher.__all__,
    szproduct.__all__,
]

__all__: List[str] = []
# for import_list in import_lists:
#     __all__.extend(import_list)

# Step 2: Overwrite the "name" that did point to the file in step #1 to now point to the class.
# Each of the submodules must have the having an __all__ variable defined for the "*" to work.

#! /usr/bin/env python3

from senzing import SzEngineFlags

RESULT = SzEngineFlags.flags_by_value()
print(f"\n{RESULT}\n")

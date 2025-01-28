#! /usr/bin/env python3

from senzing import SzEngineFlags

RESULT = SzEngineFlags.flags_by_name()
print(f"\n{RESULT}\n")

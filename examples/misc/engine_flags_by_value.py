#! /usr/bin/env python3

from senzing import SzEngineFlags

result = SzEngineFlags.flags_by_value()
print(f"\n{result}\n")

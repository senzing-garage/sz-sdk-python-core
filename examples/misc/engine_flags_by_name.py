#! /usr/bin/env python3

from senzing import SzEngineFlags

result = SzEngineFlags.flags_by_name()
print(f"\n{result}\n")

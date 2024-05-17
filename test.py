#! /usr/bin/env python3
import json

try:
    int("s")
except ValueError as err:
    print(err)

print()
# int("a")
# print()

try:
    json.loads(1)
except TypeError as err:
    print(err)

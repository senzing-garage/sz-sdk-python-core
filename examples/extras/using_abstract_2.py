#! /usr/bin/env python3

from senzing import SzAbstractFactory, SzEngine, SzError

__all__ = ["try_using_abstract"]


def get_stats(sz_engine: SzEngine) -> None:
    """Example of using SzEngine"""
    try:
        stats = sz_engine.get_stats()
        print(f"Stats: {stats}")
    except SzError as err:
        print(f"\nFile {__file__}:\nError:\n{err}\n")


def try_using_abstract(sz_abstract_factory: SzAbstractFactory) -> None:
    """Example of using SzAbstractFactory"""
    try:
        sz_product = sz_abstract_factory.create_product()
        version = sz_product.get_version()
        print(f"Version: {version}")
        sz_engine = sz_abstract_factory.create_engine()
        get_stats(sz_engine)
    except SzError as err:
        print(f"\nFile {__file__}:\nError:\n{err}\n")

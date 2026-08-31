"""favs.duckdb - favourite additional duckdb functions - Olaf, 31 Aug 2026."""
import csv
import io
import operator
from collections.abc import Iterable, Iterator, Mapping
from typing import Annotated

import duckdb
from annotated_types import Predicate
from duckdb.sqltypes import DuckDBPyType

from .dicttools import map_mapping_values
from .itertools import mark_first


def is_homogenous(row: Mapping[str, object]) -> bool: return False


@operator.call                                      # evaluate once
def _python_to_sql_type_lookup() -> Mapping[type, DuckDBPyType]:
    import ctypes
    import datetime
    import decimal
    import types
    import uuid

    import duckdb.sqltypes as sqltypes

    return {ctypes.c_int8: sqltypes.TINYINT,        # signed integers
            ctypes.c_int16: sqltypes.SMALLINT,
            ctypes.c_int32: sqltypes.INTEGER,
            ctypes.c_int64: sqltypes.BIGINT,
            ctypes.c_longlong: sqltypes.HUGEINT,
            ctypes.c_uint8: sqltypes.UTINYINT,      # unsigned integers
            ctypes.c_uint16: sqltypes.USMALLINT,
            ctypes.c_uint32: sqltypes.UINTEGER,
            ctypes.c_uint64: sqltypes.UBIGINT,
            ctypes.c_ulonglong: sqltypes.UHUGEINT,
            ctypes.c_float: sqltypes.FLOAT,         # floating/decimal numbers
            ctypes.c_double: sqltypes.DOUBLE,
            decimal.Decimal: duckdb.DecimalValue,   # FIXME: this needs work probably
            datetime.date: sqltypes.DATE,           # temporal types
            datetime.time: sqltypes.TIME,
            datetime.datetime: sqltypes.TIMESTAMP,
            datetime.timedelta: sqltypes.INTERVAL,
            uuid.UUID: sqltypes.UUID,               # UUID
            types.NoneType: sqltypes.SQLNULL,       # missing/unknown data type
            } | {
            typ: DuckDBPyType(typ)                  # directly recognized by `DuckDBPyType`
            for typ in (int, float, bool, str, bytes, bytearray)
            }


def _sql_type[T](cls: type[T], /) -> DuckDBPyType:
    """Return SQL type equivalent to Python type `cls`.

    >>> _sql_type(int)
    BIGINT
    """
    return _python_to_sql_type_lookup[cls]


def _sql_type_str[T](instance: T, /) -> str:
    """Return name of SQL type of Python `instance`.

    >>> _sql_type_str(42)  # 42 -> int -> BIGINT -> 'BIGINT'
    'BIGINT'
    """
    cls = type(instance)
    return str(_sql_type(cls))


def relation_from_dicts(dict_rows: Annotated[Iterable[Mapping[str, object]], Predicate(is_homogenous)], /, *,
                        connection: duckdb.DuckDBPyConnection | None = None) -> duckdb.DuckDBPyRelation:
    """Return new DuckDB relation at `connection` (default is DuckDB's default) from `dict_rows`.

    Column names and types are taken from first row; values come from all rows.
    Note homogeneity over `dict_rows` is required.

    >>> def rows() -> Iterator[Mapping[str, object]]:
    ...     for i in range(4):
    ...         yield dict(i=i, square=float(i * i), name=f"name-{i}")
    >>> relation_from_dicts(rows()).show()  # doctest: +NORMALIZE_WHITESPACE
    ┌───────┬────────┬─────────┐
    │   i   │ square │  name   │
    │ int64 │ double │ varchar │
    ├───────┼────────┼─────────┤
    │     0 │    0.0 │ name-0  │
    │     1 │    1.0 │ name-1  │
    │     2 │    4.0 │ name-2  │
    │     3 │    9.0 │ name-3  │
    └───────┴────────┴─────────┘
    """
    conn = duckdb if connection is None else connection

    with io.StringIO(newline='') as stream:
        columns: Mapping[str, str] = {}                                # initialize to track no-rows situation
        for dict_row, first in mark_first(dict_rows):
            if first:
                columns = map_mapping_values(_sql_type_str, dict_row)  # column name -> SQL type name
                csv_writer = csv.DictWriter(stream, columns.keys())
                csv_writer.writeheader()                               # cache header to `stream`
            csv_writer.writerow(dict_row)                              # cache data to `stream`

        stream.seek(0)                                                 # rewind stream to ingest from start
        if columns:
            return conn.read_csv(stream, columns=columns)
        else:                                                          # handle no-rows situation with undefined columns
            return conn.read_csv(stream)

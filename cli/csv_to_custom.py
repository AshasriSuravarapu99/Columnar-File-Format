from custom_format.writer import ColumnarWriter
from custom_format.schema import Column, INT32, FLOAT64, STRING
import sys

schema = [
    Column("id", INT32),
    Column("name", STRING),
    Column("salary", FLOAT64)
]

ColumnarWriter(sys.argv[2]).write(sys.argv[1], schema)

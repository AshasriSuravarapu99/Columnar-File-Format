import csv
import struct
from .schema import INT32, FLOAT64, STRING, Column
from .utils import pack_int, pack_long, pack_byte, compress

MAGIC = b"CSTM"

class ColumnarWriter:
    def __init__(self, output_file):
        self.output_file = output_file

    def write(self, csv_file, schema):
        with open(csv_file, newline="") as f:
            reader = list(csv.reader(f))
            header, rows = reader[0], reader[1:]

        columns_data = {col.name: [] for col in schema}

        for row in rows:
            for i, col in enumerate(schema):
                columns_data[col.name].append(row[i])

        with open(self.output_file, "wb") as f:
            f.write(MAGIC)
            f.write(pack_int(len(schema)))
            f.write(pack_int(len(rows)))

            header_start = f.tell()

            # Placeholder header
            for col in schema:
                f.write(pack_int(len(col.name)))
                f.write(col.name.encode())
                f.write(pack_byte(col.dtype))
                f.write(pack_long(0))
                f.write(pack_long(0))
                f.write(pack_long(0))

            # Write columns
            for col in schema:
                col.offset = f.tell()

                raw = b""
                if col.dtype == INT32:
                    raw = b"".join(struct.pack("<i", int(v)) for v in columns_data[col.name])
                elif col.dtype == FLOAT64:
                    raw = b"".join(struct.pack("<d", float(v)) for v in columns_data[col.name])
                elif col.dtype == STRING:
                    offsets = []
                    data = b""
                    pos = 0
                    for v in columns_data[col.name]:
                        b = v.encode()
                        pos += len(b)
                        offsets.append(pos)
                        data += b
                    raw = b"".join(struct.pack("<i", o) for o in offsets) + data

                compressed = compress(raw)
                col.compressed_size = len(compressed)
                col.uncompressed_size = len(raw)
                f.write(compressed)

            # Rewrite header with real metadata
            f.seek(header_start)
            for col in schema:
                f.write(pack_int(len(col.name)))
                f.write(col.name.encode())
                f.write(pack_byte(col.dtype))
                f.write(pack_long(col.offset))
                f.write(pack_long(col.compressed_size))
                f.write(pack_long(col.uncompressed_size))

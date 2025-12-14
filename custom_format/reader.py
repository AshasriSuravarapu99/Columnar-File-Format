import struct
from .utils import decompress
from .schema import INT32, FLOAT64, STRING


class ColumnarReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self, columns=None):
        with open(self.file_path, "rb") as f:
            # Read header
            magic = f.read(4)
            num_cols = struct.unpack("<i", f.read(4))[0]
            num_rows = struct.unpack("<i", f.read(4))[0]

            # Read column metadata
            metadata = []
            for _ in range(num_cols):
                name_len = struct.unpack("<i", f.read(4))[0]
                name = f.read(name_len).decode("utf-8")
                dtype = struct.unpack("<b", f.read(1))[0]
                offset = struct.unpack("<q", f.read(8))[0]
                csize = struct.unpack("<q", f.read(8))[0]
                usize = struct.unpack("<q", f.read(8))[0]
                metadata.append((name, dtype, offset, csize, usize))

            result = {}

            # Read required columns only (column pruning)
            for name, dtype, offset, csize, _ in metadata:
                if columns and name not in columns:
                    continue

                f.seek(offset)
                data = decompress(f.read(csize))

                if dtype == INT32:
                    # FIX: extract scalar from tuple
                    result[name] = [v[0] for v in struct.iter_unpack("<i", data)]

                elif dtype == FLOAT64:
                    # FIX: extract scalar from tuple
                    result[name] = [v[0] for v in struct.iter_unpack("<d", data)]

                elif dtype == STRING:
                    offsets = [o[0] for o in struct.iter_unpack("<i", data[:4 * num_rows])]
                    strings = data[4 * num_rows:]
                    prev = 0
                    result[name] = []
                    for end in offsets:
                        result[name].append(strings[prev:end].decode("utf-8"))
                        prev = end

            return result

INT32 = 1
FLOAT64 = 2
STRING = 3

class Column:
    def __init__(self, name, dtype):
        self.name = name
        self.dtype = dtype
        self.offset = 0
        self.compressed_size = 0
        self.uncompressed_size = 0

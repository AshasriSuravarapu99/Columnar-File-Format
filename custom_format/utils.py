import struct
import zlib

def pack_int(value):
    return struct.pack("<i", value)

def pack_long(value):
    return struct.pack("<q", value)

def pack_byte(value):
    return struct.pack("<b", value)

def compress(data: bytes) -> bytes:
    return zlib.compress(data)

def decompress(data: bytes) -> bytes:
    return zlib.decompress(data)

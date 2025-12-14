# Custom Columnar File Format Specification

## Byte Order
Little-endian

## Header Layout
- Magic Number (4 bytes): b'CSTM'
- Number of Columns (4 bytes, int32)
- Number of Rows (4 bytes, int32)

For each column:
- Column Name Length (4 bytes)
- Column Name (UTF-8)
- Data Type (1 byte)
  - 1 = INT32
  - 2 = FLOAT64
  - 3 = STRING
- Column Offset (8 bytes, int64)
- Compressed Size (8 bytes)
- Uncompressed Size (8 bytes)

## Data Section
Each column stored as:
- Compressed binary block (zlib)

Strings:
- Stored as:
  - Offset array (int32[])
  - Concatenated UTF-8 string bytes

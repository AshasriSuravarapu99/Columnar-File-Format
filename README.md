# Custom Columnar File Format

## Overview

This project implements a **custom columnar binary file format** inspired by analytical storage formats like **Apache Parquet** and **ORC**. The goal of the project is to understand how such formats work internally by building a simplified version from scratch.

The format stores data **column-wise**, uses **zlib compression** for each column, and maintains **metadata with offsets** to enable **efficient selective column reads (column pruning)**. The project also provides command-line tools to convert data between CSV and the custom binary format.

---

## Features

* Custom binary file format with a documented specification (SPEC.md)
* Columnar storage (each column stored as a separate block)
* Support for data types:

  * 32-bit integers (INT32)
  * 64-bit floating-point numbers (FLOAT64)
  * Variable-length UTF-8 strings (STRING)
* Per-column compression using **zlib**
* Metadata-driven offsets for fast seeking
* Selective column reads (column pruning)
* CLI tools for CSV ↔ Custom format conversion

---

## Project Structure

```
custom_columnar_format/
├── custom_format/
│   ├── __init__.py
│   ├── schema.py
│   ├── writer.py
│   ├── reader.py
│   └── utils.py
├── cli/
│   ├── csv_to_custom.py
│   └── custom_to_csv.py
├── tests/
│   └── test_roundtrip.py
├── SPEC.md
├── README.md
└── requirements.txt
```

---

## Requirements

* Python **3.8 or higher**
* No external libraries are required (uses only Python standard library)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd custom_columnar_format
```

### 2. (Optional) Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux / macOS
```

### 3. Install Dependencies

This project does not require external dependencies. The standard Python library is sufficient.

```bash
pip install -r requirements.txt
```

---

## Usage Examples

### Prepare a Sample CSV File

Create a file named `test.csv` in the project root:

```csv
id,name,salary
1,Alice,50000.5
2,Bob,60000.75
3,Charlie,55000.25
```

---

### CSV → Custom Columnar Format

Run the CSV-to-custom converter from the **project root directory**.

#### Windows (Command Prompt)

```bat
set PYTHONPATH=.
python cli/csv_to_custom.py test.csv output.cstm
```

### Power Shell
```bash
python cli/csv_to_custom.py test.csv output.cstm
```


#### Linux / macOS

```bash
export PYTHONPATH=.
python cli/csv_to_custom.py test.csv output.cstm
```

This command creates a binary file named `output.cstm` in the custom columnar format.

---

### Custom Columnar Format → CSV

Convert the custom file back to CSV:

```bash
python cli/custom_to_csv.py output.cstm final.csv
```

The generated `final.csv` should match the original input CSV.

---

## Selective Column Read Example

You can read only specific columns without scanning the entire file:


```bash
python test_selective_column_read.py
```

This demonstrates **column pruning**, a core feature of analytical file formats.

---

## Testing

To verify correctness using round-trip conversion:

```bash
python tests/test_roundtrip.py
```

This test converts CSV → custom format → CSV and checks correctness.

---

## Documentation

* **SPEC.md** – Detailed binary file format specification
* **README.md** – Setup and usage instructions

---

## Summary

This project demonstrates a practical understanding of:

* Binary file format design
* Columnar storage concepts
* Metadata and offsets
* Compression and decompression
* Efficient analytical data access patterns


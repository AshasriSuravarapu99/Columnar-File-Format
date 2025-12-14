from custom_format.reader import ColumnarReader
import csv, sys

data = ColumnarReader(sys.argv[1]).read()

with open(sys.argv[2], "w", newline="") as f:
    writer = csv.writer(f)
    headers = data.keys()
    writer.writerow(headers)
    for i in range(len(next(iter(data.values())))):
        writer.writerow([data[h][i] for h in headers])

from custom_format.reader import ColumnarReader

reader = ColumnarReader("output.cstm")
data = reader.read(columns=["name", "salary"])

print(data)

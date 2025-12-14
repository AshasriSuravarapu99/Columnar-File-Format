import subprocess

subprocess.run(["python", "cli/csv_to_custom.py", "test.csv", "output.cstm"])
subprocess.run(["python", "cli/custom_to_csv.py", "output.cstm", "final.csv"])

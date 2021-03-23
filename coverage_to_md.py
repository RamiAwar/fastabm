import sys

lines = None
with open(sys.argv[1]) as f:
    lines = f.readlines()

# Find coverage
start_index = 0
for i, line in enumerate(lines):
    if line.split()[0] == "Name":
        start_index = i
    elif line.split()[0] == "TOTAL":
        stop_index = i

# Build table header
header = ["|"]
separator = ["|"]

headers = lines[start_index].split()
for i, name in enumerate(headers):
    header.append(name)
    header.append("|")

    if i == 0:
        separator.append(":-------------")
    elif i == len(headers):
        separator.append("-----------:")
    else:
        separator.append(":----------:")
    separator.append("|")

# Build table body
body = []
start_index += 1
stop_index += 1
for line in lines[start_index:stop_index]:
    x = ["|"]
    for word in line.split():
        x.extend([word, "|"])

    body.append(" ".join(x))

table = [" ".join(header), " ".join(separator), *body]

with open("table.md", "w") as f:
    f.write("\n".join(table))

import fileinput


for line in fileinput.input('items.xml', inplace=True):
    if '<?xml version="1.0" encoding="utf-8"?>' in line:
        continue
    print(line)



import os, sys

d = './ft_fun'
if len(sys.argv) > 1:
    d = sys.argv[1]

files = list(filter(lambda s: s.endswith('.pcap'), os.listdir(d)))
l = [''] * len(files)
for fname in files:
    file_name = "{}/{}".format(d, fname)
    with open(file_name) as f:
        lines = f.readlines()
    idx = int(lines[-1][6:])
    l[idx - 1] = ''.join(lines[:-1])
output = ''.join(l)

with open('main.c', 'w+') as f:
    f.write(output)
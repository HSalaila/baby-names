import sys
from src.pandashandler import *

if len(sys.argv) < 3 or len(sys.argv) > 4:
    print("Enter two names. Path is optional")
    print("e.g. analysis <name1> <name2> [<path>]")
    sys.exit()

n1 = sys.argv[1]
n2 = sys.argv[2]
if len(sys.argv) == 3:
    path = DEFAULT_PATH
else:
    path = sys.argv[3]

print("running analysis with names and path:")
print(n1)
print(n2)
print(path)
d = filter_two_names(read_csv(path), n1, n2)
for name, series in d.items():
    print(name + " mean: " + str(series.mean()) + " std: " + str(series.std()))

import sys
import pandas as pd


def read_csv(file):
    """"reads a specified csv file
    return pandas.DataFrame."""
    return pd.read_csv(file)


def filter_two_names(df, name1, name2):
    """filters the data frame on the specified names and groups it per year; regardless of gender.
    return dictionary key: <Name> value: pandas.DataFrame"""
    def filter_name_groupby_year(name):
        return df[df["Name"].isin([name])].groupby(["Year"])["Count"].sum()
    return {name1: filter_name_groupby_year(name1), name2: filter_name_groupby_year(name2)}

if len(sys.argv) < 3 or len(sys.argv) > 4:
    print("Enter two names. Path is optional")
    print("e.g. analysis <name1> <name2> [<path>]")
    sys.exit()

n1 = sys.argv[1]
n2 = sys.argv[2]
if len(sys.argv) == 3:
    path = "../data/NationalNames.csv"
else:
    path = sys.argv[3]

print("running analysis with names and path:")
print(n1)
print(n2)
print(path)
d = filter_two_names(read_csv(path), n1, n2)
for name, series in d.items():
    print(name + " mean: " + str(series.mean()) + " std: " + str(series.std()))

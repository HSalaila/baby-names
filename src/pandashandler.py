import pandas as pd

DEFAULT_PATH = "data/NationalNames.csv"


def read_csv(file=DEFAULT_PATH):
    """"reads a specified csv file
    return pandas.DataFrame."""
    return pd.read_csv(file)


def filter_two_names(df, name1, name2):
    """filters the data frame on the specified names and groups it per year; regardless of gender.
    return dictionary key: <Name> value: pandas.DataFrame"""
    min_index = df["Year"].min()
    max_index = df["Year"].max() + 1

    def filter_name_groupby_year(name):
        return df[df["Name"].isin([name])].groupby(["Year"])["Count"]\
            .sum()\
            .reindex(range(min_index, max_index), fill_value=0)
    return {name1: filter_name_groupby_year(name1), name2: filter_name_groupby_year(name2)}

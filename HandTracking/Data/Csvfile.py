import pandas

pandas.set_option('display.max_rows', None)
datafile = r"a\HandTracking\Data\dataset_20211124-1.csv"
# datafile = r"a\HandTracking\Data\test.csv"


dataframe = pandas.read_csv(datafile, index_col=0)
# print(dataframe)
dataIndex = dataframe.columns.values
print(dataIndex)
Search_word = "逓信省"
# Result_data = dataframe[dataframe[Search_Genre].str.contains(Search_word)]

# print(Result_data)
# print(dataframe.isnull().sum())

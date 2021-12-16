# タイトルの日本語かな表記を追加したい
#
import pandas
from pandas.core.indexes.base import Index
import pykakasi
import numpy as np


# pandas.set_option('display.max_rows', None)
pandas.set_option('display.max_columns', None)
datafile = r"a\HandTracking\Data\dataset_20211130-2.csv"
# datafile = r"a\HandTracking\Data\dataset_20211130-2.csv"
# datafile = r"a\HandTracking\Data\dataset_20211201-1.csv"
# datafile = r'a\HandTracking\Data\dataset_20211216-1.csv'


dataframe = pandas.read_csv(datafile, index_col=0)

# dataframe = dataframe.fillna("No_data")

dataIndex = dataframe.columns.values
Index_Num = 1
Appendfile = []
kks = pykakasi.kakasi()


for i in range(len(dataframe)):
    name = dataframe.iat[i, Index_Num]
    changed_name = kks.convert(name)
    append_name = ""
    for cname in changed_name:
        append_name += cname["kana"]
    print("{0}=>{1}".format(name, changed_name))
    Appendfile.append(append_name)

#     Appendfile.append(kks.convert(list[2]))
print(Appendfile)
dataframe.insert(Index_Num+1, '出版者（ふりがな）', Appendfile)

dataframe = dataframe.reset_index()

dataframe.to_csv('a\HandTracking\Data\dataset_20211216-1.csv')

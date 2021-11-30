# タイトルの日本語かな表記を追加したい
#

from numpy.lib.function_base import append
from numpy.lib.shape_base import apply_over_axes
import pandas
from pandas.core.indexing import check_bool_indexer
import pykakasi

pandas.set_option('display.max_rows', None)
datafile = r"a\HandTracking\Data\dataset_20211124-1.csv"

dataframe = pandas.read_csv(datafile)
dataIndex = dataframe.columns.values
Appendfile = []
kks = pykakasi.kakasi()


for i in range(len(dataframe)):
    name = dataframe.iat[i, 1]
    changed_name = kks.convert(name)
    append_name = ""
    for cname in changed_name:
        append_name += cname["kunrei"]
    # print("{0}=>{1}".format(name, changed_name))
    Appendfile.append(append_name)

#     Appendfile.append(kks.convert(list[2]))
print(Appendfile)
dataframe.insert(2, 'タイトル（ふりがな）', Appendfile)

dataframe.to_csv('a\HandTracking\Data\dataset_20211130-1.csv')

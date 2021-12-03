from numpy.lib.function_base import percentile
import pandas
from pandas.core.frame import DataFrame

Data_File = "a\HandTracking\Data\dataset_20211201-1.csv"

Data_Frame = pandas.read_csv(Data_File)
Data_Index = Data_Frame.columns.values

print(Data_Index)

pandas.set_option('display.max_rows', None)

# 1:URL, 2:タイトル, 3:タイトル（ふりがな）, 4:巻次, 5:シリーズ, 6:版表示, 7:著者, 8:出版者, 9:出版者（ふりがな）, 10:出版年,
# 11:出版年(W3CDTF), 12:ISBN, 13:冊数（ページ数・大きさ）, 14:NDC分類, 15:NDC分類（第８版）, 16:NDC分類（第９版）, 17:NDLC分類,
# 18:件名（NDLSH）, 19:公開範囲


Search_Word = '吾輩は'
Search_Index = 1
Sort_Index=10

# print(Data_Frame.isnull().sum())

# print(Data_Frame[Data_Index[Search_Index]])
# print(Data_Index[Search_Index])


# if Data_Frame[Data_Index[Search_Index] == Search_Word]:
#     print(Data_Frame[Data_Index[Search_Index] == Search_Word])
# else:
#     print("404: Not Found.")
Search_Result = Data_Frame[Data_Frame[Data_Index[Search_Index]].str.contains(Search_Word)]
if not Search_Result.empty:
    # 出力行を限定する
    Search_Result = Search_Result[[Data_Index[1], Data_Index[10]]]
    print(Search_Result.sort_values(Data_Index[Sort_Index]))
else:
    print("[]:Not_found")

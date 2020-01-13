import pandas as pd
import xlsxwriter
import openpyxl

#파일이름 입력 받기
fileDate = input('Type Report Date : ')

#파일 읽기
assetRawFile = 'YouTube_loenent_M_'+fileDate+'_asset_raw_v1-1.csv.gz'
summaryRawFile = 'YouTube_loenent_M_'+fileDate+'_asset_summary_v1-1.csv.gz'

df_summaryRaw = pd.read_csv(summaryRawFile, encoding='utf8')
df_assetRaw = pd.read_csv(assetRawFile, encoding='utf8')

#안쓰는 값 지우기
del df_assetRaw["Adjustment Type"]
del df_assetRaw["Day"]
del df_assetRaw["Asset Labels"]
del df_assetRaw["GRid"]
del df_assetRaw["Administer Publish Rights"]
del df_assetRaw["YouTube Revenue Split : Partner Sold YouTube Served"]
del df_assetRaw["YouTube Revenue Split : Partner Sold Partner Served"]
del df_assetRaw["Partner Revenue : Partner Sold YouTube Served"]
del df_assetRaw["Partner Revenue : Partner Sold Partner Served"]

df_filled = df_assetRaw.fillna('Value_Missing')

df_PT = df_filled.pivot_table(index=['Asset ID','Country','Asset Title','Asset Channel ID','Asset Type','Custom ID','ISRC','UPC'], values=['Owned Views','YouTube Revenue Split : Auction','YouTube Revenue Split : Reserved','YouTube Revenue Split','Partner Revenue : Auction','Partner Revenue : Reserved','Partner Revenue'],aggfunc='sum', fill_value='-')
print(df_PT)

df_Final = df_PT.reset_index()

df_PAGE1 = df_Final[:1000000]
df_PAGE2 = df_Final[1000000:]

writer = pd.ExcelWriter('YT_asset_raw_no_dates_'+fileDate+'.xlsx', engine='xlsxwriter')


df_summaryRaw.to_excel(writer, sheet_name='YT Summary')
df_PAGE1.to_excel(writer, sheet_name='1')
df_PAGE2.to_excel(writer, sheet_name='2')

writer.save()
writer.close()
# Setup ================================================================================================================
# Setting Directory for File Input and Output
import os
os.chdir("C:\\BC0401 - Project\\BC0401-Project")
# print(os.getcwd())

# Read .xlsx using Pandas
import pandas as pd
df = pd.read_excel("stockcards.xlsx")

# Key information of file ==============================================================================================
# print(df.index) #RangeIndex(start=0, stop=56086, step=1)
# print(len(df)) # 56086 rows
# print(df.dtypes)
# Date             datetime64[ns]
# Type                     object
# RefNo                     int64
# SNO                       int64
# Cur                      object
# TUPrice                 float64
# ODAmt                   float64
# Amt                     float64
# Worth                   float64
# Customer Code            object
# StkISN                  float64
# df_temp = df[["TUPrice", "ODAmt", "Amt", "Worth"]]
# print(df_temp.describe())
#              TUPrice          ODAmt            Amt          Worth
# count   55822.000000   55822.000000   55822.000000   55822.000000
# mean       64.361679    1749.795741   -1749.056717   -1465.939653
# std      2878.339602    4949.587200    5031.809780    4657.307719
# min        -0.100000   -1550.000000 -320771.530000 -320772.000000
# 25%         3.200000     220.000000   -1490.285000   -1188.047500
# 50%         4.800000     528.000000    -520.000000    -396.100000
# 75%        17.400000    1519.030000    -217.500000    -154.000000
# max    320771.530000  320771.530000   67360.810000   18420.320000

# print(df.isnull().sum()) # Number of NA values
# Date               0
# Type               0
# RefNo              0
# SNO                0
# Cur              334
# TUPrice          264
# ODAmt            264
# Amt              264
# Worth            264
# Customer Code    546
# StkISN           544
# dtype: int64

# Joining .JSON file ===================================================================================================
cat_class_json = pd.read_json('cat_class.json')
cat_class_json.rename(columns={'StockISN':'StkISN'}, inplace=True)
# print(cat_class_json)
df = pd.merge(df, cat_class_json, on = "StkISN", how="left")
print(df)

# Data Cleaning ========================================================================================================
# KIV---
# Consider removing 'RefNo', 'SNO', 'TUPrice' columns if they are not helpful for analysis.
# Can consider checking if we are incurring a lot of foreign exchange losses as a result of conversion.

# Individual columns---
# 1. "Type"
# print(df["Type"].unique()) # ['ICG', 'ICX']
# print(df["Type"].value_counts())
# ['ICG' 'ICX']
# ICG    51745
# ICX     4341
# Name: Type, dtype: int64
# A : There are 51745 ICG and 4341 ICX transaction types = 56086 total values. Thus, there are 0 NA values and no other values to be ignored.



# Archive ==============================================================================================================
# JSON way ---
# import json
# with open('cat_class.json') as cat_class_json:
#     data = json.load(cat_class_json)
#
# # File has 2 keys, 'StockISN' and 'CatCode'
# for i in data:
#     print(i)

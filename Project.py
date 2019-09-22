# Setup ================================================================================================================
# Setting Directory for File Input and Output
import os
os.chdir("C:\\BC0401 - Project\\BC0401-Project")
# print(os.getcwd())

# Read .xlsx using Pandas
import pandas as pd
df = pd.read_excel("stockcards.xlsx")

# Key information of file
# print(df.index) #RangeIndex(start=0, stop=56086, step=1)
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


# with open("stockcards.xlsx", "r") as stock_cards:
#     for each in stock_cards:
#         print(each)


# JSON
# import json
# with open('cat_class.json') as f:
#     data = json.load(f)
#
# for i in data:
#     print(i['StockISN'], i['CatCode'])
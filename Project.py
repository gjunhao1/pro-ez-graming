# Setup ================================================================================================================
# Setting Directory for File Input and Output
import os
os.chdir("C:\\BC0401 - Project\\BC0401-Project")
# print(os.getcwd())

# Read .xlsx using Pandas
import pandas as pd
df = pd.read_excel("stockcards.xlsx")

# Joining .JSON file ===================================================================================================
cat_class_json = pd.read_json('cat_class.json')
cat_class_json.rename(columns={'StockISN':'StkISN'}, inplace=True)
# print(cat_class_json)
df = pd.merge(df, cat_class_json, on = "StkISN", how="left")
# print(df)

# Key information of file ==============================================================================================
# print(df.index)
    # dtype='int64', length=56086)
# print(len(df))
    # 56086
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
    # CatCode                  object
    # dtype: object

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

    # All columns in the context of price has negative values, as seen from their min.
    # Column "Amt" and "Worth" have 75% of their values as negative, thus inappropriate to drop rows with negative value. Instead, it might be better to clean it by apply absolute function to it.
    # To discover the extent of values with negative values later while cleaning.

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
    # CatCode          544




# Data Cleaning ========================================================================================================
# 1. "Type"
# To check for any other values besides ["ICG", "ICX"]
# print(df["Type"].unique()) # ['ICG', 'ICX']
# print(df["Type"].value_counts())
# ['ICG' 'ICX']
# ICG    51745
# ICX     4341
# Name: Type, dtype: int64
# A : There are 51745 ICG and 4341 ICX transaction types = 56086 total values. Thus, there are 0 NA values and no other values to be ignored.

# 2. "Cur"
# Clean inconsistent format into acceptable values ["S$", "M$", "USD$"]
# print(df["Cur"].unique())
# print(df["Cur"].value_counts())
    # SIN    44738
    # S$      7246
    # US$     2352
    # M$      1300
    # USD       99
    # SGD       12
    # US         5
    # ['US$' 'SIN' 'S$' 'M$' nan 'US' 'SGD' 'USD']
df["Cur"] = df["Cur"].replace(["SIN","SGD"],"S$")
df["Cur"] = df["Cur"].replace(["US$", "USD", "US"],"USD$")
# print(df["Cur"].value_counts())
    # S$      51996
    # USD$     2456
    # M$       1300
    # Tallied successfully with previous data. To account for 334 missing values.
df["Cur"].fillna("S$", inplace = True)
# print(df["Cur"].value_counts())
    # S$      52330
    # USD$     2456
    # M$       1300
    # Tallied with all len(df) = 56086

# 3. "Customer Code"
# Change all NA to CASH
df["Customer Code"].fillna("CASH", inplace=True)
# Change all values to Upper Case, to standardise format, and replace "cash" with "CASH"
df["Customer Code"] = df['Customer Code'].str.upper()
# print(df["Customer Code"].value_counts())
# IJ01       7665
# IT23       6632
# CASH       4864
# IG01       4194
# IT04       3271
#            ...
# SM03          1
# SS29          1
# SZ36          1
# IT06          1
# SZ103         1

# Creating a new column to explicitly reflect customer's geographical location.
df["Country"] = df["Customer Code"].str[0:1]
df["Country"] = df["Country"].map({"A":"Australia","F":"Finland","I":"Indonesia","M":"Malaysia","S":"Singapore","C":"Non-Regular"})
# print(df["Country"].value_counts())
    # Indonesia      46764
    # Non-Regular     4876
    # Malaysia        2315
    # Singapore       2093
    # Australia          9
    # Finland            7
    # Only 56064 total records returned, out of 56086 total records, discrepancy of 22.
df["Country"].fillna("MISSING", inplace=True)
# print(df.loc[df['Country']=="MISSING"].index)
    # Int64Index([50385, 50386, 50387, 50388, 50389, 50390, 50391, 50392, 50393,
    #             50394, 50395, 50396, 50397, 50398, 50399, 50400, 50401, 50402,
    #             50403, 50404, 50405, 50406],
    #            dtype='int64')
# print(df["Customer Code"][50385:50407])
    # 22 discrepancies belong to Customer Code belong to unknown "RB01", thus drop these values instead.
# print(len(df)) #56086 rows
df.drop(df.index[50385:50407], inplace=True)
# print(len(df)) #56064 rows
df.reset_index(inplace=True) # Reset index after dropping rows

# 4. "StkISN"
# print(df.isnull().sum())
    # Remove the 544 NA values as calculated
# print(len(df)) #56064 rows
df.dropna(subset=["StkISN"], inplace=True)
# print(df.isnull().sum())
    # 0 NA values in dataset
# print(len(df)) #55520 rows
df.reset_index(inplace=True) # Reset index after dropping rows

# 5. "Amt" and "Worth"
# df_temp = df[["TUPrice", "ODAmt", "Amt", "Worth"]]
# print(df_temp.describe())
    # As mentioned, about 75% of data is negative. Thus, it might be appropriate to assume that we can clean these column by applying the absolute function instead.
df.Amt = df.Amt.abs()
df.Worth = df.Worth.abs()

# 6. "TUPrice"
# for each in df.TUPrice:
#     if each < 0:
#         print(each)
    # Returned only 1 data consisting negative value
# print(df.loc[df['TUPrice'] < 0]) # [24619]
# print(df.loc[24619, ["TUPrice", "ODAmt", "Amt", "Worth"]])
    # TUPrice    -0.1
    # ODAmt     -45.3
    # Amt        45.3
    # Worth         0
    # Since there are valid values in other columns, we shall not drop this row and instead, absolute the value instead
df.TUPrice = df.TUPrice.abs()

# 7. "ODAmt"
# for each in df.ODAmt:
#     if each < 0:
#         print(each)
    # Returned only 5 data consisting negative values
# print(df.loc[df["ODAmt"] < 0].index) # [11429, 15172, 17645, 24619, 24825]
# print(df.loc[[11429, 15172, 17645, 24619, 24825], ["TUPrice", "ODAmt", "Amt", "Worth"]])
    #        TUPrice   ODAmt     Amt  Worth
    # 11429    310.0 -1550.0  1550.0  930.0
    # 15172    120.0  -240.0   240.0    0.0
    # 17645      3.1  -387.5   387.5  337.0
    # 24619      0.1   -45.3    45.3    0.0
    # 24825      3.6   -28.8    28.8    8.0
    # Since ODAmt are just negative values of Amt, we can assume that these negative values are valid but with incorrect signs. Thus, to apply the absolute function instead.
df.ODAmt = df.ODAmt.abs()

# df_temp = df[["TUPrice", "ODAmt", "Amt", "Worth"]]
# print(df_temp.describe())
    # Minimum value for TUPrice, ODAMT, Amt and Worth >= 0

# 8. Cleaning 0 values
# print((df[["TUPrice", "ODAmt", "Amt","Worth"]]==0).sum())
    # TUPrice    1265
    # ODAmt      1043
    # Amt        1019
    # Worth       445
    # There are many missing values or values with 0 in these 4 columns. It may not be appropriate to drop all missing value data, despite it only being (1265/56064=2.25%) of overall dataset.

# print((df.groupby(["TUPrice", "ODAmt", "Amt", "Worth"]).size()))
    # 373 pairs of 0 values for all 4 columns observed. Drop these rows as there is no way of estimating these values, and are thus meaningless for the purpose of analytics.
# print(len(df)) #55520 rows
zero_values = df[(df["TUPrice"]==0) & (df["ODAmt"]==0) & (df["Amt"]==0) & (df["Worth"]==0)].index
df.drop(zero_values, inplace=True)
# print(len(df)) # 55147 rows
df.reset_index(drop=True) # Reset index after dropping rows




# df.to_csv(r"C:\\Users\\Tony\\Documents\\The Documents\\School\\BC0401 - Programming & Analytics\\Project\\stockcards1.csv")
# Archive ==============================================================================================================
# General Instructions---

# Let's break this project down into 3 stages to better visualise milestones. Some of the stages don't need face to face collaboration (e.g. data cleaning, report), while some might be beneficial (e.g. creating a relevant customer loyalty program, presentation).
#
# Since it is sequential, we need to clear a stage first in order to proceed to the next. Thus, everyone needs to work on each stage collectively by an agreed timeline to ensure the project is moving.
#
# 1. Data Cleaning
# a) Prove that column 'Type' has only "ICX" and "ICG"
# b) Filter column 'Cur' to only " ", USD, S$, M$
# (levels(DT$Cur)
# [1] ""    "M$"  "S$"  "SGD" "SIN" "US"  "US$" "USD")
# c) For column 'Customer Code', change NA values to 'Cash' to prevent misinterpretation for missing values.
# d) Remove NA values for column 'StkISN'
# e) To left join stockscard.csv (left) with cat_class.json (right) on StockISN
# f) Remove irrelevant data that is not within scope of the project
#
# 2. Application
# - Market analytics: Customer buying patterns, geographical distribution of transactions, stocks item analysis
# - Create an appropriate customer loyalty program (regional focus)
# - Create a guide for item stockup
# - Create cmd-line query application to query data, and perform statistical summaries (data up to 5 years)
#
# 3. Report and Presentation
# -  Analysis
# - Coding Structure
# - Design Process
# - Reflection of what we have learnt in this course
# - Programming codes (Appendix)
#
# Right now we are at stage 1 of data cleaning, and we need to prep the data to apply it later. I summarised the project instructions vaguely above. We can put our names into each of the tasks under data cleaning and 分工合作 lor, then we join the code together once we are done with stage 1.


# Data Cleaning ========================================================================================================
# KIV---
# Consider removing 'RefNo', 'SNO', 'TUPrice' columns if they are not helpful for analysis.
# Can consider checking if we are incurring a lot of foreign exchange losses as a result of conversion.

# "Cur" column
# df["Cur"] = df["Cur"].map({"SIN":"S$", "S$":"S$", "US$":"USD$", "M$":"M$", "USD":"USD$", "SGD":"S$", "US":"USD$"})

# "Customer Code" Factor
# Change all to Upper case
# df['Customer Code'] = df['Customer Code'].str.upper()

# df["Country"] = df["Country"].replace([["A"], "Australia"])
# df["Country"] = df["Country"].replace([["F"], "Finland"])
# df["Country"] = df["Country"].replace([["I"], "Indonesia"])
# df["Country"] = df["Country"].replace([["M"], "Malaysia"])
# df["Country"] = df["Country"].replace([["S"], "Singapore"])
# df["Country"] = df["Country"].replace([["C"], "Non-Regular"])
# print(df["Country"].value_counts())


# JSON way ---
# import json
# with open('cat_class.json') as cat_class_json:
#     data = json.load(cat_class_json)
#
# # File has 2 keys, 'StockISN' and 'CatCode'
# for i in data:
#     print(i)

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

# 4. "StkISN"
# print(df.isnull().sum())
    # Remove the 544 NA values as calculated
df.dropna(subset=["StkISN"], inplace=True)
# print(df.isnull().sum())
    # 0 NA values in dataset







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

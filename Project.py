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

# Data Exploration ==============================================================================================
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

    # To resolve missing values by
    # 1. Estimating with central tendency methods (mean, mode)
    # 2. To drop rows containing missing values


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

    # 7 levels of value for categorical variable, inclusive missing data.
    #Replace unacceptable formats to acceptable formats

df["Cur"] = df["Cur"].replace(["SIN","SGD"],"S$")
df["Cur"] = df["Cur"].replace(["US$", "USD", "US"],"USD$")
# print(df["Cur"].value_counts())
    # S$      51996
    # USD$     2456
    # M$       1300
    # Tallied successfully with previous data. To account for the remaining 334 missing values.

df["Cur"].fillna("S$", inplace = True)
# print(df["Cur"].value_counts())
    # S$      52330
    # USD$     2456
    # M$       1300
    # Tallied with total rows of len(df) = 56086

# 3. "Customer Code"
    # Explore the different types of values
# print(df["Customer Code"].value_counts())
    # There are inconsistencies in terms of capitalization.
    # Change all values to Upper Case to standardise format.

df["Customer Code"] = df['Customer Code'].str.upper()
    # Change all NA to CASH
df["Customer Code"].fillna("CASH", inplace=True)

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
    # 22 discrepancies belong to Customer Code belong to unknown "RB01", thus drop these values as there are no ways to estimate or replace this value.
# print(len(df)) #56086 rows
df.drop(df.index[50385:50407], inplace=True)
# print(len(df)) #56064 rows
df.reset_index(drop=True) # Resetting index to ensure index is a running sequence.

# 4. "StkISN"
# print(df.isnull().sum())
    # NA values in multiple attributes
# print(len(df)) #56064 rows
df.dropna(subset=["StkISN"], inplace=True)
# print(df.isnull().sum())
    # 0 NA values remaining in dataset
# print(len(df)) # 55520 rows remiaining in dataset after dropping rows.
df.reset_index(drop=True) # Resetting index to ensure index is a running sequence.

# 5. "TUPrice", "ODAmt", "Amt", "Worth"
    # Cleaning 0 values
# print((df[["TUPrice", "ODAmt", "Amt","Worth"]]==0).sum())
    # TUPrice    1265
    # ODAmt      1043
    # Amt        1019
    # Worth       445
    # There are many missing values or with value '0' in these 4 columns. It may not be appropriate to drop all rows and assume it as missing values, despite it is representing only (1265/56064=2.25%) of overall dataset.

# print((df.groupby(["TUPrice", "ODAmt", "Amt", "Worth"]).size()))
    # The first row shows 373 pairs of 0 values for all 4 columns observed. To drop these rows as there is no possible way of estimating these values via referencing, and are thus meaningless for the purpose of analytics.
# print(len(df)) # 55520 rows
zero_values = df[(df["TUPrice"]==0) & (df["ODAmt"]==0) & (df["Amt"]==0) & (df["Worth"]==0)].index
df.drop(zero_values, inplace=True)
# print(len(df)) # 55147 rows
df.reset_index(drop=True) # Resetting index to ensure index is a running sequence.

    # Detecting outliers
import matplotlib.pyplot as plt
# plt.scatter(x=df.index, y=df.ODAmt)
# plt.scatter(x=df.index, y=df.Amt)
# plt.scatter(x=df.index, y=df.Worth)
# plt.scatter(x=df.index, y=df.TUPrice)

    # Observed visually that there are many overlapping outliers near the vertical slice where index is close to 20000.
    # Thus, to attempt to further explore these outliers.

    # Finding outliers
import numpy as np
import pandas as pd

outliers = []

def detect_outlier(col):
    threshold = 3
    mean_1 = np.mean(col)
    std_1 = np.std(col)

    for y in col:
        z_score = (y - mean_1) / std_1
        if np.abs(z_score) > threshold:
            outliers.append(y)
            # print(outliers)
    return pd.DataFrame({'TUPrice': outliers})

outlier_df = detect_outlier(df.TUPrice)
    # Create a dataframe containing all outliers of TUPrice with z-values more than 3.
    # Total of 12 outliers above the z-value of 3 for column "TUPrice". From empirical rule, these data exceeds the 99.7% of the confidence interval range, assuming TUPrice follows normal distribution.
    # Hence, we should drop these outliers for the purpose of more meaningful, and less skewed analysis.

df.reset_index(inplace=True)
df['index'] = np.arange(len(df))
temp_df = df[['index','TUPrice']]
temp1_df = pd.merge(outlier_df, temp_df, on = "TUPrice", how="left")
# print(temp1_df)
    # Find the index for the outliers captured in previous dataframe.

# print(len(df)) # 55147 rows
list1 = temp1_df["index"].tolist()
df.drop(index=list1, inplace=True)
# print(len(df)) # 55135 rows
df.reset_index(drop=True)
    # Dropped a total of 12 rows, from the original 55147 rows to 55135 rows.
    # Resetting index to ensure index is a running sequence.
# plt.scatter(x=df.index, y=df.TUPrice)
    # Dataset is corrected as TUPric spans to approximately 5000 only.


# 6. "TUPrice"
# for each in df.TUPrice:
#     if each < 0:
#         print("The negative value is ", each)
    # Returned only 1 data consisting negative value
# print(df.loc[df['TUPrice'] < 0]) # [24439]
# print(df.loc[24439, ["TUPrice", "ODAmt", "Amt", "Worth", "StkISN"]])
    # TUPrice - 0.1
    # ODAmt - 45.3
    # Amt - 45.3
    # Worth - 0
    # StkISN - 10445

    # There is only 1 negative value under "TUPrice".
    # Since there are appropriate values in other rows, we should not drop this row, but instead estimate the TUPrice with its StkISN by means of averaging.
# print("The mean of StkISN = 10445 is: ", df.TUPrice[df['StkISN'] == 10445].mean())
df["TUPrice"] = df["TUPrice"].replace([-0.1, 1.35])
# print(df.loc[24439, ["TUPrice", "ODAmt", "Amt", "Worth", "StkISN"]])
# Wrong replacement

# 8. "ODAmt"
    # Locating negative values
# for each in df.ODAmt:
#     if each < 0:
#         print(each)
    # Returned only 5 data consisting negative values
od_negative = df.loc[df["ODAmt"] < 0].index
# print(df.loc[od_negative, ["TUPrice", "ODAmt", "Amt", "Worth"]])
    #        TUPrice   ODAmt     Amt  Worth
    # 11429    310.0 -1550.0  1550.0  930.0
    # 15172    120.0  -240.0   240.0    0.0
    # 17645      3.1  -387.5   387.5  337.0
    # 24619      0.1   -45.3    45.3    0.0
    # 24825      3.6   -28.8    28.8    8.0
    # Since we can observe that ODAmt are the exact values but only with negative signs as compared to Amt, we should be able to assume that these negative values are valid but with erroneously entered with incorrect signs.  Thus, to apply the absolute function instead.
df.ODAmt = df.ODAmt.abs()
# print(df.loc[od_negative, ["TUPrice", "ODAmt", "Amt", "Worth"]])
    #        TUPrice   ODAmt     Amt  Worth
    # 11390    310.0  1550.0  1550.0  930.0
    # 15107    120.0   240.0   240.0    0.0
    # 17579      3.1   387.5   387.5  337.0
    # 24515      3.4    45.3    45.3    0.0
    # 24721      3.6    28.8    28.8    8.0

    # ODAmt have 0 remaining negative values.

    # Cleaning zero values
# print("There are a total of", df.ODAmt[(df.ODAmt==df.Amt) & (df.Cur=="S$")].count(), "rows of data when ODAmt = Amt when Currency is S$.")
    # There is a significant amount of data (51413 rows) to show that when Currency = "S$", ODAmt can be estimated with Amt.
    # Thus, we should replace the zero values in ODAmt with values of Amt.
pd.options.mode.chained_assignment = None
print(df.ODAmt[(df.ODAmt==0) & (df.Cur=="S$")].count()) # 669 rows
df.ODAmt[(df.ODAmt==0) & (df.Cur=="S$")] = df.Amt
print(df.ODAmt[(df.ODAmt==0) & (df.Cur=="S$")].count()) # 645 rows
pd.options.mode.chained_assignment = 'warn'
# To find a way to skip the warning. --> https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas

# 8. "Amt" and "Worth"
    # Locating negative values
# df_temp = df[["TUPrice", "ODAmt", "Amt", "Worth"]]
# print(df_temp.describe())
# plt.plot(df.Amt)
    # As mentioned, about 75% of data is negative for both "Amt" and "Worth" column. Hence,
    # Dropping the rows is not an option, as this will greatly reduce our dataset.
    # It might thus be appropriate to assume that we can clean these column by applying the absolute function instead, as most of the data appears to have been recorded with a negative sign.

    # Applying the absolute function
df.Amt = df.Amt.abs()
df.Worth = df.Worth.abs()
# plt.plot(df.Amt)
    # Column "Amt" and "Worth" are standardized to positive signs for analytics purposes.










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

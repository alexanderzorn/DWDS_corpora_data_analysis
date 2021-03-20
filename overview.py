# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.7.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import requests, pandas as pd
from io import StringIO
    
limit = 5000
p =1
data_input = pd.DataFrame()
    
while(True):
    print("Scraping one page")
    url = f"https://www.dwds.de/r/?format=kwic&limit={limit}&view=csv&output=inline&q=dem+Präsidenten&corpus=zeit&date-start=1946&date-end=2018&sort=date_desc&p={p}"
    r = requests.get(url)
    new_df = pd.read_csv(StringIO(r.text.replace(";"," ").replace("\",\"",";").replace("\"","")), delimiter=";")
    print(f"Found {new_df.shape[0]} entries")
    if new_df.shape[0] == 0:
        break
    data_input = pd.concat([data_input, new_df])
    p+=1
    if new_df.shape[0] < limit:
        break
data_input["Date"] = pd.to_datetime(data_input["Date"], format='%Y-%m-%d')

# %%
print(f"Before: {data_input.shape[0]}")
data_input = data_input.drop_duplicates()
print(f"After: {data_input.shape[0]}")



data_input["Year"] = data_input["Date"].apply(lambda x: x.year)
data_input["Month"] = data_input["Date"].apply(lambda x: x.month)
year_overview = pd.DataFrame([], columns=["Nr_articles"])
for year in data_input.groupby("Year"):
    year_overview.loc[year[0]] = year[1].shape[0]
year_overview.plot(figsize=(15,10))

# %%

'''
dem+Präsidenten
'''
data_input["Hit"].unique()

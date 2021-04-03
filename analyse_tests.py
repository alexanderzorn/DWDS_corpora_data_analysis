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
import os, pandas as pd

def get_lexem_overview():
    #Get test ratios
    #complete_table = pd.DataFrame()
    ratios = {}
    for lexem_foldername in os.listdir("Result"):
        if lexem_foldername == ".DS_Store":
            continue
        ratios[lexem_foldername] = {}
        ratios[lexem_foldername]["Total"] = 0
        for variante_filename in os.listdir("Result/"+lexem_foldername):
            if "overview" in variante_filename:
                continue
            variante_pd = pd.read_csv("Result/"+lexem_foldername + "/" + variante_filename)
            variante_size = variante_pd.shape[0]
            if variante_size == 1: 
                variante_size = 0
            ratios[lexem_foldername][variante_filename] = {"Total": variante_size, "Done_tests" : 0, "Hit" : 0, "Hit_rel": 1}
            ratios[lexem_foldername]["Total"] += variante_size


    return ratios

# %%
#go through all test result files
tests = pd.DataFrame()
ratios = get_lexem_overview()
for file in os.listdir("Tests_done"):
    if file == ".DS_Store":
        continue
    print(file)
    new_file = pd.read_csv("Tests_done/"+file, delimiter=";")
    tests = pd.concat([tests,new_file])


for idx, row in tests.iterrows():
    if row["Test"] in [0,1]:
        ratios[row["Lexem"]][row["Lexem Variante"]]["Done_tests"] +=1
        if row["Test"] == 1:
            ratios[row["Lexem"]][row["Lexem Variante"]]["Hit"] +=1
    else:
        print("Entry not in 0,1 stoping")
        #print(row)
        print("huhu")
    
        
for lexem in ratios.keys():
    for variante in ratios[lexem].keys():
        if variante == "Total":
            continue
        done_tests = float(ratios[lexem][variante]["Done_tests"])
        hits = float(ratios[lexem][variante]["Hit"])
        if(done_tests == 0):
            print(variante)
            continue
        ratios[lexem][variante]["Hit_rel"] = hits/done_tests

result = pd.DataFrame()
for lexem in ratios.keys():
    for variante in ratios[lexem].keys():
        if variante == "Total":
            continue
        row = pd.Series(ratios[lexem][variante])
        row["Hit_rel (%)"] = round(row["Hit_rel"]*100,2)
        row["reduced total"] = round(row["Total"]*row["Hit_rel"],2)
        if row["Total"] == 0:
            row["Tested ratio (%)"] = 100
        else:
            row["Tested ratio (%)"] = round(row["Done_tests"]/row["Total"]*100,2)
        result[variante] = row.drop("Hit_rel")
result.transpose().to_csv("Test_results.csv")

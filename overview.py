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

# %%
import requests,os, pandas as pd
from io import StringIO
import time
import itertools
from tqdm import tqdm
import random
import math
from copy import deepcopy as dc
def get_and_save(fall,pronomen, substant, foldername):
    limit = 5000
    p =1
    data_input = pd.DataFrame()
    search_word = f"%40{pronomen}+%232+%40{substant}" 
    last_found = 0
    while(True):
        url = f"https://www.dwds.de/r/?format=kwic&limit={limit}&view=csv&output=inline&q={search_word}&corpus=zeit&date-start=1946&date-end=2018&sort=date_desc&p={p}"
        r = requests.get(url)
        new_df = pd.read_csv(StringIO(r.text.replace(";"," ").replace("\",\"",";").replace("\"","")), delimiter=";")
        #if :
        if "Date" not in new_df.columns or(new_df.shape[0] == 0 or (new_df.shape[0] < limit and last_found == new_df.shape[0])):
            break
        data_input = pd.concat([data_input, new_df], sort=False).drop_duplicates()
        p+=1
        
        last_found = new_df.shape[0]
        time.sleep(3+random.randint(0, 5))
    data_input["Date"] = pd.to_datetime(data_input["Date"], format='%Y-%m-%d')
    if not os.path.isdir(foldername):
        os.mkdir(foldername)
    outputname = foldername+"/"+pronomen+substant+".csv"
    data_input.to_csv(outputname)


    overview_filename = foldername + "/"+foldername+"_overview.csv"
    new_row_dict = {"Lexem": foldername, "Fall":fall,"Suchwort clean":pronomen+" "+substant, "Suchwort":search_word, "Filename": outputname, "Anzahl treffer":data_input.shape[0]}
    if os.path.isfile(overview_filename):
        df = pd.read_csv(overview_filename)
        pd_dict = pd.Series(new_row_dict).to_frame().T
        model_df = df.append(pd_dict.iloc[0])
    else:
        model_df = pd.Series(new_row_dict).to_frame().T
    model_df.to_csv(overview_filename, index=False)
    return data_input

def go_through_one_lexem(lexem, lexem_formen):
    pronouns = {"Genitiv": ["des", "eines"], "Dativ": ["dem", "einem"], "Akkusativ": ["den", "einen"]}
    for fall in lexem_formen.keys():
        lexemen = lexem_formen[fall]
        pronoun = pronouns[fall]
        combs = [list(zip(x,lexemen)) for x in itertools.permutations(pronoun,len(lexemen))]
        for comb in combs[0]+combs[1]:
            get_and_save(fall,comb[0], comb[1], lexem)


# %%
#Lexeme zum Durchgehen:
lexeme = {}

#Typ I:
lexeme["Kollege"]    = {"Genitiv": ["Kollegen"],            "Dativ": ["Kollege", "Kollegen"],        "Akkusativ": ["Kollege", "Kollegen"]}
lexeme["Mensch"]     = {"Genitiv": ["Menschen"],            "Dativ": ["Mensch", "Menschen"],         "Akkusativ": ["Mensch", "Menschen"]}
lexeme["Prinz"]      = {"Genitiv": ["Prinzen"],             "Dativ": ["Prinz", "Prinzen"],           "Akkusativ": ["Prinz", "Prinzen"]}
lexeme["Experte"]    = {"Genitiv": ["Experten"],            "Dativ": ["Experte", "Experten"],        "Akkusativ": ["Experte", "Experten"]}
lexeme["Held"]       = {"Genitiv": ["Helden"],              "Dativ": ["Held", "Helden"],             "Akkusativ": ["Held", "Helden"]}
#Typ II:
lexeme["Präsident"]  = {"Genitiv": ["Präsidenten"],         "Dativ": ["Präsident", "Präsidenten"],   "Akkusativ": ["Präsident", "Präsidenten"]}
lexeme["Journalist"] = {"Genitiv": ["Journalisten"],        "Dativ": ["Journalist", "Journalisten"], "Akkusativ": ["Journalist", "Journalisten"]}
lexeme["Soldat"]     = {"Genitiv": ["Soldaten"],            "Dativ": ["Soldat", "Soldaten"],         "Akkusativ": ["Soldat", "Soldaten"]}
lexeme["Patient"]    = {"Genitiv": ["Patienten"],           "Dativ": ["Patient", "Patienten"],       "Akkusativ": ["Patient", "Patienten"]}
lexeme["Nachbar"]    = {"Genitiv": ["Nachbars","Nachbarn"], "Dativ": ["Nachbar", "Nachbarn"],        "Akkusativ": ["Nachbar", "Nachbarn"]}

#for lexem in tqdm(lexeme.keys()):
#    go_through_one_lexem(lexem, lexeme[lexem])


https://www.dwds.de/r/?format=kwic&limit=100&view=csv&output=inline&
    q=dem+Präsident&corpus=zeit&date-start=1946&date-end=2018&sort=date_desc&seed=





# %%
#INSPECT result and provide test tables
complete_table = pd.DataFrame()
overview_number_entries = {}
for lexem_foldername in os.listdir("Result"):
    if lexem_foldername == ".DS_Store":
        continue
    overview_number_entries[lexem_foldername] = {}
    overview_number_entries[lexem_foldername]["Total"] = 0
    for variante_filename in os.listdir("Result/"+lexem_foldername):
        if "overview" in variante_filename:
            continue
        variante_pd = pd.read_csv("Result/"+lexem_foldername + "/" + variante_filename)
        variante_size = variante_pd.shape[0]
        if variante_size == 1: 
            variante_size = 0
        overview_number_entries[lexem_foldername][variante_filename] = variante_size
        overview_number_entries[lexem_foldername]["Total"] += variante_size
        variante_pd["Lexem"] = lexem_foldername
        variante_pd["Lexem Variante"] = variante_filename
        if variante_size >0:
            complete_table = pd.concat([complete_table, variante_pd])
varianten_group = complete_table.groupby("Lexem Variante")
lexem_group = complete_table.groupby("Lexem")

# %%
overview_number_entries


# %%
#Add another test file
def create_new_test_file(complete_table, overview_number_entries):

    #get on percent (aufgerundet) overall bis auf die die bereits vorhanden sind 
    number_already_tested = {}
    for key in overview_number_entries.keys():
        number_already_tested[key] = {}
        for key_ in overview_number_entries[key].keys():
            number_already_tested[key][key_] = 0


    #collect all already done tests
    def get_all_tests():
        test_pd  = pd.DataFrame()
        nr_files = 0
        for test_filename in os.listdir("Tests"):
            if test_filename == ".DS_Store":
                continue
            nr_files +=1
            variante_pd = pd.read_csv("Tests/"+test_filename)
            variante_size = variante_pd.shape[0]
            test_pd = pd.concat([test_pd, variante_pd])
        return test_pd, nr_files
    all_tested_cases, nr_test_files = get_all_tests()
    all_tested_cases_w_o_result = all_tested_cases
    #print(all_tested_cases_w_o_result)
    if all_tested_cases.shape[0] >0:
        all_tested_cases_w_o_result = all_tested_cases.drop("Test", axis=1)


    
    #create new test file with .5% rounded up 
    test_share_per_file = .1
    new_test_pd = pd.DataFrame()
    for lexem in tqdm(overview_number_entries.keys()):
        for lexem_variante in overview_number_entries[lexem].keys():
            total_nr_entr = overview_number_entries[lexem][lexem_variante]
            nr_entries_wanted = math.ceil(total_nr_entr*test_share_per_file)
            if nr_entries_wanted == 0 or lexem_variante == "Total":
                continue
            variante_dp_copy = dc(complete_table[complete_table["Lexem Variante"] == lexem_variante])
            if all_tested_cases_w_o_result.shape[0] >0:
                cols = variante_dp_copy.columns
                variante_dp_copy['key1'],all_tested_cases_w_o_result['key2'] = 1,1
                non_tested_variante = pd.merge(variante_dp_copy, all_tested_cases_w_o_result, on=list(cols), how = 'left')
                non_tested_variante = non_tested_variante[~(non_tested_variante.key2 == non_tested_variante.key1)]
                non_tested_variante = non_tested_variante.drop(['key1','key2'], axis=1)
            else:
                non_tested_variante = variante_dp_copy
            nr_already_tested = total_nr_entr - non_tested_variante.shape[0]
            if non_tested_variante.shape[0] == 0 or (nr_already_tested>= .1*total_nr_entr and nr_already_tested>= 100):
                continue
            if non_tested_variante.shape[0] >= nr_entries_wanted:
                new_test_pd = pd.concat([new_test_pd, non_tested_variante.sample(n=nr_entries_wanted)])
            else: 
                new_test_pd = pd.concat([new_test_pd, non_tested_variante])
    new_test_pd["Test"] = 1
    new_test_pd.to_csv("Tests/testset_"+str(nr_test_files+1)+".csv", index=False)

for _ in range(15):
    create_new_test_file(complete_table.drop('Unnamed: 0', axis=1), overview_number_entries)

# %%
#Grossbuchstaben Tabelle:
found_substantiv_table = pd.DataFrame()
nr = 0
for idx, entry in tqdm(complete_table.iterrows()):
    nr+=1
    #if nr > 5000:
    #    break
    #TODO nicht so schön
    variante = entry["Lexem Variante"].replace(".csv","").replace(entry["Hit"],"")
    if entry["Lexem Variante"] == "denPräsidenten.csv":
        variante = "Präsidenten"
    if entry["Lexem Variante"] == "denPräsident.csv":
        variante = "Präsident"
    if entry["Lexem Variante"] == "desBundesligisten.csv":
        variante = "Bundesligisten"
    words = entry["ContextAfter"].replace("   ", " ").replace("  ", " ")
    if words[0] == " ":
        words = words[1:len(words)]
    words = words.split(" ")
    nr_words = len(words)
    found_idx = 0 if words[0] == variante else (1 if nr_words >=2 and words[1] == variante else (2 if nr_words >=3 and words[2] == variante else -1))
    words = words[0:found_idx]
    substantiv_found = False
    for word in words:
        #check if first charakter ist gross
        if word != "" and word[0].isupper():
            substantiv_found = True
    if substantiv_found:
        found_substantiv_table = found_substantiv_table.append(entry)

print(f"Nr entries with extra substantiv found {found_substantiv_table.shape[0]}")
found_substantiv_table.to_csv("substantiv_cases.csv")
found_substantiv_table

# %%
#todo nur noch mit den gespeicherten Dateien arbeiten.
print(f"Before: {data_input.shape[0]}")
data_input = data_input.drop_duplicates()
print(f"After: {data_input.shape[0]}")



data_input["Year"] = data_input["Date"].apply(lambda x: x.year)
data_input["Month"] = data_input["Date"].apply(lambda x: x.month)
year_overview = pd.DataFrame([], columns=["Nr_articles"])
for year in data_input.groupby("Year"):
    year_overview.loc[year[0]] = year[1].shape[0]
year_overview.plot(figsize=(15,10))
plt.show()

# %%

'''
dem+Präsidenten
'''
data_input["Hit"].unique()

# %%
data_input

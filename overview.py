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
import requests,os, pandas as pd
from io import StringIO
import time
import itertools
from tqdm import tqdm
import random 
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

#PROTOTYP I
lexeme["Kollege"]      = {"Genitiv": ["Kolleges","Kollegen"],            "Dativ": ["Kollege", "Kollegen"],            "Akkusativ": ["Kollege", "Kollegen"]}
lexeme["Mensch"]       = {"Genitiv": ["Menschs","Menschen"],             "Dativ": ["Mensch", "Menschen"],             "Akkusativ": ["Mensch", "Menschen"]}
lexeme["Pilot"]        = {"Genitiv": ["Pilots","Piloten"],               "Dativ": ["Pilot", "Piloten"],               "Akkusativ": ["Pilot", "Piloten"]}
lexeme["Nachbar"]      = {"Genitiv": ["Nachbars","Nachbarn"],            "Dativ": ["Nachbar", "Nachbarn"],            "Akkusativ": ["Nachbar", "Nachbarn"]}
lexeme["Prinz"]        = {"Genitiv": ["Prinz","Prinzen"],                "Dativ": ["Prinz", "Prinzen"],               "Akkusativ": ["Prinz", "Prinzen"]}
lexeme["Experte"]      = {"Genitiv": ["Expertes","Experten"],            "Dativ": ["Experte", "Experten"],            "Akkusativ": ["Experte", "Experten"]}
lexeme["Rivale"]       = {"Genitiv": ["Rivales","Rivalen"],              "Dativ": ["Rivale", "Rivalen"],              "Akkusativ": ["Rivale", "Rivalen"]}
lexeme["Wille"]        = {"Genitiv": ["Willes","Willen"],                "Dativ": ["Wille", "Willen"],                "Akkusativ": ["Wille", "Willen"]}
lexeme["Gedanke"]      = {"Genitiv": ["Gedankes","Gedanken"],            "Dativ": ["Gedanke", "Gedanken"],            "Akkusativ": ["Gedanke", "Gedanken"]}
lexeme["Glaube"]       = {"Genitiv": ["Glaubes","Glauben"],              "Dativ": ["Glaube", "Glauben"],              "Akkusativ": ["Glaube", "Glauben"]}
#Prototyp II:
lexeme["Präsident"]    = {"Genitiv": ["Präsidents","Präsidenten"],       "Dativ": ["Präsident", "Präsidenten"],       "Akkusativ": ["Präsident", "Präsidenten"]}
lexeme["Journalist"]   = {"Genitiv": ["Journalists","Journalisten"],     "Dativ": ["Journalist", "Journalisten"],     "Akkusativ": ["Journalist", "Journalisten"]}
lexeme["Bundesligist"] = {"Genitiv": ["Bundesligists","Bundesligisten"], "Dativ": ["Bundesligist", "Bundesligisten"], "Akkusativ": ["Bundesligist", "Bundesligisten"]}
lexeme["Soldat"]       = {"Genitiv": ["Soldats","Soldaten"],             "Dativ": ["Soldat", "Soldaten"],             "Akkusativ": ["Soldat", "Soldaten"]}
lexeme["Diplomat"]     = {"Genitiv": ["Diplomats","Diplomaten"],         "Dativ": ["Diplomat", "Diplomaten"],         "Akkusativ": ["Diplomat", "Diplomaten"]}
lexeme["Patient"]      = {"Genitiv": ["Patients","Patienten"],           "Dativ": ["Patient", "Patienten"],           "Akkusativ": ["Patient", "Patienten"]}
lexeme["Konkurrent"]   = {"Genitiv": ["Konkurrents","Konkurrenten"],     "Dativ": ["Konkurrent", "Konkurrenten"],     "Akkusativ": ["Konkurrent", "Konkurrenten"]}


#for lexem in tqdm(lexeme.keys()):
#    go_through_one_lexem(lexem, lexeme[lexem])




# %%
#INSPECT result and provide test tables
complete_table = pd.DataFrame()
overview
for lexem_foldername in os.listdir("Result"):
    if lexem_foldername == ".DS_Store":
        continue
    for variante_filename in os.listdir(lexem_foldername)

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

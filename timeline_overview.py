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
import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime

def get_all_found_entries():
    output_df = pd.DataFrame()
    for lexem_foldername in os.listdir("Result"):
        if lexem_foldername == ".DS_Store":
            continue
        
        for variante_filename in os.listdir("Result/"+lexem_foldername):
            if "overview" in variante_filename:
                continue
            variante_pd = pd.read_csv("Result/"+lexem_foldername + "/" + variante_filename)
            variante_pd["Lexem Variante"] = variante_filename
            variante_pd["Lexem"] = lexem_foldername
            output_df = pd.concat([output_df, variante_pd])
    return output_df


def add_date_cols(df):
    df['Date']= pd.to_datetime(df['Date'])
    df['Month'], df['Year'] = df['Date'], df['Date']
    df['Month'] = df['Month'].apply(lambda s: datetime.date(s.year, s.month, 1))
    df['Year'] = df['Year'].apply(lambda s: datetime.date(s.year, 1, 1))


# %%
all_entries = get_all_found_entries()
add_date_cols(all_entries)

# %%
all_entries

# %%
nr_entries_per_day = pd.DataFrame()
for group in all_entries.groupby("Year"):
    nr_entries_per_day[group[0]] = [group[1].shape[0]]
nr_entries_per_day= nr_entries_per_day.transpose()

# %%
#compare two lexem variants
test_results = pd.read_csv("Test_results.csv")
compare_1 = ["denMensch.csv"]
compare_2 = ["denMenschen.csv"]

compare_2=["desKollegen.csv","demKollegen.csv","denKollegen.csv","desMenschen.csv","demMenschen.csv","denMenschen.csv","desPrinzen.csv","demPrinzen.csv","denPrinzen.csv","desExperten.csv","demExperten.csv","denExperten.csv","desHelden.csv","demHelden.csv","denHelden.csv","desPräsidenten.csv","demPräsidenten.csv","denPräsidenten.csv","desJournalisten.csv","demJournalisten.csv","denJournalisten.csv","desSoldaten.csv","demSoldaten.csv","denSoldaten.csv","desPatienten.csv","demPatienten.csv","denPatienten.csv","desNachbarn.csv","demNachbarn.csv","denNachbarn.csv"]
compare_1=["demKollege.csv","denKollege.csv","demMensch.csv","denMensch.csv","demPrinz.csv","denPrinz.csv","demExperte.csv","denExperte.csv","demHeld.csv","denHeld.csv","demPräsident.csv","denPräsident.csv","demJournalist.csv","denJournalist.csv","demSoldat.csv","denSoldat.csv","demPatient.csv","denPatient.csv","desNachbars.csv","demNachbar.csv","denNachbar.csv"]             
compare_lexems = pd.DataFrame()
for group in all_entries.groupby("Year"):
    comp_1_sum, comp_2_sum = 0,0
    for var_group in group[1].groupby("Lexem Variante"):
        mult = test_results[test_results['Unnamed: 0'] == var_group[0]].iloc[0]['Hit_rel (%)']/100
        comp_1_sum += (var_group[1].shape[0] if var_group[0] in compare_1 else 0)*mult
        comp_2_sum += (var_group[1].shape[0] if var_group[0] in compare_2 else 0)*mult
    new_entry = pd.Series([comp_1_sum, comp_2_sum], index = ["Stark", "Schwach"])#[str(compare_1), str(compare_2)]) ["den Mensch", "den Menschen"])#
    compare_lexems[group[0]] = new_entry
compare_lexems= compare_lexems.transpose()


# %%
compare_lexems.plot(figsize=(15,10))
plt.title("Zeitlicher Vergleich von starken und schwachen Formen aller untersuchten Lexeme")
plt.xlabel("Jahr")
plt.ylabel("Geschätzte Anzahl Treffer")
plt.savefig("Gesamt_stark_schwach_Vergleich.png" , dpi=300)
plt.show()

# %%
test_results = pd.read_csv("Test_results.csv")
test_results.columns

# %%
nr_entries_per_day.plot(figsize = (15,10), title="Zeitlicher Verlauf ")
plt.show()


# %% [markdown]
# # Übersicht Hit rate

# %%
def get_all_test_entries():
    output_df = pd.DataFrame()
    for lexem_filename in os.listdir("Tests_done"):
        if lexem_filename == ".DS_Store":
            continue
        variante_pd = pd.read_csv("Tests_done/"+lexem_filename, delimiter=";")
        output_df = pd.concat([output_df, variante_pd])
    return output_df


# %%
all_tests = get_all_test_entries()
add_date_cols(all_tests)

# %%
#tests per year
nr_tests_per_year = pd.DataFrame()
hit_share_per_year = pd.DataFrame()
for group in all_tests.groupby("Year"):
    #nr tests per year
    nr_tests_per_year[group[0]] = [group[1].shape[0]]
    #hit share per year
    hit_share_per_year[group[0]] = [100*group[1][group[1]["Test"] == 1].shape[0]/group[1].shape[0]]

nr_tests_per_year= nr_tests_per_year.transpose()
nr_tests_per_year.plot(figsize=(15,10))
plt.show()


hit_share_per_year= hit_share_per_year.transpose()
hit_share_per_year.plot(figsize=(15,10))
plt.ylim([0,100])
plt.xlabel("Jahr")
plt.ylabel("Anteil akzeptierter Treffer (%)")
plt.title("Zeitlicher Verlauf der akzeptierten Treffer")
plt.savefig("Zeitlicher_Verlauf_der_akzeptierten_Treffer.png", dpi=300)
plt.show()

# %%
#complete overview over all filetered findings over time
test_results = pd.read_csv("Test_results.csv")

#compare_2=["desKollegen.csv","demKollegen.csv","denKollegen.csv","desMenschen.csv","demMenschen.csv","denMenschen.csv","desPrinzen.csv","demPrinzen.csv","denPrinzen.csv","desExperten.csv","demExperten.csv","denExperten.csv","desHelden.csv","demHelden.csv","denHelden.csv","desPräsidenten.csv","demPräsidenten.csv","denPräsidenten.csv","desJournalisten.csv","demJournalisten.csv","denJournalisten.csv","desSoldaten.csv","demSoldaten.csv","denSoldaten.csv","desPatienten.csv","demPatienten.csv","denPatienten.csv","desNachbarn.csv","demNachbarn.csv","denNachbarn.csv"]
#compare_1=["demKollege.csv","denKollege.csv","demMensch.csv","denMensch.csv","demPrinz.csv","denPrinz.csv","demExperte.csv","denExperte.csv","demHeld.csv","denHeld.csv","demPräsident.csv","denPräsident.csv","demJournalist.csv","denJournalist.csv","demSoldat.csv","denSoldat.csv","demPatient.csv","denPatient.csv","desNachbars.csv","demNachbar.csv","denNachbar.csv"]             
all_lexems = pd.DataFrame()
for group in all_entries.groupby("Year"):
    comp_1_sum = 0
    for var_group in group[1].groupby("Lexem Variante"):
        mult = test_results[test_results['Unnamed: 0'] == var_group[0]].iloc[0]['Hit_rel (%)']/100
        comp_1_sum += var_group[1].shape[0]*mult
    new_entry = pd.Series([comp_1_sum], index = ["Alle Lexeme"])
    all_lexems[group[0]] = new_entry
all_lexems= all_lexems.transpose()

all_lexems.plot(figsize=(15,10))
plt.title("Zeitlicher Verlauf der geschätzten Vorkommnisse aller untersuchten Lexeme")
plt.xlabel("Jahr")
plt.ylabel("Geschätzte Anzahl Treffer")
plt.savefig("Zeitlicher_Verlauf_aller_Lexeme.png" , dpi=300)
plt.show()
all_lexems.sum()

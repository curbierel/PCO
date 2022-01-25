import sqlite3
import pandas as pd
import spacy
def TsMesLivresNLP(base,table):
    connecteur=sqlite3.connect(base)
    df=pd.read_sql_query("SELECT titre FROM bedetheque",connecteur)
    connecteur.close()
    nlp=spacy.load('fr_core_news_md')
    nlp.Defaults.stop_words.add("tome")
    df['titre']=df['titre'].apply(lambda x:nlp(x))
    df['titre']=df['titre'].apply(pasStop)
    return  df['titre']

def pasStop(words):
    tmp=" ".join(str(token) for token in words if  not(token.is_stop) )
    return tmp

#import
import numpy as np
import random
import pandas as pd
import urllib.request, json 
import gensim
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import KeyedVectors
import gc



def tags_to_vec(list_words, embeddings, dim=300):
 
    # we break the string into words
    nb_words = 0
    somme = np.zeros((300,))
    for i in range(len(list_words)):
        word= list_words[i]
        if word in embeddings:
            somme += embeddings[word ]
            nb_words +=1 
    
    if nb_words==0:
        nb_words=1
        
    return somme/nb_words

def resemblance_embed(list_tag1, list_tag2, embeddings):
    

    list_tag1_emb= tags_to_vec(list_tag1, embeddings, dim=300).reshape(1,-1)
    list_tag2_emb= tags_to_vec(list_tag2, embeddings, dim=300).reshape(1,-1)
    
    
    distances = cosine_similarity(list_tag1_emb ,list_tag2_emb , dense_output=True)
    
    
    return distances[0][0]   
    



#cette fonction renvoie un dataframe avec tous les facts et funfacts
def load_data():
    
    with urllib.request.urlopen('https://api.snipfeed.co/intent/fact/all/active') as url:
        Json_file = json.loads(url.read().decode())
        
    
    # we get only the data
    list_json = Json_file["data"]
    for i in list_json:
        i['displayName'] = ("CUSTOM_FUNFACT_" if (i['fun'] == 1) else "CUSTOM_FACT_") + i['theme'] + "-" + i['id']
        i['tags'].append(i['country'])
        i['tags'].append(i['theme'])
    
    #we transform it into a dataframe
    data_all = pd.DataFrame(list_json)

    collected = gc.collect() # ligne rajoutée

    return data_all
 



""" give a score of resemblance for two list of tags """
def resemblance(list_tag1, list_tag2):
    
    n1=len(list_tag1)
   
    common=list(set(list_tag1).intersection(list_tag2))
    score=len(common)/10
    return score


""" Function that creates a dictionary of tags from data and list_ref. """
def create_dict(data):
    list_ref = list(data['displayName'])
    list_tags = list(data['tags'])
    n=len(list_ref)
    dict_tag={}
    for i in range(n):
        dict_tag[list_ref[i]] = list_tags[i]
    return dict_tag



""" give a list of suggested facts in order of pertinance for a given news"""
""" give a list of suggested facts in order of pertinance for a given news"""
def suggestion(list_tags_news, list_contexts_news, dict_tags, embeddings):
    
    #initialize
    list_ref = list(dict_tags.keys())
    n = len(list_ref )
    list_scores=[] 
    list_ref_to_keep = []
    best_ref = list_contexts_news
    
    #compute de scores of the facts
    for i in range(n):
        score = resemblance_embed(dict_tags[list_ref[i]], list_tags_news, embeddings)

        list_ref_to_keep.append(list_ref[i])
        list_scores.append(score)

    
    indices = sorted(range(len(list_scores)), key=lambda k: list_scores[k])
    indices= indices[::-1]
    
    # we add the references at best_ref
    for i in range(len(indices)):
        if list_ref_to_keep[indices[i]] not in best_ref:
            best_ref.append(list_ref_to_keep[indices[i]])
    
    collected = gc.collect()

    return  best_ref[:10]






def most_relevant_fact(list_tags_news, dict_tags, embeddings):
    
    #initialize
    list_ref = list(dict_tags.keys())
    n = len(list_ref )
    list_scores=[] 
    list_ref_to_keep = []
    best_ref = []
    
    #compute de scores of the facts
    for i in range(n):
        score = resemblance_embed(dict_tags[list_ref[i]], list_tags_news, embeddings)
        if score > 0.5:
            list_ref_to_keep.append(list_ref[i])
            list_scores.append(score)

    
    indices = sorted(range(len(list_scores)), key=lambda k: list_scores[k])
    indices= indices[::-1]
    
    # we add the references at best_ref
    for i in range(len(indices)):
        if list_ref_to_keep[indices[i]] not in best_ref:
            best_ref.append(list_ref_to_keep[indices[i]])
    
    collected = gc.collect()
    
    return  best_ref
    




#============== Fonctions rajoutées ================================


def search_active(list_json):
    return [news for news in list_json if news['active'] == 1]      


#laod all the news and gives a list of dict of news
def load_news():
    
    #load data 
    link_news = 'https://api.snipfeed.co/intent/news/all'
   
    with urllib.request.urlopen(link_news) as url:
        Json_file_news = json.loads(url.read().decode())
    # we get only the data
    list_json = Json_file_news["data"]
    dict_news = search_active(list_json)
    return dict_news
        
#output a dict with all the news id by theme
def dict_by_theme(dict_news):
    
    
    dict_themes = {'gaming':[], 'mode':[],'cuisine':[],
                   'business':[], 'celebrity':[],
                   'sciences':[],'travel':[] ,'sport':[],
                   'movies':[] ,'health':[], 'music':[],'politics':[] ,
                   'news':[],'tech':[] ,
                  'selfimprovement':[],'arts':[],
                  'math':[],'history':[] }
        
    for i in range(len(dict_news)):
        theme=dict_news[i]['theme']
        if  theme in dict_themes.keys():
            dict_themes[theme].append(dict_news[i]['id'])
           
           
    return dict_themes
    



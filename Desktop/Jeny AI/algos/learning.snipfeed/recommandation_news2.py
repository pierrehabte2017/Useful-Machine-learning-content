#import
import numpy as np
import random
import pandas as pd
import urllib.request, json
from random import uniform

from useful_functions import load_news
from useful_functions import dict_by_theme


# =================== function rajoutée ============== #
class Instance:
    data_news = []
    dict_themes= {}
instance = Instance()


def update_new():

    '''import data news from database '''
    instance.data_news = load_news()
    instance.dict_themes = dict_by_theme(instance.data_news)

    
#======================================================

def give_proba(dict_scores):
    
    dict_proba = dict_scores.copy()
    liste_scores = list(dict_scores.values())
    list_category = list(dict_scores.keys())
    somme = sum(liste_scores)
    
    probas=[]
    for i in range(len(liste_scores)):
        dict_proba[list_category[i]] = liste_scores[i]/somme
        
    return dict_proba
                      

#Fonction qui pourra être amenée changer
def compute_new_score(score, nb_messages_seen):
     
    return (0.7 + nb_messages_seen*2)*score                       
              
              

def is_snip(name):
    if name[:12]=='CUSTOM_FACT' or name[:11]=='CUSTOM_FUN' or name[:15]=='CUSTOM_SUMMARY':
        return False   
    return True


#this function avoid to have a category that is never given
def avoid_extreme(dict_proba):
    
    list_keys= list(dict_proba.keys())
    for key in list_keys:
        dict_proba[key] = max( min( dict_proba[key], 0.7), 0.00000001)
    dict_proba = give_proba(dict_proba)
    return(dict_proba) 
    

def include_preferences(dict_proba, Json_file ):
    
    list_pref = Json_file['data']['entity']['theme']
    if list_pref is not None:
        for pref in list_pref:
            if pref in dict_proba.keys():
                dict_proba[pref] = dict_proba[pref] * 200
    return dict_proba
    
#compute the scores of each category directly from the feed.
#compute the scores of each category directly from the feed.

def compute_score(clientID) : 

    #initialize dict:
    dict_scores = {'gaming':1, 'mode':1,'cuisine':1,
                   'business':1, 'celebrity':1,
                   'sciences':1,'travel':1,'sport':1,
                   'movies':1,'health':1, 'music':1,'politics':1,
                   'news':1,'tech':1 ,
                  'selfimprovement':1,'arts':1,
                  'math':1,'history':1}
    
    list_keys= list(dict_scores.keys())
    list_news_done = []

    # download data
    link = 'https://api.snipfeed.co/client/' + clientID
    with urllib.request.urlopen(link) as url:
        Json_file = json.loads(url.read().decode())

    list_json = Json_file['data']['message']



    # see the number of news/fact/funfact opened 
    for i in reversed(range(len(list_json))):

        if list_json[i] is not None:

            #Si on est sur un snip, on continue 
            if( is_snip(list_json[i]['displayName']) and list_json[i]['theme'] in dict_scores.keys()):

                theme = list_json[i]['theme'] # tech, celebrity etc
                
                list_news_done.append(list_json[i]['displayName'].split('-')[1][:16])
                nb_message = 0
                compt = i

                #on va checker le nombre de messages apres la news 
                while( (not is_snip(list_json[compt-1]['displayName'])) and compt >0):      
                    nb_message += 1
                    compt = compt - 1

                #on met à jour le dico des scores

                dict_scores[theme]= compute_new_score(dict_scores[theme], nb_message)


    dict_scores = include_preferences(dict_scores, Json_file)
    dict_proba = give_proba(dict_scores)
    dict_proba  = avoid_extreme(dict_proba)


    return dict_proba, list_news_done


# GIVE A LIST OF THEME ACCORDING TO DICT OF PROABILITY FOR EACH THEME
def get_theme_from_probas(dict_proba, nb_news = 50):
    
    
    items =  list(dict_proba.keys())
    items_weights = list(dict_proba.values())
    list_themes =[]
    
    for i in range(nb_news):
        list_themes.append(random.choices(items, weights=items_weights)[0])
   
    return list_themes    
    

# GIVE A LIST NEWS ID FOR A USER 
def give_list_news_to_user(clientID):
    
    
    dict_proba, list_news_done = compute_score(clientID)
    list_themes = get_theme_from_probas(dict_proba, nb_news = 50)
    
    
    list_news_to_user = []
    
    dict_indice_theme = {'gaming':0, 'mode':0,'cuisine':0,
                   'business':0, 'celebrity':0,
                   'sciences':0,'travel':0,'sport':0,
                   'movies':0,'health':0, 'music':0,'politics':0,
                   'news':0,'tech':0 ,
                  'selfimprovement':0,'arts':0,
                  'math':0,'history':0}
    
    for i in range(len(list_themes)):
        theme = list_themes[i]
        
        if len(instance.dict_themes[theme]) > dict_indice_theme[theme]:
            
            indice = dict_indice_theme[theme]
            list_news_to_user.append(instance.dict_themes[theme][indice])
            dict_indice_theme[theme]+=1
        
      
    list_news_to_user = [x for x in list_news_to_user if x not in list_news_done] 
    
   
    return list_news_to_user
        


        
        
    
    
    
#import
import numpy as np
import random
import pandas as pd
import urllib.request, json


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


    if name[:12]=='CUSTOM_FACT_' or name[:15]=='CUSTOM_FUNFACT_' or name[:16]=='CUSTOM_SUMMARY_':

        return False   
    return True


#this function avoids to have a category that is never given or given too much
def avoid_extreme(dict_proba):
    
    list_keys= list(dict_proba.keys())
    for key in list_keys:
        dict_proba[key] = max( min( dict_proba[key], 0.4), 0.001)
    dict_proba = give_proba(dict_proba)
    
    return dict_proba
 

 #function que je viens d'inclure
def include_preferences(dict_proba, Json_file ):
    
    list_pref = Json_file['data']['entity']['theme']
    if list_pref is not None:
        for pref in list_pref:
            if pref in dict_proba.keys():
                dict_proba[pref] = (dict_proba[pref]+1) * 100
    

    return dict_proba

#compute the scores of each category directly from the feed.
# def compute_score(clientID):
    
#     # download data
#     link = 'https://api.snipfeed.co/client/' + clientID
#     with urllib.request.urlopen(link) as url:
#         Json_file = json.loads(url.read().decode())
#     list_json = Json_file['data']
 
    
#     #initialize dict:
#     dict_scores = {'gaming':1, 'mode':1,'cuisine':1,
#                    'business':1, 'celebrity':1,
#                    'sciences':1,'travel':1,'sport':1,
#                    'movies':1,'health':1, 'music':1,'politics':1,
#                    'news':1,'tech':1 ,
#                   'selfimprovement':1,'arts':1,
#                   'math':1,'history':1}
#     list_keys= list(dict_scores.keys())

    
#     # see the number of news/fact/funfact opened 
#     for i in reversed(range(len(list_json))):

#         print(list_json[i]['theme'])
#         #Si on est sur un snip, on continue 
#         if( is_snip(list_json[i]['displayName']) and list_json[i]['theme'] in dict_scores.keys()):
        
#             theme = list_json[i]['theme'] # tech, celebrity etc
#             nb_message = 0
#             compt = i

#             #on va checker le nombre de messages apres la news 
#             while( (not is_snip(list_json[compt-1]['displayName'])) and compt >0):      
#                 nb_message += 1
#                 compt = compt - 1
                
#             #on met à jour le dico des scores
            
#             dict_scores[theme]= compute_new_score(dict_scores[theme], nb_message)
            
#     #je viens de rajouter la ligne du dessous     
#     dict_proba = include_preferences(dict_scores, Json_file )
    
#     dict_proba = avoid_extreme(give_proba(dict_scores))
#     return dict_proba



#compute the scores of each category directly from the feed.
def compute_score(clientID):

    #initialize dict:
    dict_scores = {'gaming':1, 'mode':1,'cuisine':1,
                   'business':1, 'celebrity':1,
                   'sciences':1,'travel':1,'sport':1,
                   'movies':1,'health':1, 'music':1,'politics':1,
                   'news':1,'tech':1 ,
                  'selfimprovement':1,'arts':1,
                  'math':1,'history':1}
    list_keys= list(dict_scores.keys())

    # download data
    
    link = 'https://api.snipfeed.co/client/' + clientID
    
    try:
        with urllib.request.urlopen(link) as url:
            Json_file = json.loads(url.read().decode())
        
        list_json = Json_file['data']['message']



        # see the number of news/fact/funfact opened 
        for i in reversed(range(len(list_json))):
            
            if list_json[i] is not None:
                
                #Si on est sur un snip, on continue 
                if( is_snip(list_json[i]['displayName']) and list_json[i]['theme'] in dict_scores.keys()):

                    theme = list_json[i]['theme'] # tech, celebrity etc
                    nb_message = 0
                    compt = i

                    #on va checker le nombre de messages apres la news 
                    while( (not is_snip(list_json[compt-1]['displayName'])) and compt >0):      
                        nb_message += 1
                        compt = compt - 1

                    #on met à jour le dico des scores

                    dict_scores[theme]= compute_new_score(dict_scores[theme], nb_message)

             
        # dict_proba = include_preferences(dict_scores, Json_file )
        # dict_proba = avoid_extreme(give_proba(dict_scores))
        
        dict_scores = include_preferences(dict_scores, Json_file)
        
        dict_proba = give_proba(dict_scores)
        dict_proba  = avoid_extreme(dict_proba)

        return dict_proba

    except:
        print(' Problème avec le lien ', link, ' lors du calcul dict_score')
        print(' le numero clien est ',clientID)
        dict_proba = give_proba(dict_scores)

        return dict_proba

    

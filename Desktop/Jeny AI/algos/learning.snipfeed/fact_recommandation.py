
# coding: utf-8

# In[1]:


__author__ = "Pierre-Habté Nouvellon"
__version__ = "0.0.1"
__email__ = "pierrehabte_nouv@berkeley.edu"
__status__ = "Early Prototype"


# # Import

# In[2]:


#import
import random
from useful_functions import load_data
from useful_functions import create_dict
from useful_functions import suggestion
import gensim
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import KeyedVectors
import gc



class Instance:
    data = []
    dict_tags_fact =  {}
    dict_tags_fun = {}
    wv_embeddings = KeyedVectors.load_word2vec_format('/home/data/GoogleNews-vectors-negative300.bin', binary= True, limit= 500000)

instance = Instance()


#update all data

def update_data():

    '''import data from database '''
    instance.data = load_data()

    # create dictionary with all references of facts and all sheets
    instance.dict_tags_fact = create_dict(instance.data[instance.data['fun']==0])
    instance.dict_tags_fun = create_dict(instance.data[instance.data['fun']==1])

def suggest_facts(list_tag_news, count = 10):
    res = []
    
    res.append(suggestion(list_tag_news, [], instance.dict_tags_fact, instance.wv_embeddings)[:count])
    res.append(suggestion(list_tag_news, [], instance.dict_tags_fun, instance.wv_embeddings)[:count])
    return res




def verify_facts(list_tags_news):
    list_ref = most_relevant_fact(list_tags_news, instance.dict_tags_fact, instance.wv_embeddings)
    return list_ref 

def verify_fun(list_tags_news):
    list_ref = most_relevant_fact(list_tags_news, instance.dict_tags_fun, instance.wv_embeddings)
    return list_ref 


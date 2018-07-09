#import
from gensim.summarization.summarizer import summarize

import re
import operator
import urllib.request
import urllib
from bs4 import BeautifulSoup
from newspaper import Article
import nltk


#functions
def link_to_text(url1):
    
    try:
        article = Article(url1)
        article.download()
        article.parse()
        text = article.text
        return text
    except:
        return ''

    



def summarize_text(link):
    
    text = link_to_text(link)
    if len(text)==0:
        return []
    try:
        summary = summarize(text,word_count=200,split=True)
        return summary
    except:
        return [text]
    

# def simulation():
    
#     url1 = str(input(' Enter the link'))
    
#     summary = summarize_text(url1)
#     for i in range(len(summary)):
#         print( '\n',i, summary[i])
#     return summary


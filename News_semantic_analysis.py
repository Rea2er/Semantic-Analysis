from newsapi import NewsApiClient
import csv
import pandas as pd
import re
import numpy as np
import math

number_articles = 50

newsapi = NewsApiClient(api_key='97061584466e4c1a9ca46b71d0b3247d')
tag = "Canada OR University OR Dalhousie University OR Halifax OR Canada Education"
data = newsapi.get_everything(q=tag, language="en", page=1, page_size=number_articles)
articles = data['articles']


def cleanData(content):
    #  remove any @user as well as any special character, tab, white space
    return ' '.join(re.sub("(\w+://\S+)|([^0-9A-Za-z \t])", " ", content).split())


df = pd.DataFrame(data=[cleanData(article['title']) for article in articles], columns=['Title'])
df['Desc'] = np.array([cleanData(article['description']) for article in articles])
df['Content'] = np.array([cleanData(article['content']) for article in articles])

df.to_csv("news.csv", index=False, encoding="utf-8", mode="a")

term_canada_frequency = 0
term_university_frequency = 0
term_dalhousie_university_frequency = 0
term_halifax_frequency = 0
term_canada_education_frequency = 0

with open("news.csv") as file:
    for row in file:
        news = row.strip('\n')
        word_arr = row.strip('\n').split(" ")
        for word in word_arr:
            if word.lower() == "canada":
                term_canada_frequency += 1
            if word.lower() == "university":
                term_university_frequency += 1
            if word.lower() == "dalhousie":
                term_dalhousie_university_frequency += 1
            if word.lower() == "halifax":
                term_halifax_frequency += 1
            if word.lower() == "education":
                term_canada_education_frequency += 1

with open("news_TF-IDF.csv", "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(['Search Query', 'Document containing term(df)', 'Total Documents(N)/ number of documents term appeared (df)', 'Log10(N/df)'])
    writer.writerow(['Canada', term_canada_frequency, term_canada_frequency / number_articles, math.log(10, term_canada_frequency / number_articles) if term_canada_frequency != 0 else 0])
    writer.writerow(['University', term_university_frequency, term_university_frequency / number_articles, math.log(10, term_university_frequency / number_articles) if term_university_frequency != 0 else 0])
    writer.writerow(['Dalhousie University', term_dalhousie_university_frequency, term_dalhousie_university_frequency / number_articles, math.log(10, term_dalhousie_university_frequency / number_articles) if term_dalhousie_university_frequency != 0 else 0])
    writer.writerow(['Halifax', term_halifax_frequency, term_halifax_frequency / number_articles, math.log(10, term_halifax_frequency / number_articles) if term_halifax_frequency != 0 else 0])
    writer.writerow(['Canada Education', term_canada_education_frequency, term_canada_education_frequency / number_articles, math.log(10, term_canada_education_frequency / number_articles) if term_canada_education_frequency != 0 else 0])

with open("news_highest_word.csv", "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(['Term', "Canada"])
    writer.writerow(['Canada appeared in ' + 'number_articles' + ' documents', "Total Words (m)", "Frequency (f)", "Computing (f/m)"])

max_article_title = ""
max_article_computing = 0

with open("news.csv") as file:
    next(file, None)
    for row in file:
         news = row.strip('\n')
         word_arr = row.strip('\n').split(" ")
         word_count_canada = 0
         for word in word_arr:
             if word.lower() == "canada":
                 word_count_canada += 1

         with open("news_highest_word.csv", "a", newline="", encoding="utf-8") as f:
             writer = csv.writer(f)

             if word_count_canada/len(word_arr) >= max_article_computing:

                max_article_computing = word_count_canada/len(word_arr)
                max_article_title = news.split(",")[0]

             writer.writerow([news.split(",")[0], len(word_arr), word_count_canada, word_count_canada/len(word_arr)])

print("highest relative frequency of artile is: " +max_article_title)


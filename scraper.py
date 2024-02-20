import math
from bs4 import BeautifulSoup
from urllib import request
from urllib.parse import urljoin
import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, words
import re



def scrape(link, count):
    #try to open the link and return none if it fails
    try:
        html = request.urlopen(link).read().decode('utf8')
    except:
        return None, count
    

    #create soup object from link
    soup = BeautifulSoup(html)

    #filtering out pages that do not reference the main topic
    terms = ["captainsparklez", "jordan maron", "maron"]
    if not any(x in html.lower() for x in terms):
        return None, count

    #write the raw html to a file
    count += 1
    f = open(f'{count}.txt', "w+")
    f.write(html)
    f.close()
    
    #returning the soup object and count of files
    return soup, count
    
#crawl for "number" of links starting with "links"
def crawl(links, number):
    count = 0
    wikipedia_count = 0

    #list of links to skip
    skip = ['#', 'youtu.be', 'youtube', 'twitter', 'discord', 'facebook', 'twitch.tv', 'github', 'instagram',
                'wikimedia', 'wayback', "archive", "cnbc", "google", "ign", "bloomberg", "dirt.com", "Santa",
                "billboard", "telegraph", "tvguide", "soundcloud", "viaf", "cantic", ".gov", ".cz", ".pl", "musicbrainz",
                "//es.", "//id.", "//he.", "//ms.", "//ru.", "//fi.", "//vi.", "//zh.", "//sv.", "//arz.", "Talk", "index",
                "Wikipedia", "Category", "Special", "File", "DJ"]
    #crawl through all links in the list
    for x in links:
        #only letting 5 pages from wikipedia be read
        if "wikipedia" in x and wikipedia_count>4:
            continue

        #scrape the text
        soup, count = scrape(x, count)
        if soup is None:
            continue
        
        #updating count if wikipedia was used
        if "wikipedia" in x:
            wikipedia_count += 1
        
        #checking through the links on the page to see if it should be skipped or not
        for y in soup.find_all('a'):
            new_link = y.get("href")

            #if link is nonexistant skip it
            if new_link is None or new_link == "" :
                continue
            #if link is selfreferential combine it with current domain
            if new_link[0] == '/':
                new_link = urljoin(x, new_link)

            #check the link against the skip list
            useful = True
            for z in skip:
                if z in new_link:
                    useful = False
                    break

            #adding links to the list of links to crawl
            if useful:
                if new_link not in links:
                    links.append(new_link)
                pass
        #stop crawling when enough pages have been scraped
        if count >= number:
            break

#processing the raw html into something useable
def clean(number):

    #running through all the links
    for x in range(1,number+1):
        #opening the files
        try:
            f_in = open(f"{x}.txt",'r')
        except FileNotFoundError:
            break
        f_out = open(f"{x}cleaned.txt", 'w')

        #reading in the raw html and making a soup object
        html = f_in.read()
        soup = BeautifulSoup(html)

        #sorting through all the paragraph tags for which ones do not have any class or id
        # as I have found that this is the best solution so far and concatenating them
        body = soup.find_all("p",attrs={'class': None, 'id':None})
        text = ""
        for line in body:
                text = f"{text}\n{line}"

        #removing the tags from the text and outputting them to a file
        cleaned = re.sub('<.*?>', " ", text)
        f_out.write(cleaned)

#creating a term frequency dict from the tokens
def create_tf_dict(tokens):
    tf_dict = {}

    #making a dict of tokens and their counts for each unique token
    token_set = set(tokens)
    tf_dict = {t:tokens.count(t) for t in token_set}
    
    # normalizing term frequency by number of tokens
    for t in tf_dict.keys():
        tf_dict[t] = tf_dict[t] / len(tokens)
        
    return tf_dict

#calculating tf_idf for each token in tf
def create_tfidf(tf, idf):
    tf_idf = {}
    for t in tf.keys():
        tf_idf[t] = tf[t] * idf[t] 
        
    return tf_idf

def extract(number):
    important_terms = {}
    all_tokens = []
    stop_words = set(stopwords.words("english"))
    texts = []
    tf_dicts = []
    wnl = WordNetLemmatizer()
    idf_dict = {}
    tf_idf_dicts = []
    vocab = set()  

    #iterating through each file
    for x in range(1,number+1):
        #opening a file and reading it in
        try:
            f_in = open(f"{x}cleaned.txt",'r')
        except FileNotFoundError:
            continue
        text = f_in.read().lower()
        texts.append(text)

    for text in texts:
        #processing and lemmatizing the text in tokens
        tokens = nltk.word_tokenize(text)
        processed_tokens = []
        for y in tokens:
            if y.isalpha():
                if len(y) > 4:
                    if y not in stop_words: 
                        processed_tokens.append(y.lower())
        lemmatized = [wnl.lemmatize(t) for t in processed_tokens]
        all_tokens.append(lemmatized)
    
    #creating a unified set of unique tokens
    for x in all_tokens:
        vocab = vocab.union(set(x))

    #creating a tf_dict for each text
    for x in all_tokens:
        tf_dicts.append(create_tf_dict(x))
        
    #creating a list of all the vocabs
    vocab_by_topic = [t.keys() for t in tf_dicts]

    #creating idf for each text
    for term in vocab:
        temp = ['x' for voc in vocab_by_topic if term in voc]
        idf_dict[term] = math.log((1+number) / (1+len(temp))) 
    
    #creating tf idf for each text
    for x in tf_dicts:
        tf_idf_dicts.append(create_tfidf(x, idf_dict))

    #sorting each tf_idf and selecting the 25 most important terms from each
    for x in tf_idf_dicts:
        sorted_weights = sorted(x.items(), key = lambda t:t[1], reverse = True)
        for y in range(0,26):
            try:
                important_terms[sorted_weights[y][0]] = sorted_weights[y][1]
            except IndexError:
                break
    
    #sorting the combined most important terms and outputing the 40 most important terms overall
    sorted_terms = sorted(important_terms.items(), key = lambda t:t[1], reverse = True)
    for x in range(0,41):
        print(f"{sorted_terms[x][0]}:{sorted_terms[x][1]}")

    

def main():
    link = ["https://en.wikipedia.org/wiki/CaptainSparklez",]
    number = 18
    #crawl(link, number)
    #clean(number)
    extract(number)
    

if __name__ == '__main__':
    main()
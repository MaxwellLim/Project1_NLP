import urllib
from bs4 import BeautifulSoup
from urllib import request
import nltk
from nltk import sent_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download("words")
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
    for script in soup(["script", "style"]):
            script.extract()
    text = soup.get_text()
    count += 1

    #write the contents to a file
    f = open(f'{count}.txt', "w+")
    f.write(text)
    f.close()
    
    return soup, count
    

def crawl(links, number):
    count = 0
    #crawl through all links in the list
    for x in links:
        #scrape the text
        soup, count = scrape(x, count)
        if soup is None:
            continue
        #list of links to skip
        #domain = re.search('^(?:https?:\/\/)?(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,})(?:\/.*)?$', x)
        skip = ['#', 'youtu.be', 'youtube', 'twitter', 'discord', 'facebook', 'twitch.tv', 'github', 'instagram', 'afreeca',
                'wikipedia', 'wikimedia', 'wiki']
        
        #checking through the links on the page to see if it should be skipped or not
        for y in soup.find_all('a'):
            new_link = y.get("href")
            if new_link is None or new_link[0] == '/':
                continue
            useful = True
            for z in skip:
                if z in new_link:
                    useful = False
                    break
            if useful:
                #links.append(new_link)
                pass
        if count >= number:
            break

def clean(number):
    stop_words = set(stopwords.words('english'))
    tokens = []
    lemmatizer = WordNetLemmatizer()
    for x in range(1,number+1):
        try:
            f_in = open(f"{x}.txt",'r')
        except FileNotFoundError:
            break
        f_out = open(f"{x}cleaned.txt", 'w')
        text = f_in.read()
        text_chunks = [chunk for chunk in text.splitlines() if not re.match(r'^\s*$', chunk)]
        for y in text_chunks:
            f_out.write(f'{y}\n')

def calc_tf_idf():
    pass

def extract(number):
    important_terms = ()
    words = set(words.words())
    stop_words = set(stopwords.words("english"))
    for x in range(1,number+1):
        try:
            f_in = open(f"{x}cleaned.txt",'r')
        except FileNotFoundError:
            break
        text = f_in.read().lower()
        tokens = nltk.word_tokenize(text)
        processed_tokens = []
        for y in tokens:
            if y.isalpha():
                if y not in stop_words: 
                    if len(y) > 5:
                        processed_tokens.append(x.lower())
        
    pass

def main():
    link = ["https://en.wikipedia.org/wiki/Faker_(gamer)",]
    crawl(link, 30)
    clean(30)
    

if __name__ == '__main__':
    main()
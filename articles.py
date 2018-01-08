import requests
from bs4 import BeautifulSoup
from polyglot.text import Text
import spacy


    GUARDIAN_KEY= ""

    base_url= 'https://content.guardianapis.com/search?q='
    quote='"'

    search_url = base_url + quote + search_term +  quote + "&page-size=" + str(page_size) + "&api-key=" + GUARDIAN_KEY
    print("searching guardian with following url \n [%s]" % search_url)
    r = requests.get(search_url)
    # TODO - Check for 200
    if r.status_code == 200:
        return json.loads(r.content)["response"]
    else:
        print("search guardian failed " + r.reason)
        return None

def generate_ngrams(text=None, min_n = 2, max_n = 4):
    from nltk import ngrams
    if text is None:
        return None
    else:
        sentence = text
    
    n_grams = []
    words = sentence.split()
    for i in range(min_n,max_n+1):
        #current_grams = ngrams(sentence.split(), i)
        current_grams = ngrams(words, i)
        for grams in current_grams:
            n_grams.append( ' '.join(grams))
    
    if len(n_grams) > 0 :
        return n_grams
    else:
        return None



def download_article(web_url):
    print("downloading article from url: \n[%s]" % web_url)
    r = requests.get(web_url)
    if r.status_code != 200:
        print("download article failed " + r.reason)
        return None
    # TODO : Check for 200
    soup = BeautifulSoup(r.content, 'html.parser')
    text_element = soup.find('div', attrs={'class':"content__article-body"} )
    if text_element is None:
        text = ""
    else:
        text = text_element.text

    return text

def fuzzy_search(search_term, article_list, matching_ratio=80):
    from fuzzywuzzy import fuzz
    result = []
    for article in article_list:
        match_found = False
        for word in article["ngrams"]:
            #if len(word.split()) == len(search_term.split()):
            fuzz_ratio = fuzz.token_set_ratio(search_term, word) 
            if  fuzz_ratio > matching_ratio :
                print("term [%s] word [%s] ratio [ %d] " % (search_term, word, fuzz_ratio ))
                match_found = True
            if match_found is True:
                #print_article(article)
                result.append(article)
                break
        
    return result


def parse_search_result(search_response):
    results = search_response["results"]
    num_pages = search_response["pages"]
    act_page_size = search_response["pageSize"]
    search_articles = []
    for i in range(0, act_page_size):
        web_url = results[i]["webUrl"]
        publish_date = results[i]["webPublicationDate"]
        title = results[i]["webTitle"]
        # print("Date [ %s] Title [%s]" % (publish_date, title))
        text = download_article(web_url)
        if text is None:
            continue

        article = {
            "title" : title,
            "date" : publish_date,
            "url" : web_url,
            "text" : text
        }

        search_articles.append(article)
    
    return search_articles
    
    #print(json.dumps(article))

def print_article(article):
    print(article["title"])
    print(article["date"])
    print(article["text"][:600])
    print(article["ngrams"])
    #print(article["entities"])
    for key in article["entities"].keys():
        for entity in article["entities"][key]:
            print("entity type [%s] entity [%s] length [%d] type [%r]" % (key, entity, len(entity), type(entity)))

def check_string(input):
    if all(x.isalpha() or x.isspace() or x.isdigit() for x in input):
        return True
    return False

def extract_entities(article_list):
    new_articles = []
    for i in range(0, len(article_list)):
        print("Parsing article number %d " % (i))
        article = {}
        copy_article(article_list[i], article)
        parsed_text = Text(article["text"])
        article["entities"] = {}
        article["ngrams"] = []
        if parsed_text == "":
            print("Skipping article %d" % i)
            continue
        for sent in parsed_text.sentences:
            for entity in sent.entities:
                named_entity = ' '.join(entity)
                if not(check_string(str(named_entity)) == True):
                    continue
                #n_grams = generate_ngrams(article["text"], min_n=2, max_n=len(entity))
                n_grams = generate_ngrams( named_entity, min_n=2, max_n=len(entity))
                if n_grams is not None:
                    article["ngrams"].extend(n_grams)
                if entity.tag not in article["entities"].keys():
                    article["entities"][entity.tag] = [named_entity]
                else:
                    article["entities"][entity.tag].append(named_entity)
        for key in article["entities"].keys():
            article["entities"][key] = list(set(article["entities"][key]))

        unique_ngrams = list(set(article["ngrams"]))
        article["ngrams"] = unique_ngrams
        new_articles.append(article)
    return new_articles

# article2 = extract_entities(article)

def extract_entities_spacy(article_list):
    new_articles = []
    nlp = spacy.load('en')
    for i in range(0, len(article_list)):
        print("Parsing article number %d " % (i))
        article = {}
        copy_article(article_list[i], article)
        
        doc = nlp(article["text"])
        article["entities"] = {}
        article["ngrams"] = []

        for ent in doc.ents:
            if ent.label_ not in article["entities"].keys():
                article["entities"][ent.label_] = [ent.text]
            else:
                article["entities"][ent.label_].append(ent.text)
            article["ngrams"].append(ent.text)

        for key in article["entities"].keys():
            article["entities"][key] = list(set(article["entities"][key]))

        article["ngrams"] = list(set(article["ngrams"]))
        new_articles.append(article)
    return new_articles


def copy_article(source, target):
    for key in source.keys():
        target[key] = source[key]

def copy_articles(source, target):
    for i in range(0, len(source)):
        article = {}
        copy_article(source[i], article)
        target.append(article)



def save_articles(file_name, data):
    import json
    with open(file_name,encoding="utf-8", mode='w') as f:
        json.dump(data, f, ensure_ascii=False)

articles = []
search_term = "money laundering"
page_size=200
search_response = search_guardian(search_term=search_term, page_size=page_size)
# Load the results in to articles
articles = []
articles = parse_search_result(search_response)

a2 = []
copy_articles(articles, a2)
len(articles)
len(a2)
new_articles = extract_entities_spacy(a2)

a3 = []
copy_articles(articles, a3)

save_articles("/Users/rdx/Documents/knowledge/data/articles_guardian.json", new_articles)

save_articles("/Users/rdx/Documents/knowledge/data/articles_guardian_spacy.json", a3)
# matching_articles = fuzzy_search("perram", new_articles)





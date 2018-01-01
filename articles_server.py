from flask import Flask, request
from flask_restful import Resource, Api
from fuzzywuzzy import fuzz
import json
import logging
from logging.handlers import RotatingFileHandler
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

articles = []
log = lambda msg: app.logger.info(msg, extra={'app': __name__ })

def load_articles():
    file_name = "/Users/rdx/Documents/knowledge/data/articles_guardian.json"
    return json.load(open(file_name,'r'))

def fuzzy_search(search_term, article_list, matching_ratio=80):
    from fuzzywuzzy import fuzz
    result = []
    #log("Inside fuzzysearch now ")
    for article in article_list:
        for word in article["ngrams"]:
            #if len(word.split()) == len(search_term.split()):
            fuzz_ratio = fuzz.partial_ratio(search_term, word) 
            
            if  fuzz_ratio > matching_ratio :
                log("term [%s] word [%s] ratio [%d] " % (search_term, word, fuzz_ratio ))
                #print_article(article)
                log("Found article : title [%s] " % article["title"])
                result.append(article)
                break
        
    return result


class Articles(Resource):
    def get(self, search_string):
        result = fuzzy_search(search_string, articles, 65)
        return result                
        
    
    def put(self):
        pass

api.add_resource(Articles, '/articles/<string:search_string>')


if __name__ == "__main__":
    articles = load_articles()
    LOG_FILENAME='/Users/rdx/Documents/knowledge/logs/foo.log'
    app.debug = True
    app.debug_log_format = """[%(pathname)s:%(lineno)d]:\n%(message)s"""
    app.run(debug=True)
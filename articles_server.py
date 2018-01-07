from flask import Flask, request
from flask_restful import Resource, Api
from fuzzywuzzy import fuzz
import json
import logging
from logging.handlers import RotatingFileHandler
from flask_cors import CORS
import networkx as nx
from networkx.readwrite import json_graph
from random import choice

app = Flask(__name__)
api = Api(app)
CORS(app)

articles = []
G = nx.Graph()
log = lambda msg: app.logger.info(msg, extra={'app': __name__ })

def generate_cases():
    case_start = 101
    num_cases = 9
    case_max = case_start + num_cases +1 
    case_range = range(case_start,case_start + num_cases + 1)
    return case_range


def generate_persons():
    person_start = 201
    num_persons = 21
    person_max = person_start + num_persons +1
    person_range = range(person_start, person_start + num_persons + 1)
    return person_range

def generate_orgs():
    org_start = 301
    num_orgs = 2 
    org_max = org_start + num_orgs + 1
    org_range = range(org_start, org_start + num_orgs + 1)
    return org_range

def generate_articles():
    article_start = 401
    num_articles = 5 
    article_max = article_start + num_articles + 1
    article_range = range(article_start, article_max)
    return article_range


def generate_counterparties():
    counterparties = [
        (201, 205),
        (203, 206),
        (204, 205),
        (205, 214),
        (206, 208),
        (206, 207),
        (207, 209),
        (208, 209),
        (208, 220),
        (210, 211),
        (212, 221),
        (217, 219),
        (217, 218),
        (217, 216),
        (218, 220),
        (218, 219),
        (221, 211)
    ]

    return counterparties


def generate_employees():
    employees = [
        (202, 301),
        (203, 301),
        (212, 302),
        (213, 302),
        (216, 303),
        (219, 303)
    ]
    return employees

def generate_involved_parties():
    involved_parties = [
        (101, 202),
        (101, 203),
        (101, 204),
        (101, 201),
        (102, 214),
        (102, 211),
        (103, 205),
        (104, 204),
        (104, 210),
        (105, 215),
        (106, 210),
        (107, 210),
        (108, 220),
        (109, 213),
        (109, 212),
        {109, 216}
        
    ]
    return involved_parties


def generate_aliases():
    # aliases = [
    #     (210, 220),
    #     (210, 215)
    # ]

    aliases = []

    return aliases

def generate_mentions():
    mentions = []
    choice_list = []
    choice_list.extend(generate_persons())
    choice_list.extend(generate_orgs())
    for article_num in generate_articles():
        chosen = choice(choice_list)
        mentions.append((article_num, chosen))
    
    return mentions
        




def generate_graph():


    G.add_nodes_from(generate_cases(), type="case")
    G.add_nodes_from(generate_persons(), type="person")
    G.add_nodes_from(generate_orgs(), type="org")
    G.add_nodes_from(generate_articles(), type="article")

    G.add_edges_from(generate_counterparties(), relationship = "counterparty")
    G.add_edges_from(generate_employees()   , relationship = "employee")
    G.add_edges_from(generate_involved_parties()  , relationship = "involve")
    G.add_edges_from(generate_aliases()  , relationship = "sameAs")
    G.add_edges_from(generate_mentions()  , relationship = "mentions")



def get_neighbors(node_id, type=None, radius =1):
    neighbors = []
    print("Fetching neighbors of [%d]" % (node_id))
#     for n in G.neighbors(node_id):
    for n in nx.ego_graph(G, node_id, radius=radius):
        attrs = G.nodes(data=True)[n]
        if type is None:
            neighbors.append(n)
        elif "type" in attrs.keys() and attrs["type"] == type:
            neighbors.append(n)
    return neighbors

def metrics(case_id,G, ignore_list=[], level=0):
    # All other cases on entities in a case
    edges = G.edges(case_id, data=True)
    res = {}
    res["aliases"] = set()
    res["alias_cases"] = set()
    res["other_cases"] = set()
    for edge in edges:
       
        if edge[1] in ignore_list :
#             print("[%d] Skipping edge (%d,%d) (%s) " % (level,edge[0], edge[1], edge[2]["relationship"]))
            continue
        if edge[2]["relationship"] == "sameAs":
            res["aliases"].update(edge[1])            
        elif edge[2]["relationship"] == "involve":
                res["other_cases"].add(edge[1])


        elif edge[2]["relationship"] == "employee":
#             print("[%d] 2Recursively calling related_cases with [%s] id [%d] [%s]" % (level,G.nodes()[edge[1]]["type"], edge[1],edge[2]["relationship"]))       
            result_cases.update(related_cases(edge[1], G, [edge[0]], level+1)) #2
        elif edge[2]["relationship"] == "counterparty":
#             print("[%d] 3Recursively calling related_cases with [%s] id [%d] [%s]" % (level,G.nodes()[edge[1]]["type"], edge[1],edge[2]["relationship"]))
            ignore_list.append(edge[1])
#             print("[%d] 3IgnoreList" % level)
#             print(ignore_list)
            result_cases.update(related_cases(edge[1], G, ignore_list, level+1)) #2
    
    # result_cases = result_cases.remove(case_id)
#     print(result_cases)
    return list(result_cases)

def related_cases(case_id,G, ignore_list=[], level=0):
    # All other cases on entities in a case
    edges = G.edges(case_id, data=True)

    result_cases = {}
    result_cases["aliases"] = set()
    result_cases["alias_cases"] = set()
    result_cases["other_cases"] = set()
    result_cases["org_cases"] = set()
    result_cases["cpty_cases"] = set()
    r = None
    for edge in edges:
        aliases = set()
        alias_cases = set()
        other_cases = set()
        org_cases = set()
        cpty_cases = set()

        r = None
       
        if edge[1] in ignore_list :
            continue
        else:
            pass
        if edge[2]["relationship"] == "sameAs":
            result_cases["aliases"].add(edge[1])
            r = related_cases(edge[1], G, [edge[0]],level+1)
        elif edge[2]["relationship"] == "involve":
            if G.nodes()[edge[1]]["type"] == "case":
                result_cases["other_cases"].add(edge[1])
            else:
                r = related_cases(edge[1], G, [edge[0]], level+1)
        elif edge[2]["relationship"] == "employee":
            r = related_cases(edge[1], G, [edge[0]], level+1)
        elif edge[2]["relationship"] == "counterparty":
            ignore_list.append(edge[1])

            r = related_cases(edge[1], G, ignore_list, level+1)
        else:
            continue
    
    if r is not None:
            result_cases["aliases"].update(r["aliases"])
            result_cases["alias_cases"].update(r["alias_cases"])
            result_cases["other_cases"].update(r["other_cases"])
            result_cases["org_cases"].update(r["org_cases"])
            result_cases["cpty_cases"].update(r["cpty_cases"])
            log("[%d] - r " % (level))
            log(r)    

    result_cases["aliases"] = list(result_cases["aliases"] )
    result_cases["alias_cases"] = list(result_cases["alias_cases"] )
    result_cases["other_cases"] = list(result_cases["other_cases"] )
    result_cases["org_cases"] = list(result_cases["org_cases"])
    result_cases["cpty_cases"] = list(result_cases["cpty_cases"])

    return result_cases

def vis_json(graph_data):
    nodes_data = graph_data["nodes"]
    links_data = graph_data["links"]
    graph_data["edges"] = graph_data.pop("links")
    for item in nodes_data:
        item["label"] = str(item["id"])
        item["group"] = item.pop("type")
        
    for item in links_data:
        item["from"] = item.pop("source")
        item["to"] = item.pop("target")
        item["label"] = item.pop("relationship")

def load_articles():
    file_name = "data/articles_guardian.json"
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

def print_log(message):
    log(message)


class Network(Resource):
    def get(self):
        json_data = json_graph.node_link_data(G)
        vis_json(json_data)
        log(json_data)
        return json_data

    def put(self):
        pass

class EgoGraph(Resource):
    def get(self, input_str):
        log("Received request [%s] " % (input_str))
        input_params = json.loads(input_str)
        node_num = int(input_params["id"][0])
        radius = input(input_params["radius"])
        ego = nx.ego_graph(G, node_num, radius = radius)
        json_data = json_graph.node_link_data(ego)
        vis_json(json_data)
        log("Returning data ")
        log(json_data)
        return json_data

    def put(self):
        pass


class Metrics(Resource):
    def get(self, node_id):
        log("Received request [%d] " % (node_id))
        results = related_cases(node_id, G, [node_id])
        log(results)
        log("Returning data ")
        
        return results

    def put(self):
        pass


api.add_resource(Articles, '/articles/<string:search_string>')
api.add_resource(Network, '/network')
api.add_resource(EgoGraph, '/network/<string:input_str>')
api.add_resource(Metrics, '/network/metrics/<int:node_id>')


if __name__ == "__main__":
    articles = load_articles()
    generate_graph()

    LOG_FILENAME='logs/foo.log'
    app.debug = True
    app.debug_log_format = """[%(pathname)s:%(lineno)d]:\n%(message)s"""
    app.run(debug=True)
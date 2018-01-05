from faker import Faker
from faker.providers import BaseProvider
import datetime
import string

from random import choice

fake = Faker()


class ArticleProvider(BaseProvider):
    def fake_article(self):
        
        return {
            "published_date" : str(fake.date_between(start_date="-1y", end_date="-30d")),
            "id" : 'ART' + ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(5)),
            # "text" : fake.paragraphs(),
            "title" : fake.sentence()
            
        }

fake.add_provider(ArticleProvider)

class EntityProvider(BaseProvider):
    def fake_entity(self):
        
        return {
            "name" : fake.name(),
            "id" : 'ENT' + ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(5)),
            "iban" : fake.ean()
        }

fake.add_provider(EntityProvider)

statuses = ["New", "Open", "Triage", "Under Investigation",  "Closed"]
class CaseProvider(BaseProvider):
    def fake_case(self):
        created_date = fake.date_between(start_date="-1y", end_date="-30d")
        case = {
            "created_date" : str(created_date),
            "id" : 'C' + ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(9)),
            "status" : choice(statuses),
            "closed_date" : None
        }
        if case["status"] == "Closed":
            case["closed_date"]  = str(fake.date_between(start_date=created_date, end_date="-10d"))

        return case

fake.add_provider(CaseProvider)


# 3 articles
# each article has 3 entities
articles = {}
entities = {}
cases = {}
num_articles = 3
num_entities = 3
num_cases = 3

G = nx.Graph()
for i in range(0,num_articles):
    article = fake.fake_article()
    articles[article["id"]] = article

    # Add node, set the type and then the properties
    G.add_node(article["id"])
    G.node[article["id"]]["type"] = "article" 
    G.node[article["id"]]["properties"] = article

    #entities = {}
    for j in range(0, num_entities):
        entity = fake.fake_entity()
        entities[entity["id"]] = entity
        # Add node, set the type and then the properties
        G.add_node(entity["id"])
        G.node[entity["id"]]["type"] = "entity" 
        G.node[entity["id"]]["properties"] = entity
        
        # Add edge from outer id to inner id
        # Set the edge type
        G.add_edge(article["id"], entity["id"])
        #print(G.edges(data=True))
        G.edges[(article["id"],entity["id"])]["type"] = "mentions"
        # cases = {}
        for k in range(0, num_cases):
            case = fake.fake_case()
            cases[case["id"]] = case
            # Add node, set the type and then the properties
            G.add_node(case["id"])
            G.node[case["id"]]["type"] = "case"
            G.node[case["id"]]["properties"] = case

            # Add edge from outer id to inner id
            # Set the edge type
            G.add_edge(entity["id"], case["id"])
            G.edges[(entity["id"],case["id"])]["type"] = "is_involved_in"
        


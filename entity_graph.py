import networkx as nx
import itertools

# Extract all the entities from articles
def ner(text, output="both"):
    import polyglot.text as Text
    parsed = Text(text)
    for sent in parsed.sentences:
        for entity in sent.entities:
            if output is "both":
                yield entity.tag, entity
            elif output is "tag":
                yield entity.tag
            elif output is "entity":
                yield entity
            else:
                yield None

def check_string(input):
    if all(x.isalpha() or x.isspace() or x.isdigit() for x in input):
        return True
    return False

# Create a graph with all the entities returned 
# from the ner() [ named entity recognition ]
G = nx.Graph()
for article in articles:
    nodes = [ ' '.join(e) for e in ner(article["text"], output="entity") if check_string(' '.join(e)) ]
    edges = list(itertools.permutations(nodes,2))
    current_nodes = G.number_of_nodes()
    current_edges = G.number_of_edges()
    new_nodes = len(nodes)
    new_edges = len(edges)
    expected_nodes = current_nodes + new_nodes
    expected_edges = current_edges + new_edges
   
    
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    
    actual_nodes = G.number_of_nodes()
    actual_edges = G.number_of_edges()
    print("B - N[%10d] E[%10d] , A - N[%10d] E[%10d] , Delta - N[%10d] E[%10d] " % (current_nodes, current_edges, actual_nodes, actual_edges, actual_nodes-current_nodes, actual_edges-current_edges))

# Delete all the entities from the 
# graph in reverse order
for article in reversed(a2):
    nodes = [ ' '.join(e) for e in ner(article["text"], output="entity") if check_string(' '.join(e)) ]
    edges = list(itertools.permutations(nodes,2))
    current_nodes = G.number_of_nodes()
    current_edges = G.number_of_edges()
    new_nodes = len(nodes)
    new_edges = len(edges)
    expected_nodes = current_nodes - new_nodes
    expected_edges = current_edges - new_edges
   
    G.remove_edges_from(edges)
    G.remove_nodes_from(nodes)
   
    
    actual_nodes = G.number_of_nodes()
    actual_edges = G.number_of_edges()
    print("B - N[%10d] E[%10d] , A - N[%10d] E[%10d] , Delta - N[%10d] E[%10d] " % (current_nodes, current_edges, actual_nodes, actual_edges, actual_nodes-current_nodes, actual_edges-current_edges))


# tf, idf and idf calculations
from nltk import word_tokenize
from nltk.corpus import stopwords
from string import punctuation

def tokenize(text):
    stop_words = stopwords.words('english') + list(punctuation)
    words = word_tokenize(text)
    words = [ w.lower() for w in words ]
    return [ w for w in words if w not in stop_words ]

def prepare_vocabulary(documents):
    vocabulary = set()
    for document in documents:
        if isinstance(document, str):
            words = tokenize(document)
            vocabulary.update(words)
    vocabulary = list(vocabulary)

    return vocabulary

def index_words(vocabulary):
    # Returns a {w:index} dictionary of all words in a list
    return { w : index for index, w in enumerate(vocabulary)}

def idf(documents):
    from collections import defaultdict
    import math
    word_idf = defaultdict(lambda : 0 )
    for document in documents:
        if isinstance(document, str):
            words = set(tokenize(document))
        for word in words:
            word_idf[word] += 1
    
    for word in prepare_vocabulary(documents):
        word_idf[word] = math.log(len(documents) / float(1 + word_idf[word]))
    
    return word_idf

def word_tf(word, document):
    if isinstance(document, str):
        document = tokenize(document)
    return float(document.count(word)) / len(document)


def tf_idf(word, document):
    if isinstance(document, str):
        document = tokenize(document)

    vocabulary = prepare_vocabulary(document)
    word_index = index_words()

vocabulary = prepare_vocabulary(documents)
word_index = index_words(vocabulary)
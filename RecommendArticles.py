
# coding: utf-8

# In[50]:


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


# In[54]:


categories = { 
    "bribery" : "bribery",
    "hezbollah" : "terrorism",
    "manu" : "sports",
    "moneylaundering" : "financialcrime"
}

ds = None

for category in categories.keys():
    file_path = "data/articles_guardian_" + category + ".json"
    print(file_path)
    if ds is None:
        ds = pd.read_json(file_path)
        ds["category"] = category
        print("Loading %d rows for %s " % ( len(ds2.index), category))
        
    else:
        ds2 = pd.read_json(file_path)
        ds2["category"] = category
        ds = pd.concat([ds, ds2], ignore_index = True)
        print("Loading %d rows for %s " % ( len(ds2.index), category))
    
print("total articles in ds are %d " % (len(ds.index)))


# In[62]:


# Resetting index is necessary so that we can use id later on
ds.reset_index(drop=True)

ds["id"] = ds.index

tf = TfidfVectorizer(analyzer="word", ngram_range=(1,3), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(ds["text"])


# In[63]:


cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

results = {}

for idx, row in ds.iterrows():
    similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
    similar_items = [(cosine_similarities[idx][i], ds['id'][i]) for i in similar_indices]
    
    results[row['id']] = similar_items[1:]

print("Done!")


# In[64]:


# hacky little function to get a friendly item name from the description field, given an item ID
def item(item_id):
    return ds.loc[ds['id'] == item_id]['text'].tolist()[0].split(' - ')[0]

# Just reads the results out of the dictionary. No real logic here.
def recommend(item_id, num):
    print("#"*90)
    print("Recommending " + str(num) + " products similar to " + item(item_id=item_id)[:500] + "...")
    print("*"*90)
    recs = results[item_id][:num]
    for rec in recs:
        print("Recommended: " + " (score:" + str(rec[0]) + ")"+ item(rec[1])[0:500] )
        print("*"*90)


for item_id in [11,111,211,311,411,511,611,711]:
    recommend(item_id, num=5)


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import random


products = pd.read_json('product_data.json')

products['AuthorId'] = products['AuthorId'].fillna('').astype(str)
products['Desc'] = products['Desc'].fillna('').astype(str)
products['CategoryId'] = products['CategoryId'].fillna('').astype(str)

products['content'] = products['AuthorId'] + ' ' + products['Desc'] + ' ' + products['CategoryId']

tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0.01)
tfidf_matrix = tf.fit_transform(products['content'])

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

indices = pd.Series(products.index, index=products['Id']).drop_duplicates()

def get_recommendations(productId):
    idx = indices[productId]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    product_indices = [i[0] for i in sim_scores]
    return products['Id'].iloc[product_indices].tolist()


def get_random_recommendations():
    return random.sample(products['Id'].tolist(), 10)

result = get_recommendations(1500)
print(result)

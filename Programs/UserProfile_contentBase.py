import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import Ridge
from sklearn.feature_extraction.text import TfidfVectorizer





n_user = pd.read_json('UserData.json')
n_rating = pd.read_json('CommentData.json')
n_product = pd.read_json('product_data.json')

# chia n_rating thành 2 tập dữ liệu: tập dữ liệu huấn luyện và tập dữ liệu kiểm tra

train_data, test_data = train_test_split(n_rating, test_size=0.2)

vectorizer = TfidfVectorizer()
x_train_counts = vectorizer.fit_transform(n_product['text'])

transformer = TfidfTransformer(smooth_idf=True, norm ='l2')
tfidf = transformer.fit_transform(x_train_counts.tolist()).toarray()

def get_item_rated_by_user(rate_matrix, user_id):
    y = rate_matrix[:, 0]

    ids = np.where(y == user_id + 1)[0]
    item_ids = rate_matrix[ids, 1] - 1
    scores = rate_matrix[ids, 2]
    return (item_ids, scores)


d = tfidf.shape[1]
W = np.zeros((d, n_user))
b = np.zeros((1, n_user))

for n in range(n_user):
    ids, scores = get_item_rated_by_user(train_data, n)
    clf = Ridge(alpha=0.01, fit_intercept = True)
    Xhat = tfidf[ids, :]
    clf.fit(Xhat, scores)
    W[:, n] = clf.coef_
    b[0, n] = clf.intercept_

Yhat = tfidf.dot(W) + b

n = 10
ids, scores = get_item_rated_by_user(test_data, n)
Yhat[n, ids]
print('Rated movies ids:', ids)
print('True ratings:', scores)
print('Predicted ratings:', Yhat[n, ids])





import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import random
import time


products = pd.read_json('product_data.json')

products['AuthorId'] = products['AuthorId'].fillna('').astype(str)
products['Desc'] = products['Desc'].fillna('').astype(str)
products['CategoryId'] = products['CategoryId'].fillna('').astype(str)
products['content'] = products['AuthorId'] + ' ' + products['Desc'] + ' ' + products['CategoryId']

# tạo đối tượng TfidfVectorizer và fit dữ liệu vào đối tượng đó
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0.01)
tfidf_matrix = tf.fit_transform(products['content'])
# tfidf matrix shape = (số lượng sản phẩm, số lượng từ trong tập dữ liệu)


cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
# cosine_sim shape = (số lượng sản phẩm, số lượng sản phẩm)

#tạo một series với index là Id của sản phẩm và giá trị là index của sản phẩm trong tập dữ liệu
indices = pd.Series(products.index, index=products['Id']).drop_duplicates()
print(indices)

def get_recommendations(productId):
    idx = indices[productId]
    # tính toán điểm tương đồng giữa sản phẩm đầu vào và các sản phẩm còn lại
    sim_scores = list(enumerate(cosine_sim[idx]))
    # sắp xếp các sản phẩm theo thứ tự giảm dần của điểm tương đồng
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # lấy ra 10 sản phẩm có điểm tương đồng cao nhất loại bỏ sản phẩm đầu vào
    sim_scores = sim_scores[1:11]
    product_indices = [i[0] for i in sim_scores]
    return products['Id'].iloc[product_indices].tolist()


def get_random_recommendations():
    return random.sample(products['Id'].tolist(), 10)

start_time = time.time()
result = get_recommendations(2)
print(result)
end_time = time.time()
print(f"Time: {end_time - start_time}")
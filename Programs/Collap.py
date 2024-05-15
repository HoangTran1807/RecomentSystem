import pandas as pd
import numpy as np
import seaborn as sns
from collections import Counter
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity



users = pd.read_json('UserData.json')
ratings = pd.read_json('CommentData.json')
products = pd.read_json('product_data.json')

# # hiển thị 4 dòng đầu của mỗi bảng
# print("simple data:")
# print(users.head(4))
# print(ratings.head(4))
# print(products.head(4))

# # hiển thị thông tin của mỗi bảng
# print("shape of data:")
# print( "users: ", users.shape)
# print( "Ratings: ", ratings.shape)
# print("Product: " ,products.shape)

# # hiển thị chi tiết bảng ratings
# n_ratings = len(ratings)
# n_products = ratings['ProductID'].nunique()
# n_users = ratings['UserID'].nunique()

# print("Number of ratings: ", n_ratings)
# print("Number of unique users: ", n_users)
# print("Number of unique products: ", n_products)
# print("average number of ratings per user: ", round(n_ratings/n_users, 2))
# print("average number of ratings per product: ", round(n_ratings/n_products, 2))


# # hiển thị mức rating trung bình của mỗi sản phẩm
# average_rating = ratings.groupby('ProductID')['Rating'].mean()
# print(average_rating)

# # hiển thị mức rating trung bình của mỗi người dùng
# average_rating = ratings.groupby('UserID')['Rating'].mean()
# print(average_rating)

# # hiển thị mức rating trung bình của tất cả sản phẩm
# average_rating = ratings['Rating'].mean()
# print(average_rating)

# # hiển thị mức rating trung bình của tất cả người dùng
# average_rating = ratings['Rating'].mean()
# print(average_rating)

# # hiển thị 10 sản phẩm có số lượng rating cao nhất
# product_rating_count = ratings.groupby('ProductID')['Rating'].count()
# print(product_rating_count.sort_values(ascending=False).head(10))
# # hiển thị 10 sản phẩm có số lượng rating thấp nhất
# print(product_rating_count.sort_values(ascending=True).head(10))

# # hiển thị 10 người dùng có số lượng rating cao nhất
# user_rating_count = ratings.groupby('UserID')['Rating'].count()
# print(user_rating_count.sort_values(ascending=False).head(10))
# # hiển thị 10 người dùng có số lượng rating thấp nhất
# print(user_rating_count.sort_values(ascending=True).head(10))

# # hiển thị thể loại của sản phẩm
# genre_ferquency = Counter(g for genres in products['CategoryId'] for g in genres)
# print(genre_ferquency)


# ====================================================================================================

def create_X(df):
    M = df['UserID'].nunique()
    N = df['ProductID'].nunique()

    user_mapper = dict(zip(np.unique(df['UserID']), list(range(M))))
    product_mapper = dict(zip(np.unique(df['ProductID']), list(range(N))))

    user_inv_mapper = dict(zip(list(range(M)), np.unique(df['UserID'])))
    product_inv_mapper = dict(zip(list(range(N)), np.unique(df['ProductID'])))

    user_index = [user_mapper[i] for i in df['UserID']]
    product_index = [product_mapper[i] for i in df['ProductID']]

    X = csr_matrix((df['Rating'], (user_index, product_index)), shape=(M, N))
    return X, user_mapper, product_mapper, user_inv_mapper, product_inv_mapper


X, user_mapper, product_mapper, user_inv_mapper, product_inv_mapper = create_X(ratings) 


# đánh giá độ thưa thớt của dữ liệu để xem liệu nên sử dụng lọc cộng tác hay lọc nội dung
# đối với tập dữ liệu thưa thớt lọc theo nội dung thường tốt hơn lọc cộng tác
# nnz là số lượng phần tử khác 0 trong ma trận
# nếu độ thưa thớt lớn hơn 0.1 nên tiếp tục sử dụng lọc cộng tác ngược lại sử dụng lọc theo nội dung
n_total = X.shape[0] * X.shape[1]
n_ratings = X.nnz
sparsity = n_ratings / n_total
print(f"sparsity: {sparsity}")

# hiển thị số lượng rating của người dùng tích cực nhất và người dùng ít tích cực nhất

n_ratings_per_user = X.getnnz(axis=1)
print(len(n_ratings_per_user))
print("most active user rated:", n_ratings_per_user.max())
print("least active user rated:", n_ratings_per_user.min())

# hiển thị số lượng rating của sản phẩm được đánh giá nhiều nhất và ít nhất
n_ratings_per_product = X.getnnz(axis=0)
print(len(n_ratings_per_product))
print("most rated product has:", n_ratings_per_product.max())
print("least rated product has:", n_ratings_per_product.min())


#xây dựng model lọc cộng tác sử dụng kĩ thuật k-nearest neighbors

# from sklearn.neighbors import NearestNeighbors

# def find_similar_products(product_id, X, movie_mapper, movie_inv_mapper, k, metric='cosine'):
#     X = X.T
#     neighbour_ids = []
#     product_ind = movie_mapper[product_id]
#     product_vec = X[product_ind]
#     if isinstance(product_vec, (np.ndarray)):
#         product_vec = product_vec.reshape(1, -1)
#     kNN = NearestNeighbors(n_neighbors=k+1, algorithm="brute", metric=metric)
#     kNN.fit(X)
#     neighbour = kNN.kneighbors(product_vec, return_distance=False)
#     for i in range(1, k):
#         n = neighbour.item(i)
#         neighbour_ids.append(movie_inv_mapper[n])
#     return neighbour_ids

# similar_products = find_similar_products(10, X, product_mapper, product_inv_mapper, k=10)


# # hiển thị tên sản phẩm có id = 10 và tên các sản phẩm tương tự
# movie_id = 10
# print("because you watched: ", products[products['Id'] == movie_id]['Name'].values[0])
# print("you should watch: ")
# for i in similar_products:
#     print(products[products['Id'] == i]['Name'].values[0])


# ====================================================================================================

genres = set(g for genres in products['CategoryId'] for g in genres)

for g in genres:
    products[g] = products['CategoryId'].apply(lambda x: 1 if g in x else 0)

products_s = products.drop(columns=['Name', 'SupplierId', 'AverageRating' ,'AuthorId', 'Desc', 'CategoryId', 'content'], errors='ignore')

print(products_s[10:20])

#tạo ma trận cosine similarity
cosine_sim = cosine_similarity(products_s, products_s)

n_recommendations = 10
sim_scores = list(enumerate(cosine_sim[10]))
sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
sim_scores = sim_scores[1:n_recommendations+1]
product_indices = [i[0] for i in sim_scores]

print(products['Id'].iloc[product_indices].tolist())

# ====================================================================================================


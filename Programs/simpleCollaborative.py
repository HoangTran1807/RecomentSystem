import pyodbc
import time
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

try:
    start_time = time.time()
    # Kết nối đến cơ sở dữ liệu SQL Server
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-38TO487\SQLEXPRESS;DATABASE=Fahasa;UID=Hoang;PWD=123')
    cursor = conn.cursor()

    # Truy vấn để lấy dữ liệu từ bảng product
    cursor.execute('''
    select  id from people
''')
    listUser = cursor.fetchall()

    cursor.execute('''
    select  id from product
''')
    listProduct = cursor.fetchall()

    cursor.execute('''
    select productid,userid, rating from comment
''')
    
    ratings = cursor.fetchall()

except Exception as e:
    print(f"Loi : {e}")


# tạo ma trận user và product nếu rating = 0 thì gán giá trị = null
user_matrix = np.zeros((len(listUser), len(listProduct)))
for rating in ratings:
    user_matrix[rating[1] - 1][rating[0] - 1] = rating[2]

# # Tính giá trị trung bình của mỗi người dùng
# avg_rating = np.zeros(len(listUser))

# for i in range(len(listUser)):
#     sum_rating = 0
#     count_rating = 0
#     for j in range(len(listProduct)):
#         if user_matrix[i][j] > 0:
#             sum_rating += user_matrix[i][j]
#             count_rating += 1
#     if count_rating == 0:
#         continue
#     avg_rating[i] = sum_rating / count_rating

# # duyệt ma trận user_matrix nếu rating != 0 thì gán giá trị = rating - avg_rating
# for i in range(len(listUser)):
#     for j in range(len(listProduct)):
#         if user_matrix[i][j] > 0:
#             user_matrix[i][j] -= avg_rating[i]

# Tính độ tương đồng cosine giữa các người dùng
user_similarity = cosine_similarity(user_matrix)


def predict_ratings(user_similarity, ratings):
    mean_user_rating = ratings.mean(axis=1)
    ratings_diff = (ratings - mean_user_rating[:, np.newaxis])
    pred = mean_user_rating[:, np.newaxis] + user_similarity.dot(ratings_diff) / np.array([np.abs(user_similarity).sum(axis=1)]).T
    return pred

predicted_ratings = predict_ratings(user_similarity, user_matrix)

def recommend_products(user_id, predicted_ratings, num_recommendations=5):
    # Lấy xếp hạng dự đoán cho người dùng
    user_ratings = predicted_ratings[user_id]
    
    # Sắp xếp các sản phẩm theo xếp hạng dự đoán
    sorted_product_ids = np.argsort(user_ratings)
    
    # Lấy ID của các sản phẩm được đề xuất
    recommended_product_ids = sorted_product_ids[-num_recommendations:]
    
    return recommended_product_ids

# ID của người dùng
user_id = 10

# Lấy các sản phẩm được đề xuất
recommended_product_ids = recommend_products(user_id, predicted_ratings)

print("Sản phẩm được đề xuất cho người dùng {}: {}".format(user_id, recommended_product_ids))
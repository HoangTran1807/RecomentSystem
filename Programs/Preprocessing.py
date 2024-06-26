import pyodbc
import json 
import re
from underthesea import word_tokenize
import unidecode
import time

# Đọc file stopwords
with open("./data/vietnamese-stopwords.txt", encoding='utf-8') as f:
    stopwords = f.readlines()

# tiền xử lý dữ liệu cho oldDesc tách html và loại bỏ stopword
def preprocessingDesc(oldDesc):
    # Loại bỏ html bằng regex
    newDesc = re.sub('<[^>]*>', '', oldDesc)
    # Tách từ bằng thư viện underthesea
    words = word_tokenize(newDesc, format="text")
    # Loại bỏ stopword
    filtered_words = [word for word in words.split() if word not in stopwords]
    # Ghép lại thành chuỗi
    result = ' '.join(filtered_words)
    return result

def preprocessing_text(text):
    # Loại bỏ html bằng regex
    text = re.sub('<[^>]*>', ' ', text)
    text = text.lower()

    # Loại bỏ các ký tự Unicode không mong muốn
    text = unidecode.unidecode(text)
    # Tách từ bằng thư viện underthesea
    text = word_tokenize(text, format="text")

    # Loại bỏ dấu chấm câu và khoảng trắng thừa
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)


    # Loại bỏ các ký tự còn sót lại
    text = re.sub(r"[^\w ]", "", text)

    # Loại bỏ stopword
    filtered_words = [word for word in text.split() if word not in stopwords]
    # Ghép lại thành chuỗi
    result = ' '.join(filtered_words)
    return result





# Xử lý dữ liệu cho table_html tách html và chuyển thành json
# def process_table_html(table_html):
#     # Parse the HTML with BeautifulSoup
#     soup = BeautifulSoup(table_html, 'html.parser')
#     # Find all table rows
#     rows = soup.find_all('tr')
#     # Create a dictionary to hold the data
#     data = {}
#     # Loop through each row
#     print(rows)
#     for row in rows:
#         # Get the label (key) and value from the row
#         key = ' '.join(row.find('th', class_='table-label').text.split())
#         value = ' '.join(row.find('td').text.split())
#         # Preprocess the value
#         value = preprocessingDesc(value)
#         # Add the key-value pair to the dictionary
#         data[key] = value
#     # Convert the dictionary to a JSON string
#     json_data = json.dumps(data, ensure_ascii=False)

#     return json_data

# nếu dữ liệu đầu vào (rating) bằng null thì gán giá trị là 3
# 3 là giá trị trung bình của rating nếu rating = 0 sản phẩm có thể
# bị underated
def check_rating(rating):
    if rating == None:
        return 3
    return rating

def convert_categories(categories):
    return categories.split(',')


try:
    start_time = time.time()
    # Kết nối đến cơ sở dữ liệu SQL Server
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-38TO487\SQLEXPRESS;DATABASE=Fahasa;UID=Hoang;PWD=123')
    cursor = conn.cursor()

    # Truy vấn để lấy dữ liệu từ bảng product
    cursor.execute('''
    SELECT 
        p.[Id], 
        p.[Name], 
        p.[AuthorId], 
        p.[SupplierId], 
        p.[Desc], 
        AVG(c.[Rating]) as AverageRating,
        STRING_AGG(pc.[CategoryId], ',') WITHIN GROUP (ORDER BY pc.[CategoryId]) as Categories
    FROM 
        product p
    LEFT JOIN 
        comment c ON p.[Id] = c.[ProductId]
    LEFT JOIN 
        ProductCategory pc ON p.[Id] = pc.[ProductId]
    GROUP BY 
        p.[Id], 
        p.[Name], 
        p.[AuthorId], 
        p.[SupplierId], 
        p.[Desc]
''')
    rows = cursor.fetchall()

    # Chuyển dữ liệu đã lấy được thành dạng JSON
    data = []
    # shinkRows = rows[:100]
    for row in rows:
        processed_desc = preprocessingDesc(row[4])
        rating = check_rating(row[5])
        categories = convert_categories(row[6])
        #preprocess_html = process_table_html(row[5])
        data.append({
            'Id': row[0],
            'Name': row[1],
            'AuthorId': row[2],
            'SupplierId': row[3],
            'Desc': processed_desc,
            #'Table':preprocess_html,
            'AverageRating': rating,
            'CategoryId': categories
        })
except Exception as e:
    print(f"Loi : {e}")

    
# Ghi dữ liệu JSON vào file
with open('product_data2.json', 'w') as f:
    json.dump(data, f)

# Đóng kết nối với cơ sở dữ liệu
conn.close()

end_time = time.time()
print(f"Thời gian chạy: {end_time - start_time} giây")
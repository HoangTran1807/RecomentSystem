import time
import pyodbc
import json


try:
    start_time = time.time()
    # Kết nối đến cơ sở dữ liệu SQL Server
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-38TO487\SQLEXPRESS;DATABASE=Fahasa;UID=Hoang;PWD=123')
    cursor = conn.cursor()

    # Truy vấn để lấy dữ liệu từ bảng product
    cursor.execute('''
    select p.id, p.Name, p.Birth, p.Gender from people as p 
''')
    rows = cursor.fetchall()

    # Chuyển dữ liệu đã lấy được thành dạng JSON
    data = []
    # shinkRows = rows[:100]
    for row in rows:
        #preprocess_html = process_table_html(row[5])
        data.append({
            'Id': row[0],
            'Name': row[1],
            'Birth': row[2],
            'Gender': row[3]
        })
except Exception as e:
    print(f"Loi : {e}")


# Ghi dữ liệu JSON vào file
with open('userData.json', 'w') as f:
    json.dump(data, f)

# Đóng kết nối với cơ sở dữ liệu
conn.close()

end_time = time.time()
print(f"Thời gian chạy: {end_time - start_time} giây")
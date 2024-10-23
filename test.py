import json

# Đọc dữ liệu từ file data_copy.json
with open('data1_copy.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Tạo một tập hợp để lưu trữ các cặp (name, big_category) đã xuất hiện
unique_books = set()

# Danh sách lưu trữ các mục duy nhất
unique_data = []

# Duyệt qua các mục và loại bỏ các mục trùng lặp dựa trên name và big_category
for item in data:
    # Tạo một tuple từ name và big_category
    book_key = (item["name"], tuple(item["small_category"]))
    
    # Nếu chưa tồn tại trong tập hợp, thêm vào danh sách và đánh dấu là đã xuất hiện
    if book_key not in unique_books:
        unique_books.add(book_key)
        unique_data.append(item)

# Lưu kết quả vào file output.json
with open('output.json', 'w', encoding='utf-8') as file:
    json.dump(unique_data, file, ensure_ascii=False, indent=4)

print("Dữ liệu đã được lọc và lưu vào output.json")

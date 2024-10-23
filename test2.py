import json

# Đọc dữ liệu từ file data_copy.json
with open('output.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Dictionary để lưu các phần tử theo 'name'
combined_books = {}

# Duyệt qua các mục và kết hợp big_category và small_category nếu cùng name
for item in data:
    name = item["name"]
    
    if name in combined_books:
        # Nếu đã có sách với cùng tên, kết hợp big_category và small_category
        combined_books[name]["big_category"] = list(set(combined_books[name]["big_category"] + item["big_category"]))
        combined_books[name]["small_category"] = list(set(combined_books[name]["small_category"] + item["small_category"]))
    else:
        # Nếu chưa có sách với tên này, thêm vào dictionary
        combined_books[name] = item

# Chuyển đổi dictionary thành list
result = list(combined_books.values())

# Lưu kết quả vào file output.json
with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(result, file, ensure_ascii=False, indent=4)

print("Dữ liệu đã được xử lý và lưu vào output.json")

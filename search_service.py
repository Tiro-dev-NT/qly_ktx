import data_manager as dm
def sort_students_by_name(students: list) -> list:
    """
    Sắp xếp danh sách sinh viên theo tên bằng thuật toán Merge Sort
    Không làm thay đổi danh sách gốc mà trả về một danh sách mới
    """
    # Điều kiện dừng của đệ quy: nếu list có 1 hoặc 0 phần tử thì đã được "sắp xếp"
    if len(students) <= 1:
        return students

    # 1. Chia đôi danh sách
    mid = len(students) // 2
    left_half = students[:mid]
    right_half = students[mid:]

    # 2. Gọi đệ quy để sắp xếp từng nửa
    left_sorted = sort_students_by_name(left_half)
    right_sorted = sort_students_by_name(right_half)

    # 3. Trộn (Merge) 2 mảng đã sắp xếp lại với nhau
    return _merge_student_lists(left_sorted, right_sorted)


def _merge_student_lists(left: list, right: list) -> list:
    """
    Hàm phụ trợ để trộn 2 danh sách sinh viên đã sắp xếp.
    """
    merged = []
    i = 0  # Chỉ số duyệt mảng left
    j = 0  # Chỉ số duyệt mảng right

    while i < len(left) and j < len(right):
        # Lấy full_name và gọi hàm tách tên để so sánh (đã lower)
        name_left = _get_vietnamese_sort_key(left[i].full_name)
        name_right = _get_vietnamese_sort_key(right[j].full_name)

        if name_left <= name_right:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Đưa các phần tử còn sót lại (nếu có) của mảng left vào
    while i < len(left):
        merged.append(left[i])
        i += 1

    # Đưa các phần tử còn sót lại (nếu có) của mảng right vào
    while j < len(right):
        merged.append(right[j])
        j += 1

    return merged


def _get_vietnamese_sort_key(full_name: str) -> tuple:
    """
    Hàm phụ trợ xử lý chuỗi tiếng Việt: chuyển thành chữ thường (.lower())
    và tách tên riêng để ưu tiên sắp xếp trước họ và tên đệm.
    
    Ví dụ: "Nguyễn Văn Anh" -> ("anh", "nguyễn văn")
    """
    if not full_name:
        return ("", "")
        
    # Chuyển chuỗi về chữ thường như yêu cầu trong plan
    parts = full_name.lower().strip().split()
    
    if not parts:
        return ("", "")
    
    # Từ cuối cùng là Tên, các từ phía trước là Họ và tên đệm
    ten = parts[-1]
    ho_dem = " ".join(parts[:-1])
    
    # Trả về tuple: Python sẽ tự động so sánh 'ten' trước, 
    # nếu 'ten' giống nhau thì sẽ so sánh tiếp 'ho_dem'
    return (ten, ho_dem)

def _insertion_sort_room_by_price(rooms: list) -> list:
    """Sắp xếp phòng theo giá tăng dần — Insertion Sort"""
    for i in range(1, len(rooms)):
        key = rooms[i]
        j = i - 1
        while j >= 0 and rooms[j].price_per_month > key.price_per_month:
            rooms[j + 1] = rooms[j]
            j -= 1
        rooms[j + 1] = key
    return rooms
def _insertion_sort_rooms_by_id(rooms: list) -> list:
    """Sắp xếp phòng theo room_id tăng dần — Insertion Sort (dùng trước binary search)"""
    for i in range(1, len(rooms)):
        key = rooms[i]
        j = i - 1
        while j >= 0 and rooms[j].room_id > key.room_id:
            rooms[j + 1] = rooms[j]
            j -= 1
        rooms[j + 1] = key
    return rooms

def _binary_search_room(sorted_rooms, room_id):
    """Tìm phòng theo room_id trên mảng đã sắp xếp theo room_id"""
    left = 0
    right = len(sorted_rooms) - 1
    while left <= right:
        mid = (left + right) // 2
        if sorted_rooms[mid].room_id == room_id:
            return sorted_rooms[mid]
        elif sorted_rooms[mid].room_id < room_id:
            left = mid + 1
        else:
            right = mid - 1
    return None

def search_room_by_id(room_id):
    dm._ensure_data_loaded()
    sorted_rooms = _insertion_sort_rooms_by_id(dm.ALL_ROOMS[:])
    return _binary_search_room(sorted_rooms, room_id)

def search_room_by_type_or_status(query):
    dm._ensure_data_loaded()
    key = str(query).strip().lower()
    lst = []
    for room in dm.ALL_ROOMS:
        if str(room.room_type) == key or room.status.lower() == key:
            lst.append(room)
    return lst



def _bubble_sort_bills_by_amount(bills: list) -> list:
    n = len(bills)
    for i in range(n):
        for j in range(0, n - i - 1):
            if bills[j].total_amount < bills[j + 1].total_amount:
                bills[j], bills[j + 1] = bills[j + 1], bills[j]
    return bills

TABLE_SIZE = 100

def _hash_function(key: str) -> int:
    return sum(ord(c) for c in key) % TABLE_SIZE

def _hash_table_build(students: list) -> list:
    table = [None] * TABLE_SIZE
    for student in students:
        index = _hash_function(student.student_id)
        while table[index] is not None:
            index = (index + 1) % TABLE_SIZE
        table[index] = student
    return table

def _hash_table_lookup(table: list, student_id: str):
    index = _hash_function(student_id)
    start_index = index
    while table[index] is not None:
        if table[index].student_id == student_id:
            return table[index]
        index = (index + 1) % TABLE_SIZE
        if index == start_index:
            break
    return None

def search_student_by_id(student_id: str):
    table = _hash_table_build(dm.ALL_STUDENTS)
    return _hash_table_lookup(table, student_id)

def search_student_by_name(name_query: str) -> list:
    result = []
    query = name_query.lower()
    for student in dm.ALL_STUDENTS:
        if query in student.full_name.lower():
            result.append(student)
    return result   

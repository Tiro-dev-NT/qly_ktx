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

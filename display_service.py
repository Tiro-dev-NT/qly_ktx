def display_success(message: str):
    print(f"\n[THÀNH CÔNG] {message}")

def display_error(message: str):
    print(f"\n[LỖI] {message}")

def display_not_found(entity_name: str):
    print(f"\n[THÔNG BÁO] Không tìm thấy {entity_name}.")

def display_room_list(rooms: list, title="DANH SÁCH PHÒNG"):
    print(f"\n=== {title} ===")
    print(f"{'Mã Phòng':<10} | {'Loại':<5} | {'Giá/Tháng':<10} | {'Sức chứa':<10} | {'Đang ở':<8} | {'Trạng thái':<15}")
    print("-" * 65)
    if not rooms:
        print("Không có dữ liệu phòng.")
        return
    for r in rooms:
        print(f"{r.room_id:<10} | {r.room_type:<5} | {r.price_per_month:<10} | {r.capacity:<10} | {r.current_occupants:<8} | {r.status:<15}")

def display_student_list(students: list, title="DANH SÁCH SINH VIÊN"):
    print(f"\n=== {title} ===")
    print(f"{'MSSV':<10} | {'Họ Tên':<20} | {'Lớp':<10} | {'SĐT':<12} | {'Diện KS':<10}")
    print("-" * 65)
    if not students:
        print("Không có dữ liệu sinh viên.")
        return
    for s in students:
        print(f"{s.student_id:<10} | {s.full_name:<20} | {s.class_name:<10} | {s.phone:<12} | {s.policy_type:<10}")

def display_contract_details(contract):
    print("\n=== CHI TIẾT HỢP ĐỒNG ===")
    print(f"Mã hợp đồng : {contract.contract_id}")
    print(f"Mã sinh viên: {contract.student_id}")
    print(f"Mã phòng    : {contract.room_id}")
    print(f"Ngày bắt đầu: {contract.start_date}")
    print(f"Ngày kết thúc: {contract.end_date}")
    print(f"Trạng thái  : {contract.status}")

def display_service_bill(bill):
    print("\n=== CHI TIẾT HÓA ĐƠN DỊCH VỤ ===")
    print(f"Mã hóa đơn  : {bill.bill_id}")
    print(f"Mã phòng    : {bill.room_id}")
    print(f"Tháng/Năm   : {bill.month}/{bill.year}")
    print(f"Số điện dùng: {bill.electric_end - bill.electric_start} kWh -> {bill.electric_amount:,.0f} VNĐ")
    print(f"Số nước dùng: {bill.water_end - bill.water_start} m3 -> {bill.water_amount:,.0f} VNĐ")
    print(f"Tổng tiền   : {bill.total_amount:,.0f} VNĐ")
    print(f"Trạng thái  : {bill.status.upper()}")
    print(f"Hạn nộp     : {bill.due_date}")

def display_bill_list(bills: list, title="DANH SÁCH HÓA ĐƠN"):
    print(f"\n=== {title} ===")
    print(f"{'Mã HĐ':<15} | {'Phòng':<8} | {'Tháng':<7} | {'Tổng tiền':<12} | {'Trạng thái':<10}")
    print("-" * 60)
    if not bills:
        print("Không có dữ liệu hóa đơn.")
        return
    for b in bills:
        print(f"{b.bill_id:<15} | {b.room_id:<8} | {f'{b.month}/{b.year}':<7} | {b.total_amount:<12,.0f} | {b.status:<10}")

def display_report_overdue(data: list):
    print("\n=== BÁO CÁO SINH VIÊN NỢ PHÍ QUÁ HẠN ===")
    print(f"{'MSSV':<10} | {'Họ Tên':<20} | {'Phòng':<8} | {'Tổng nợ':<12} | {'Hạn nộp':<12}")
    print("-" * 68)
    if not data:
        print("Không có sinh viên nợ phí quá hạn.")
        return
    for d in data:
        print(f"{d['student_id']:<10} | {d['full_name']:<20} | {d['room_id']:<8} | {d['total_amount']:<12,.0f} | {d['due_date']:<12}")

def display_report_occupancy(data: list):
    print("\n=== BÁO CÁO TỈ LỆ LẤP ĐẦY PHÒNG ===")
    print(f"{'Loại phòng':<15} | {'Tỉ lệ lấp đầy (%)':<20}")
    print("-" * 40)
    if not data:
        print("Không có dữ liệu thống kê.")
        return
    for d in data:
        print(f"Phòng {d['room_type']:<9} giường | {d['occupancy_rate']}%")
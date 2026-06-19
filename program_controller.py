import sys
import contract_manager
import data_manager as dm
import room_manager
import student_manager
import display_service
import search_service
import service_fee_calculator
import report_service

class AppController:
    def __init__(self):
        dm.load_all_data_once()

    def display_main_menu(self):
        print("\n" + "="*45)
        print("     HỆ THỐNG QUẢN LÝ KÝ TÚC XÁ")
        print("="*45)
        print("1. Quản lý phòng")
        print("2. Quản lý sinh viên")
        print("3. Quản lý hợp đồng")
        print("4. Quản lý thu phí dịch vụ (điện, nước)")
        print("5. Tra cứu và tìm kiếm")
        print("6. Báo cáo thống kê")
        print("0. Thoát chương trình")
        print("="*45)

    def handle_choices(self):
        while True:
            self.display_main_menu()
            choice = input("Vui lòng chọn chức năng (0-6): ").strip()

            if choice == '1':
                self.handle_room_menu()
            elif choice == '2':
                self.handle_student_menu()
            elif choice == '3':
                self.handle_contract_menu()
            elif choice == '4':
                self.handle_service_menu()
            elif choice == '5':
                self.handle_search_menu()
            elif choice == '6':
                self.handle_report_menu()
            elif choice == '0':
                print("Cảm ơn bạn đã sử dụng hệ thống. Tạm biệt!")
                sys.exit(0)
            else:
                print("Lỗi: Lựa chọn không hợp lệ. Vui lòng nhập số từ 0 đến 6.")

    # ─────────────────────────────────────────
    # Chức năng 1: Quản lý phòng
    # ─────────────────────────────────────────
    def handle_room_menu(self):
        """Vòng lặp menu quản lý phòng."""
        while True:
            print("\n=== QUẢN LÝ THÔNG TIN PHÒNG ===")
            print("1. Xem danh sách toàn bộ phòng")
            print("2. Thêm phòng mới")
            print("3. Cập nhật thông tin phòng")
            print("4. Xóa phòng")
            print("0. Quay lại menu chính")

            choice = input("Nhập lựa chọn của bạn: ").strip()

            if choice == "1":
                self.handle_view_all_rooms()
            elif choice == "2":
                self.handle_add_room()
            elif choice == "3":
                self.handle_update_room()
            elif choice == "4":
                self.handle_delete_room()
            elif choice == "0":
                break
            else:
                print("[Lỗi] Lựa chọn không hợp lệ. Vui lòng nhập lại!")

    def handle_view_all_rooms(self):
        """Hiển thị danh sách toàn bộ phòng."""
        lst_room = room_manager.get_all_rooms()
        if not lst_room:
            display_service.display_not_found("phòng nào")
            return
        display_service.display_room_list(lst_room, title="DANH SÁCH TOÀN BỘ PHÒNG")

    def handle_add_room(self):
        """Thêm phòng mới vào hệ thống."""
        print("\n--- THÊM PHÒNG MỚI ---")
        room_id = input("Nhập mã phòng (VD: P101): ").strip()
        if not room_id:
            display_service.display_error("Mã phòng không được để trống.")
            return

        try:
            room_type = int(input("Nhập loại phòng (số giường: 4/6/8): ").strip())
            if room_type not in [4, 6, 8]:
                display_service.display_error("Loại phòng phải là 4, 6 hoặc 8.")
                return
        except ValueError:
            display_service.display_error("Loại phòng phải là số nguyên.")
            return

        try:
            price = float(input("Nhập giá thuê/tháng (VNĐ): ").strip())
            if price <= 0:
                display_service.display_error("Giá thuê phải lớn hơn 0.")
                return
        except ValueError:
            display_service.display_error("Giá thuê phải là số.")
            return

        try:
            capacity = int(input("Nhập sức chứa tối đa (số người): ").strip())
            if capacity <= 0:
                display_service.display_error("Sức chứa phải lớn hơn 0.")
                return
        except ValueError:
            display_service.display_error("Sức chứa phải là số nguyên.")
            return

        try:
            floor = int(input("Nhập tầng: ").strip())
        except ValueError:
            display_service.display_error("Tầng phải là số nguyên.")
            return

        building = input("Nhập tòa nhà (VD: A, B, C): ").strip().upper()
        if not building:
            display_service.display_error("Tòa nhà không được để trống.")
            return

        ok = room_manager.add_room(room_id, room_type, price, capacity, floor, building)
        if ok:
            display_service.display_success(f"Đã thêm phòng {room_id} vào hệ thống.")
        else:
            display_service.display_error(f"Mã phòng '{room_id}' đã tồn tại trong hệ thống.")

    def handle_update_room(self):
        """Cập nhật thông tin một phòng theo mã."""
        print("\n--- CẬP NHẬT THÔNG TIN PHÒNG ---")
        room_id = input("Nhập mã phòng cần cập nhật: ").strip()
        room = room_manager.get_room_by_id(room_id)
        if not room:
            display_service.display_not_found(f"phòng '{room_id}'")
            return

        display_service.display_room_list([room], title=f"THÔNG TIN HIỆN TẠI — PHÒNG {room_id}")

        print("\nChọn trường cần cập nhật:")
        print("1. Giá thuê/tháng")
        print("2. Trạng thái (available/full/maintenance)")
        print("3. Tầng")
        print("4. Tòa nhà")
        print("0. Hủy")

        field_choice = input("Lựa chọn: ").strip()

        if field_choice == '1':
            try:
                new_price = float(input("Nhập giá thuê mới (VNĐ): ").strip())
                if new_price <= 0:
                    display_service.display_error("Giá phải lớn hơn 0.")
                    return
                room_manager.update_room(room_id, price_per_month=new_price)
                display_service.display_success(f"Đã cập nhật giá phòng {room_id}.")
            except ValueError:
                display_service.display_error("Giá thuê phải là số.")
        elif field_choice == '2':
            new_status = input("Nhập trạng thái mới (available/full/maintenance): ").strip().lower()
            if new_status not in ["available", "full", "maintenance"]:
                display_service.display_error("Trạng thái không hợp lệ.")
                return
            room_manager.update_room(room_id, status=new_status)
            display_service.display_success(f"Đã cập nhật trạng thái phòng {room_id}.")
        elif field_choice == '3':
            try:
                new_floor = int(input("Nhập tầng mới: ").strip())
                room_manager.update_room(room_id, floor=new_floor)
                display_service.display_success(f"Đã cập nhật tầng phòng {room_id}.")
            except ValueError:
                display_service.display_error("Tầng phải là số nguyên.")
        elif field_choice == '4':
            new_building = input("Nhập tòa nhà mới: ").strip().upper()
            if not new_building:
                display_service.display_error("Tòa nhà không được để trống.")
                return
            room_manager.update_room(room_id, building=new_building)
            display_service.display_success(f"Đã cập nhật tòa nhà phòng {room_id}.")
        elif field_choice == '0':
            print("Đã hủy thao tác.")
        else:
            display_service.display_error("Lựa chọn không hợp lệ.")

    def handle_delete_room(self):
        """Xóa phòng (chỉ khi không còn hợp đồng active)."""
        print("\n--- XÓA PHÒNG ---")
        room_id = input("Nhập mã phòng cần xóa: ").strip()
        room = room_manager.get_room_by_id(room_id)
        if not room:
            display_service.display_not_found(f"phòng '{room_id}'")
            return

        for contract in dm.ALL_CONTRACTS:
            if contract.room_id == room_id and contract.is_active():
                display_service.display_error(
                    f"Không thể xóa phòng {room_id} vì đang có hợp đồng active.")
                return

        display_service.display_room_list([room], title="THÔNG TIN PHÒNG CẦN XÓA")
        confirm = input(f"Bạn có chắc chắn muốn xóa phòng {room_id}? (y/n): ").strip().lower()
        if confirm == 'y':
            room_manager.delete_room(room_id)
            display_service.display_success(f"Đã xóa phòng {room_id} khỏi hệ thống.")
        else:
            print("Đã hủy thao tác xóa.")

    # ─────────────────────────────────────────
    # Chức năng 2: Quản lý sinh viên
    # ─────────────────────────────────────────
    def handle_student_menu(self):
        """Vòng lặp menu quản lý sinh viên."""
        while True:
            print("\n=== QUẢN LÝ SINH VIÊN ===")
            print("1. Xem danh sách toàn bộ sinh viên")
            print("2. Thêm sinh viên mới")
            print("3. Cập nhật thông tin sinh viên")
            print("4. Xóa sinh viên")
            print("0. Quay lại menu chính")

            choice = input("Nhập lựa chọn của bạn: ").strip()

            if choice == "1":
                self.handle_view_all_students()
            elif choice == "2":
                self.handle_add_student()
            elif choice == "3":
                self.handle_update_student()
            elif choice == "4":
                self.handle_delete_student()
            elif choice == "0":
                break
            else:
                print("[Lỗi] Lựa chọn không hợp lệ. Vui lòng nhập lại!")

    def handle_view_all_students(self):
        """Hiển thị danh sách sinh viên đã sắp xếp theo tên (Merge Sort)."""
        lst = student_manager.get_all_students()
        if not lst:
            display_service.display_not_found("sinh viên nào")
            return
        sorted_lst = search_service.sort_students_by_name(lst)
        display_service.display_student_list(sorted_lst, title="DANH SÁCH TOÀN BỘ SINH VIÊN")

    def handle_add_student(self):
        """Thêm sinh viên mới vào hệ thống."""
        print("\n--- THÊM SINH VIÊN MỚI ---")
        student_id = input("Nhập mã sinh viên (VD: SV001): ").strip()
        if not student_id:
            display_service.display_error("Mã sinh viên không được để trống.")
            return

        full_name = input("Nhập họ tên đầy đủ: ").strip()
        if not full_name:
            display_service.display_error("Họ tên không được để trống.")
            return

        class_name = input("Nhập tên lớp (VD: IT-01): ").strip()
        phone = input("Nhập số điện thoại: ").strip()
        email = input("Nhập email: ").strip()

        print("Diện chính sách: 1. Ưu tiên (priority)  2. Bình thường (normal)")
        policy_choice = input("Chọn diện (1/2): ").strip()
        if policy_choice == '1':
            policy_type = "priority"
        elif policy_choice == '2':
            policy_type = "normal"
        else:
            display_service.display_error("Diện chính sách không hợp lệ.")
            return

        ok = student_manager.add_student(student_id, full_name, class_name, phone, email, policy_type)
        if ok:
            display_service.display_success(f"Đã thêm sinh viên {student_id} — {full_name}.")
        else:
            display_service.display_error(f"Mã sinh viên '{student_id}' đã tồn tại.")

    def handle_update_student(self):
        """Cập nhật thông tin một sinh viên theo mã."""
        print("\n--- CẬP NHẬT THÔNG TIN SINH VIÊN ---")
        student_id = input("Nhập mã sinh viên cần cập nhật: ").strip()
        student = student_manager.get_student_by_id(student_id)
        if not student:
            display_service.display_not_found(f"sinh viên '{student_id}'")
            return

        display_service.display_student_list([student], title=f"THÔNG TIN HIỆN TẠI — SINH VIÊN {student_id}")

        print("\nChọn trường cần cập nhật:")
        print("1. Họ tên")
        print("2. Lớp")
        print("3. Số điện thoại")
        print("4. Email")
        print("5. Diện chính sách")
        print("0. Hủy")

        field_choice = input("Lựa chọn: ").strip()

        if field_choice == '1':
            new_name = input("Nhập họ tên mới: ").strip()
            if not new_name:
                display_service.display_error("Họ tên không được để trống.")
                return
            student_manager.update_student(student_id, full_name=new_name)
            display_service.display_success("Đã cập nhật họ tên.")
        elif field_choice == '2':
            new_class = input("Nhập tên lớp mới: ").strip()
            student_manager.update_student(student_id, class_name=new_class)
            display_service.display_success("Đã cập nhật lớp.")
        elif field_choice == '3':
            new_phone = input("Nhập số điện thoại mới: ").strip()
            student_manager.update_student(student_id, phone=new_phone)
            display_service.display_success("Đã cập nhật số điện thoại.")
        elif field_choice == '4':
            new_email = input("Nhập email mới: ").strip()
            student_manager.update_student(student_id, email=new_email)
            display_service.display_success("Đã cập nhật email.")
        elif field_choice == '5':
            print("Diện chính sách: 1. Ưu tiên (priority)  2. Bình thường (normal)")
            policy_choice = input("Chọn diện (1/2): ").strip()
            if policy_choice == '1':
                student_manager.update_student(student_id, policy_type="priority")
            elif policy_choice == '2':
                student_manager.update_student(student_id, policy_type="normal")
            else:
                display_service.display_error("Diện không hợp lệ.")
                return
            display_service.display_success("Đã cập nhật diện chính sách.")
        elif field_choice == '0':
            print("Đã hủy thao tác.")
        else:
            display_service.display_error("Lựa chọn không hợp lệ.")

    def handle_delete_student(self):
        """Xóa sinh viên (chỉ khi không còn hợp đồng active)."""
        print("\n--- XÓA SINH VIÊN ---")
        student_id = input("Nhập mã sinh viên cần xóa: ").strip()
        student = student_manager.get_student_by_id(student_id)
        if not student:
            display_service.display_not_found(f"sinh viên '{student_id}'")
            return

        if student_manager.has_active_contract(student_id):
            display_service.display_error(
                f"Không thể xóa sinh viên {student_id} vì đang có hợp đồng active.")
            return

        display_service.display_student_list([student], title="THÔNG TIN SINH VIÊN CẦN XÓA")
        confirm = input(f"Bạn có chắc chắn muốn xóa sinh viên {student_id}? (y/n): ").strip().lower()
        if confirm == 'y':
            student_manager.delete_student(student_id)
            display_service.display_success(f"Đã xóa sinh viên {student_id} khỏi hệ thống.")
        else:
            print("Đã hủy thao tác xóa.")

    # ─────────────────────────────────────────
    # Chức năng 3: Quản lý hợp đồng
    # ─────────────────────────────────────────
    def handle_contract_menu(self):
        """Vòng lặp menu quản lý hợp đồng."""
        while True:
            print("\n--- 3. QUẢN LÝ HỢP ĐỒNG ---")
            print("1. Đăng ký phòng mới")
            print("2. Gia hạn hợp đồng")
            print("3. Chuyển phòng")
            print("4. Thanh lý hợp đồng")
            print("0. Quay lại menu chính")

            choice = input("Chọn chức năng (0-4): ").strip()
            if choice == '1':
                self.handle_register_room()
            elif choice == '2':
                self.handle_extend_contract()
            elif choice == '3':
                self.handle_transfer_room()
            elif choice == '4':
                self.handle_terminate_contract()
            elif choice == '0':
                break
            else:
                print("Lỗi: Lựa chọn không hợp lệ. Vui lòng chọn từ 0 đến 4.")

    def handle_register_room(self):
        """Đăng ký thuê phòng mới cho sinh viên."""
        print("\n-- ĐĂNG KÝ PHÒNG --")
        student_id = input("Nhập mã sinh viên: ").strip()
        room_id = input("Nhập mã phòng: ").strip()
        start_date = input("Nhập ngày bắt đầu (YYYY-MM-DD): ").strip()
        end_date = input("Nhập ngày kết thúc (YYYY-MM-DD): ").strip()
        contract_manager.register_room(student_id, room_id, start_date, end_date)

    def handle_extend_contract(self):
        """Gia hạn hợp đồng đang active."""
        print("\n-- GIA HẠN HỢP ĐỒNG --")
        contract_id = input("Nhập mã hợp đồng cần gia hạn: ").strip()
        new_end_date = input("Nhập ngày kết thúc mới (YYYY-MM-DD): ").strip()
        contract_manager.extend_contract(contract_id, new_end_date)

    def handle_transfer_room(self):
        """Chuyển sinh viên sang phòng khác."""
        print("\n-- CHUYỂN PHÒNG --")
        contract_id = input("Nhập mã hợp đồng: ").strip()
        new_room_id = input("Nhập mã phòng mới muốn chuyển tới: ").strip()
        contract_manager.transfer_room(contract_id, new_room_id)

    def handle_terminate_contract(self):
        """Thanh lý hợp đồng."""
        print("\n-- THANH LÝ HỢP ĐỒNG --")
        contract_id = input("Nhập mã hợp đồng cần thanh lý: ").strip()
        confirm = input(f"Bạn có chắc chắn muốn thanh lý hợp đồng {contract_id}? (y/n): ").strip().lower()
        if confirm == 'y':
            contract_manager.terminate_contract(contract_id)
        else:
            print("Đã hủy thao tác thanh lý.")

    # ─────────────────────────────────────────
    # Chức năng 4: Phí dịch vụ
    # ─────────────────────────────────────────
    def handle_service_menu(self):
        """Vòng lặp menu quản lý phí dịch vụ."""
        while True:
            print("\n=== QUẢN LÝ PHÍ DỊCH VỤ (ĐIỆN, NƯỚC) ===")
            print("1. Nhập chỉ số điện/nước hàng tháng")
            print("2. Thanh toán hóa đơn")
            print("3. Xem lịch sử hóa đơn theo phòng")
            print("0. Quay lại menu chính")

            choice = input("Nhập lựa chọn: ").strip()
            if choice == '1':
                self.handle_record_usage()
            elif choice == '2':
                self.handle_pay_bill()
            elif choice == '3':
                self.handle_view_bills()
            elif choice == '0':
                break
            else:
                print("[Lỗi] Lựa chọn không hợp lệ.")

    def handle_record_usage(self):
        """Ghi nhận chỉ số điện/nước và tạo hóa đơn tháng."""
        print("\n--- NHẬP CHỈ SỐ ĐIỆN/NƯỚC ---")
        room_id = input("Nhập mã phòng: ").strip()

        try:
            month = int(input("Nhập tháng (1-12): ").strip())
            year = int(input("Nhập năm (VD: 2025): ").strip())
            e_start = int(input("Chỉ số điện đầu kỳ (kWh): ").strip())
            e_end = int(input("Chỉ số điện cuối kỳ (kWh): ").strip())
            w_start = int(input("Chỉ số nước đầu kỳ (m³): ").strip())
            w_end = int(input("Chỉ số nước cuối kỳ (m³): ").strip())
        except ValueError:
            display_service.display_error("Vui lòng nhập số nguyên hợp lệ.")
            return

        ok = service_fee_calculator.record_monthly_usage(
            room_id, month, year, e_start, e_end, w_start, w_end)
        if ok:
            display_service.display_success(
                f"Đã ghi nhận chỉ số điện/nước tháng {month}/{year} cho phòng {room_id}.")
            bills = service_fee_calculator.get_bills_by_room(room_id, month, year)
            if bills:
                display_service.display_service_bill(bills[-1])
        else:
            display_service.display_error(
                f"Không thể ghi nhận. Kiểm tra: phòng tồn tại, có hợp đồng active, "
                f"chưa có hóa đơn tháng {month}/{year}, và chỉ số cuối >= đầu.")

    def handle_pay_bill(self):
        """Thanh toán một hóa đơn theo mã."""
        print("\n--- THANH TOÁN HÓA ĐƠN ---")
        bill_id = input("Nhập mã hóa đơn cần thanh toán: ").strip()
        ok = service_fee_calculator.pay_bill(bill_id)
        if ok:
            display_service.display_success(f"Đã thanh toán hóa đơn {bill_id}.")
        else:
            display_service.display_error(
                f"Không tìm thấy hóa đơn '{bill_id}' hoặc hóa đơn đã được thanh toán.")

    def handle_view_bills(self):
        """Xem lịch sử hóa đơn của một phòng (có thể lọc theo tháng/năm)."""
        print("\n--- XEM LỊCH SỬ HÓA ĐƠN ---")
        room_id = input("Nhập mã phòng: ").strip()
        month_input = input("Nhập tháng cần xem (bỏ trống = tất cả): ").strip()
        year_input = input("Nhập năm cần xem  (bỏ trống = tất cả): ").strip()

        try:
            month = int(month_input) if month_input else None
            year = int(year_input) if year_input else None
        except ValueError:
            display_service.display_error("Tháng/năm phải là số nguyên.")
            return

        bills = service_fee_calculator.get_bills_by_room(room_id, month, year)
        if not bills:
            display_service.display_not_found(f"hóa đơn nào cho phòng '{room_id}'")
            return

        sorted_bills = search_service._bubble_sort_bills_by_amount(bills[:])
        display_service.display_bill_list(sorted_bills, title=f"LỊCH SỬ HÓA ĐƠN PHÒNG {room_id}")

    # ─────────────────────────────────────────
    # Chức năng 5: Tìm kiếm
    # ─────────────────────────────────────────
    def handle_search_menu(self):
        """Vòng lặp menu tìm kiếm."""
        while True:
            print("\n=== TRA CỨU VÀ TÌM KIẾM ===")
            print("1. Tìm kiếm phòng")
            print("2. Tìm kiếm sinh viên")
            print("0. Quay lại menu chính")

            choice = input("Nhập lựa chọn: ").strip()
            if choice == '1':
                self.handle_search_room()
            elif choice == '2':
                self.handle_search_student()
            elif choice == '0':
                break
            else:
                print("[Lỗi] Lựa chọn không hợp lệ.")

    def handle_search_room(self):
        """Tìm kiếm phòng theo mã (Binary Search) hoặc loại/trạng thái (Linear Search)."""
        print("\n--- TÌM KIẾM PHÒNG ---")
        print("1. Tìm theo mã phòng (Binary Search)")
        print("2. Tìm theo loại phòng hoặc trạng thái (Linear Search)")
        sub = input("Chọn cách tìm: ").strip()

        if sub == '1':
            room_id = input("Nhập mã phòng cần tìm: ").strip()
            room = search_service.search_room_by_id(room_id)
            if room:
                display_service.display_room_list([room], title=f"KẾT QUẢ TÌM PHÒNG '{room_id}'")
            else:
                display_service.display_not_found(f"phòng '{room_id}'")
        elif sub == '2':
            query = input(
                "Nhập loại phòng (4/6/8) hoặc trạng thái (available/full/maintenance): ").strip()
            results = search_service.search_room_by_type_or_status(query)
            if results:
                sorted_results = search_service._insertion_sort_room_by_price(results[:])
                display_service.display_room_list(
                    sorted_results, title=f"KẾT QUẢ TÌM KIẾM '{query}' (sắp xếp theo giá)")
            else:
                display_service.display_not_found(f"phòng nào phù hợp với '{query}'")
        else:
            display_service.display_error("Lựa chọn không hợp lệ.")

    def handle_search_student(self):
        """Tìm kiếm sinh viên theo mã (Hash Table) hoặc tên (Linear Search)."""
        print("\n--- TÌM KIẾM SINH VIÊN ---")
        print("1. Tìm theo mã sinh viên (Hash Table)")
        print("2. Tìm theo tên (Linear Search)")
        sub = input("Chọn cách tìm: ").strip()

        if sub == '1':
            student_id = input("Nhập mã sinh viên cần tìm: ").strip()
            student = search_service.search_student_by_id(student_id)
            if student:
                display_service.display_student_list(
                    [student], title=f"KẾT QUẢ TÌM SINH VIÊN '{student_id}'")
            else:
                display_service.display_not_found(f"sinh viên '{student_id}'")
        elif sub == '2':
            name_query = input("Nhập tên hoặc một phần tên cần tìm: ").strip()
            results = search_service.search_student_by_name(name_query)
            if results:
                sorted_results = search_service.sort_students_by_name(results)
                display_service.display_student_list(
                    sorted_results, title=f"KẾT QUẢ TÌM KIẾM '{name_query}' (sắp xếp theo tên)")
            else:
                display_service.display_not_found(
                    f"sinh viên nào có tên chứa '{name_query}'")
        else:
            display_service.display_error("Lựa chọn không hợp lệ.")

    # ─────────────────────────────────────────
    # Chức năng 6: Báo cáo thống kê
    # ─────────────────────────────────────────
    def handle_report_menu(self):
        """Vòng lặp menu báo cáo thống kê."""
        while True:
            print("\n=== BÁO CÁO THỐNG KÊ ===")
            print("1. Danh sách sinh viên nợ phí quá hạn")
            print("2. Tỉ lệ lấp đầy theo loại phòng")
            print("3. Doanh thu theo tháng")
            print("0. Quay lại menu chính")

            choice = input("Nhập lựa chọn: ").strip()
            if choice == '1':
                self.handle_report_overdue()
            elif choice == '2':
                self.handle_report_occupancy()
            elif choice == '3':
                self.handle_report_revenue()
            elif choice == '0':
                break
            else:
                print("[Lỗi] Lựa chọn không hợp lệ.")

    def handle_report_overdue(self):
        """Báo cáo danh sách sinh viên có hóa đơn quá hạn chưa thanh toán."""
        data = report_service.report_overdue_students()
        display_service.display_report_overdue(data)

    def handle_report_occupancy(self):
        """Báo cáo tỉ lệ lấp đầy từng loại phòng và thống kê theo trạng thái."""
        data = report_service.report_room_occupancy_rate()
        display_service.display_report_occupancy(data)

        status_data = report_service.report_rooms_by_status()
        print("\n--- THỐNG KÊ THEO TRẠNG THÁI ---")
        print(f"  Còn chỗ  (available)  : {status_data.get('available', 0)} phòng")
        print(f"  Hết chỗ  (full)       : {status_data.get('full', 0)} phòng")
        print(f"  Bảo trì  (maintenance): {status_data.get('maintenance', 0)} phòng")

    def handle_report_revenue(self):
        """Báo cáo tổng doanh thu các hóa đơn đã thanh toán trong tháng."""
        print("\n--- DOANH THU THEO THÁNG ---")
        try:
            month = int(input("Nhập tháng (1-12): ").strip())
            year = int(input("Nhập năm (VD: 2025): ").strip())
        except ValueError:
            display_service.display_error("Tháng và năm phải là số nguyên.")
            return

        revenue = report_service.report_monthly_revenue(month, year)
        print(f"\n=== DOANH THU THÁNG {month}/{year} ===")
        print(f"Tổng doanh thu đã thu: {revenue:,.0f} VNĐ")


if __name__ == "__main__":
    app = AppController()
    app.handle_choices()

import sys
import contract_manager
import data_manager

class AppController:
    def __init__(self):
        # Đảm bảo dữ liệu được load trước khi chạy chương trình
        data_manager.load_all_data_once()

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
            choice = input("Vui lòng chọn chức năng (0-6): ")
            
            if choice == '1':
                print("Chức năng Quản lý phòng (Leader đang phát triển...)")
            elif choice == '2':
                print("Chức năng Quản lý sinh viên (Leader đang phát triển...)")
            elif choice == '3':
                self.handle_contract_menu()
            elif choice == '4':
                print("Chức năng Quản lý thu phí (TV3 đang phát triển...)")
            elif choice == '5':
                print("Chức năng Tra cứu (Đang phát triển...)")
            elif choice == '6':
                print("Chức năng Báo cáo (Đang phát triển...)")
            elif choice == '0':
                print("Cảm ơn bạn đã sử dụng hệ thống. Tạm biệt!")
                sys.exit(0)
            else:
                print("Lỗi: Lựa chọn không hợp lệ. Vui lòng nhập số từ 0 đến 6.")

    def handle_contract_menu(self):
        while True:
            print("\n--- 3. QUẢN LÝ HỢP ĐỒNG ---")
            print("1. Đăng ký phòng mới")
            print("2. Gia hạn hợp đồng")
            print("3. Chuyển phòng")
            print("4. Thanh lý hợp đồng")
            print("0. Quay lại menu chính")
            
            choice = input("Chọn chức năng (0-4): ")
            if choice == '1':
                print("\n-- ĐĂNG KÝ PHÒNG --")
                student_id = input("Nhập mã sinh viên: ")
                room_id = input("Nhập mã phòng: ")
                start_date = input("Nhập ngày bắt đầu (YYYY-MM-DD): ")
                end_date = input("Nhập ngày kết thúc (YYYY-MM-DD): ")
                contract_manager.register_room(student_id, room_id, start_date, end_date)
            elif choice == '2':
                print("\n-- GIA HẠN HỢP ĐỒNG --")
                contract_id = input("Nhập mã hợp đồng cần gia hạn: ")
                new_end_date = input("Nhập ngày kết thúc mới (YYYY-MM-DD): ")
                contract_manager.extend_contract(contract_id, new_end_date)
            elif choice == '3':
                print("\n-- CHUYỂN PHÒNG --")
                contract_id = input("Nhập mã hợp đồng: ")
                new_room_id = input("Nhập mã phòng mới muốn chuyển tới: ")
                contract_manager.transfer_room(contract_id, new_room_id)
            elif choice == '4':
                print("\n-- THANH LÝ HỢP ĐỒNG --")
                contract_id = input("Nhập mã hợp đồng cần thanh lý: ")
                confirm = input(f"Bạn có chắc chắn muốn thanh lý hợp đồng {contract_id}? (y/n): ")
                if confirm.lower() == 'y':
                    contract_manager.terminate_contract(contract_id)
                else:
                    print("Đã hủy thao tác thanh lý.")
            elif choice == '0':
                break
            else:
                print("Lỗi: Lựa chọn không hợp lệ. Vui lòng chọn từ 0 đến 4.")

# Nếu muốn test trực tiếp file này (thay vì chạy từ main.py)
if __name__ == "__main__":
    app = AppController()
    app.handle_choices()

import sys
from program_controller import AppController

def main():
    """Điểm khởi động chương trình quản lý ký túc xá."""
    print("=" * 50)
    print("   CHÀO MỪNG ĐẾN HỆ THỐNG QUẢN LÝ KÝ TÚC XÁ")
    print("   Môn: Kỹ thuật Lập trình — MI3310")
    print("=" * 50)

    try:
        app = AppController()
        app.handle_choices()
    except KeyboardInterrupt:
        print("\n\nChương trình bị ngắt. Tạm biệt!")
        sys.exit(0)

if __name__ == "__main__":
    main()

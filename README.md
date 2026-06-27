# Hệ thống Quản lý Ký túc xá

Ứng dụng quản lý sinh viên, phòng, hợp đồng thuê và hóa đơn dịch vụ cho ký túc xá.

## Yêu cầu

- Python 3.7+

## Cài đặt

```bash
# Clone hoặc tải project
cd project

# Chạy chương trình
python main.py
```

## Cấu trúc thư mục

```
project/
├── main.py                  # Điểm vào chính
├── models.py                # Định nghĩa các class (Room, Student, Contract, ServiceBill)
├── data_manager.py          # Quản lý lưu/tải dữ liệu JSON
├── room_manager.py          # Quản lý phòng
├── student_manager.py       # Quản lý sinh viên
├── contract_manager.py      # Quản lý hợp đồng
├── service_fee_calculator.py # Tính tiền điện, nước
├── program_controller.py    # Logic điều khiển chương trình
├── display_service.py       # In ra màn hình
├── search_service.py        # Tìm kiếm
├── report_service.py        # Báo cáo
└── data/                    # Dữ liệu JSON
    ├── students.json
    ├── rooms.json
    ├── contracts.json
    └── service_bills.json
```

## Chức năng chính

- **Quản lý sinh viên**: Thêm, sửa, xóa, tìm kiếm sinh viên
- **Quản lý phòng**: Xem phòng trống, cập nhật trạng thái
- **Quản lý hợp đồng**: Đăng ký, gia hạn, chuyển phòng, thanh lý hợp đồng
- **Hóa đơn dịch vụ**: Tính tiền điện, nước; thanh toán; xem quá hạn
- **Báo cáo**: Doanh thu, phòng trống, hóa đơn chưa thanh toán

## Sử dụng

Chạy `python main.py` và làm theo menu hướng dẫn.

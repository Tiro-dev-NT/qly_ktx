import datetime
import data_manager as dm
from models import Contract
import room_manager
import student_manager

def get_contract_by_id(contract_id: str) -> Contract | None:
    """Lấy thông tin hợp đồng theo mã hợp đồng"""
    dm._ensure_data_loaded()
    for contract in dm.ALL_CONTRACTS:
        if contract.contract_id == contract_id:
            return contract
    return None

def get_active_contract_of_student(student_id: str) -> Contract | None:
    """Tìm hợp đồng đang active của sinh viên"""
    dm._ensure_data_loaded()
    for contract in dm.ALL_CONTRACTS:
        if contract.student_id == student_id and contract.is_active():
            return contract
    return None

def get_contracts_by_room(room_id: str) -> list[Contract]:
    """Lấy tất cả hợp đồng (kể cả hết hạn/thanh lý) của một phòng"""
    dm._ensure_data_loaded()
    return [contract for contract in dm.ALL_CONTRACTS if contract.room_id == room_id]

def _generate_contract_id() -> str:
    """Tự sinh mã hợp đồng mới (VD: HD001, HD002)"""
    dm._ensure_data_loaded()
    if not dm.ALL_CONTRACTS:
        return "HD001"
    
    # Tìm số lớn nhất trong các mã HD hiện tại
    max_num = 0
    for contract in dm.ALL_CONTRACTS:
        if contract.contract_id.startswith("HD"):
            try:
                num = int(contract.contract_id[2:])
                if num > max_num:
                    max_num = num
            except ValueError:
                continue
                
    return f"HD{max_num + 1:03d}"

def register_room(student_id: str, room_id: str, start_date: str, end_date: str) -> bool:
    """
    Đăng ký thuê phòng mới.
    Đầu vào:
        - student_id: Mã sinh viên
        - room_id: Mã phòng
        - start_date, end_date: Ngày bắt đầu và kết thúc (YYYY-MM-DD)
    Đầu ra:
        - True nếu thành công, False nếu thất bại.
    """
    dm._ensure_data_loaded()
    
    # 1. Kiểm tra sinh viên tồn tại
    student = student_manager.get_student_by_id(student_id)
    if not student:
        print(f"Lỗi: Không tìm thấy sinh viên mã {student_id}")
        return False
        
    # 2. Kiểm tra phòng tồn tại
    room = room_manager.get_room_by_id(room_id)
    if not room:
        print(f"Lỗi: Không tìm thấy phòng mã {room_id}")
        return False
        
    # 3. Kiểm tra sinh viên chưa có hợp đồng active nào
    if get_active_contract_of_student(student_id):
        print(f"Lỗi: Sinh viên {student_id} đang có hợp đồng active.")
        return False
        
    # 4. Kiểm tra phòng còn chỗ
    if not room_manager.check_room_availability(room_id):
        print(f"Lỗi: Phòng {room_id} đã hết chỗ hoặc đang bảo trì.")
        return False
        
    # 5. Kiểm tra ngày hợp lệ
    try:
        start = datetime.date.fromisoformat(start_date)
        end = datetime.date.fromisoformat(end_date)
        if start >= end:
            print("Lỗi: Ngày kết thúc phải lớn hơn ngày bắt đầu.")
            return False
    except ValueError:
        print("Lỗi: Định dạng ngày không hợp lệ. Vui lòng dùng YYYY-MM-DD.")
        return False
        
    # 6. Tạo Contract mới
    new_contract_id = _generate_contract_id()
    created_date = datetime.date.today().isoformat()
    new_contract = Contract(
        contract_id=new_contract_id,
        student_id=student_id,
        room_id=room_id,
        start_date=start_date,
        end_date=end_date,
        status="active",
        created_date=created_date
    )
    
    # 7. Lưu vào cache và file
    dm.ALL_CONTRACTS.append(new_contract)
    dm.save_contracts(dm.ALL_CONTRACTS)
    
    # 8. Cập nhật sĩ số phòng
    room_manager.update_occupancy(room_id, 1)
    
    print(f"Thành công: Đã đăng ký phòng {room_id} cho sinh viên {student_id}. Mã HĐ: {new_contract_id}")
    return True

def extend_contract(contract_id: str, new_end_date: str) -> bool:
    """
    Gia hạn hợp đồng.
    Đầu vào:
        - contract_id: Mã hợp đồng cần gia hạn
        - new_end_date: Ngày kết thúc mới (YYYY-MM-DD)
    """
    dm._ensure_data_loaded()
    
    # 1. Kiểm tra hợp đồng tồn tại
    contract = get_contract_by_id(contract_id)
    if not contract:
        print(f"Lỗi: Không tìm thấy hợp đồng mã {contract_id}")
        return False
        
    # 2. Kiểm tra hợp đồng đang active
    if not contract.is_active():
        print(f"Lỗi: Hợp đồng {contract_id} không trong trạng thái active.")
        return False
        
    # 3. Kiểm tra ngày mới > ngày hiện tại
    try:
        current_end = datetime.date.fromisoformat(contract.end_date)
        new_end = datetime.date.fromisoformat(new_end_date)
        if new_end <= current_end:
            print("Lỗi: Ngày gia hạn mới phải lớn hơn ngày kết thúc hiện tại.")
            return False
    except ValueError:
        print("Lỗi: Định dạng ngày không hợp lệ. Vui lòng dùng YYYY-MM-DD.")
        return False
        
    # 4. Cập nhật và lưu
    contract.end_date = new_end_date
    dm.save_contracts(dm.ALL_CONTRACTS)
    
    print(f"Thành công: Đã gia hạn hợp đồng {contract_id} đến ngày {new_end_date}.")
    return True

def transfer_room(contract_id: str, new_room_id: str) -> bool:
    """
    Chuyển phòng cho sinh viên.
    Đầu vào:
        - contract_id: Mã hợp đồng hiện tại
        - new_room_id: Mã phòng mới muốn chuyển đến
    """
    dm._ensure_data_loaded()
    
    # 1. Kiểm tra hợp đồng active tồn tại
    contract = get_contract_by_id(contract_id)
    if not contract:
        print(f"Lỗi: Không tìm thấy hợp đồng mã {contract_id}")
        return False
        
    if not contract.is_active():
        print(f"Lỗi: Hợp đồng {contract_id} không trong trạng thái active.")
        return False
        
    old_room_id = contract.room_id
    if old_room_id == new_room_id:
        print("Lỗi: Phòng mới giống hệt phòng hiện tại.")
        return False
        
    # 2. Kiểm tra phòng mới tồn tại và còn chỗ
    new_room = room_manager.get_room_by_id(new_room_id)
    if not new_room:
        print(f"Lỗi: Không tìm thấy phòng mã {new_room_id}")
        return False
        
    if not room_manager.check_room_availability(new_room_id):
        print(f"Lỗi: Phòng {new_room_id} đã hết chỗ hoặc đang bảo trì.")
        return False
        
    # 3. Cập nhật occupancy: phòng cũ -1, phòng mới +1
    room_manager.update_occupancy(old_room_id, -1)
    room_manager.update_occupancy(new_room_id, 1)
    
    # 4. Cập nhật room_id trong contract, save
    contract.room_id = new_room_id
    dm.save_contracts(dm.ALL_CONTRACTS)
    
    print(f"Thành công: Đã chuyển sinh viên {contract.student_id} từ phòng {old_room_id} sang phòng {new_room_id}.")
    return True

def terminate_contract(contract_id: str) -> bool:
    """
    Thanh lý hợp đồng (Kết thúc sớm hoặc đúng hạn).
    Đầu vào:
        - contract_id: Mã hợp đồng cần thanh lý
    """
    dm._ensure_data_loaded()
    
    # 1. Kiểm tra hợp đồng active tồn tại
    contract = get_contract_by_id(contract_id)
    if not contract:
        print(f"Lỗi: Không tìm thấy hợp đồng mã {contract_id}")
        return False
        
    if not contract.is_active():
        print(f"Lỗi: Hợp đồng {contract_id} đã kết thúc hoặc bị thanh lý từ trước.")
        return False
        
    # 2. Đổi status → "terminated", gọi update_occupancy(-1), save
    contract.status = "terminated"
    room_id = contract.room_id
    
    room_manager.update_occupancy(room_id, -1)
    dm.save_contracts(dm.ALL_CONTRACTS)
    
    print(f"Thành công: Đã thanh lý hợp đồng {contract_id}, trả lại 1 chỗ cho phòng {room_id}.")
    return True


from models import Room
import data_manager as dm

def get_room_by_id(room_id: str):
    """Lấy thông tin phòng theo mã phòng"""
    dm._ensure_data_loaded()
    for room in dm.ALL_ROOMS:
        if room.room_id == room_id:
            return room
    return None
def get_all_rooms() -> list[Room]:
    """Trả về toàn bộ danh sách ROOM"""
    dm._ensure_data_loaded()
    return dm.ALL_ROOMS
        
def get_available_rooms() -> list[Room]:
    """Trả về ROOM còn ở trạng thái available"""
    dm._ensure_data_loaded()
    return [room for room in dm.ALL_ROOMS if room.is_available()]
    
def get_rooms_by_type(room_type: int) -> list[Room]:
    """Trả về ROOM theo type"""
    dm._ensure_data_loaded()
    return [room for room in dm.ALL_ROOMS  if room_type == room.room_type]
def add_room(room_id, room_type, price, capacity, floor, building) -> bool:
    if get_room_by_id(room_id) is not None:
        return False  
    dm.ALL_ROOMS.append(Room(
        room_id           = room_id,
        room_type         = room_type,
        price_per_month   = price,
        capacity          = capacity,
        current_occupants = 0,           # phòng mới chưa có ai ở
        status            = "available", # phòng mới mặc định còn chỗ
        floor             = floor,
        building          = building
    ))
    dm.save_rooms(dm.ALL_ROOMS)
    return True

def update_room(room_id, **kwargs) -> bool:
    room = get_room_by_id(room_id)
    if room is None: #Room không tồn tại
        return False
    # kwargs = {"price_per_month": 700000, "floor": 3}, tránh phải viết nhiều hàm update
    for k, v in kwargs.items():
        if hasattr(room, k):
            setattr(room, k, v)
    dm.save_rooms(dm.ALL_ROOMS)
    return True        

def delete_room(room_id: str) -> bool:
    room = get_room_by_id(room_id)
    if room is None: #room không tồn tại
        return False
    dm.ALL_ROOMS.remove(room)
    dm.save_rooms(dm.ALL_ROOMS)
    return True

def update_occupancy(room_id: str, delta: int) -> bool:# +1 khi vào, -1 khi ra
    room = get_room_by_id(room_id)
    if room is None:
        return False
    room.current_occupants = room.current_occupants + delta
    # Nếu cộng quá số lượng
    if room.current_occupants < 0 or room.current_occupants > room.capacity:
        room.current_occupants = room.current_occupants - delta  # rollback
        return False
    dm.save_rooms(dm.ALL_ROOMS)
    return True

def check_room_availability(room_id: str) -> bool:
    room = get_room_by_id(room_id)
    if room is None:
        return False
    return room.is_available()
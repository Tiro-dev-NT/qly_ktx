import os
import json
from project.models import Room, Student, Contract, ServiceBill

# Đường dẫn folder DATA, thư viện os giúp ghép đường dẫn
DATA_DIR = "data"
ROOMS_FILE    = os.path.join(DATA_DIR, "rooms.json")
STUDENTS_FILE = os.path.join(DATA_DIR, "students.json")
CONTRACTS_FILE = os.path.join(DATA_DIR, "contracts.json")
BILLS_FILE    = os.path.join(DATA_DIR, "service_bills.json")

# Biến toàn cục (cache)
ALL_ROOMS: list = []
ALL_STUDENTS: list = []
ALL_CONTRACTS: list = []
ALL_BILLS: list = []

_data_loaded = False  #Data chưa load gì (Cờ)


def load_all_data_once():  # Tải tất cả vào cache
    global _data_loaded
    if _data_loaded:
        return
    load_rooms()
    load_students()
    load_contracts()
    load_service_bills()
    _data_loaded = True #Data đã được load
def load_rooms() -> list[Room]: #Load room từ data
    global ALL_ROOMS
    raw_list = _read_json(ROOMS_FILE)
    ALL_ROOMS = [
        Room(
            room_id             = item["room_id"],
            room_type           = item["room_type"],
            price_per_month     = item["price_per_month"],
            capacity            = item["capacity"],
            current_occupants   = item["current_occupants"],
            status              = item["status"],
            floor               = item["floor"],
            building            = item["building"]
            )
        for item in raw_list
    ] #dùng list comprehension
    return ALL_ROOMS
def load_students() -> list[Student]:
    global ALL_STUDENTS
    raw_list = _read_json(STUDENTS_FILE)
    ALL_STUDENTS = [
        Student(
            student_id      = item["student_id"],
            full_name       = item["full_name"],
            class_name      = item["class_name"],
            phone           = item["phone"],
            email           = item["email"],
            policy_type     = item["policy_type"],
            enrollment_date = item["enrollment_date"]
        )
        for item in raw_list
    ]
    return ALL_STUDENTS


def load_contracts() -> list[Contract]:
    global ALL_CONTRACTS
    raw_list = _read_json(CONTRACTS_FILE)
    ALL_CONTRACTS = [
        Contract(
            contract_id  = item["contract_id"],
            student_id   = item["student_id"],
            room_id      = item["room_id"],
            start_date   = item["start_date"],
            end_date     = item["end_date"],
            status       = item["status"],
            created_date = item["created_date"]
        )
        for item in raw_list
    ]
    return ALL_CONTRACTS


def load_service_bills() -> list[ServiceBill]:
    global ALL_BILLS
    raw_list = _read_json(BILLS_FILE)
    ALL_BILLS = [
        ServiceBill(
            bill_id           = item["bill_id"],
            contract_id       = item["contract_id"],
            room_id           = item["room_id"],
            month             = item["month"],
            year              = item["year"],
            electric_start    = item["electric_start"],
            electric_end      = item["electric_end"],
            water_start       = item["water_start"],
            water_end         = item["water_end"],
            electric_amount   = item["electric_amount"],
            water_amount      = item["water_amount"],
            total_amount      = item["total_amount"],
            status            = item["status"],
            due_date          = item["due_date"],
            paid_date         = item["paid_date"]
        )
        for item in raw_list
    ]
    return ALL_BILLS

def save_rooms(rooms: list[Room]):
    """Lưu list Room xuống rooms.json"""
    data = [room.to_dict() for room in rooms]  # chuyển list Room → list dict
    _write_json(ROOMS_FILE, data)              # ghi xuống file
def save_students(students: list[Student]):
    pass
def save_contracts(contracts: list[Contract]):
    pass
def save_service_bills(bills: list[ServiceBill]):
    pass
def _read_json(filepath: str) -> list:
    pass
def _write_json(filepath: str, data: list):
    pass
def _ensure_data_loaded():
    pass
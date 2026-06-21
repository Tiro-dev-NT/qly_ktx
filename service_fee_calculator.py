import data_manager as dm
from models import ServiceBill
from datetime import datetime, timedelta

# Biểu giá điện sinh hoạt lũy tiến 6 bậc của EVN (đơn giá CHƯA gồm VAT).
# Mỗi phần tử: (số kWh tối đa trong bậc, đơn giá đ/kWh).
ELECTRIC_TIERS = [(50, 1984),            # Bậc 1: 50 kWh đầu tiên (0-50)
                  (50, 2050),            # Bậc 2: 50 kWh tiếp theo (51-100)
                  (100, 2380),           # Bậc 3: 100 kWh tiếp theo (101-200)
                  (100, 2998),           # Bậc 4: 100 kWh tiếp theo (201-300)
                  (100, 3350),           # Bậc 5: 100 kWh tiếp theo (301-400)
                  (float('inf'), 3460)   # Bậc 6: các kWh còn lại (401 trở lên)
                  ]

ELECTRIC_VAT_RATE = 0.08  # Thuế VAT điện sinh hoạt 8%
WATER_UNIT_PRICE = 15929  # Giá nước: đồng/m3 (đã gồm VAT + phí dịch vụ thoát nước)

def calculate_electric_fee(kwh_used: int) -> float:
    """Tính tiền điện theo biểu giá lũy tiến 6 bậc, kết quả ĐÃ gồm VAT 8%."""
    if kwh_used <= 0:
        return 0.0

    base_amount = 0.0
    remaining_kwh = kwh_used
    for limit, price in ELECTRIC_TIERS:
        if remaining_kwh <= 0:
            break
        kwh_in_tier = min(remaining_kwh, limit)  # số kWh tính trong bậc này
        base_amount += kwh_in_tier * price
        remaining_kwh -= kwh_in_tier

    total_fee = base_amount * (1 + ELECTRIC_VAT_RATE)  # cộng VAT vào tiền điện
    return round(total_fee, 2)

def calculate_water_fee(m3_used: int) -> float:
    return m3_used * WATER_UNIT_PRICE

def _generate_bill_id(contract_id: str, month: int, year: int) -> str:
    return f"{contract_id}_{year}_{month:02d}"

def record_monthly_usage(room_id: str, month: int, year: int, e_start: int, e_end: int, w_start: int, w_end: int) -> bool:
    if e_end < e_start or w_end < w_start:
        return False

    active_contract = None
    for contract in dm.ALL_CONTRACTS:
        if contract.room_id == room_id and contract.status == "active":
            active_contract = contract
            break

    if not active_contract:
        return False

    bill_id = _generate_bill_id(active_contract.contract_id, month, year)
    
    for bill in dm.ALL_BILLS:
        if bill.bill_id == bill_id:
            return False

    electric_used = e_end - e_start
    water_used = w_end - w_start
    
    e_amount = calculate_electric_fee(electric_used)
    w_amount = calculate_water_fee(water_used)
    total_amount = e_amount + w_amount

    due_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

    new_bill = ServiceBill(
        bill_id=bill_id, contract_id=active_contract.contract_id, room_id=room_id,
        month=month, year=year, electric_start=e_start, electric_end=e_end,
        water_start=w_start, water_end=w_end, electric_amount=e_amount,
        water_amount=w_amount, total_amount=total_amount, status="unpaid",
        due_date=due_date, paid_date=None
    )

    dm.ALL_BILLS.append(new_bill)
    dm.save_service_bills(dm.ALL_BILLS)
    return True

def pay_bill(bill_id: str) -> bool:
    for bill in dm.ALL_BILLS:
        if bill.bill_id == bill_id and bill.status == "unpaid":
            bill.status = "paid"
            bill.paid_date = datetime.now().strftime("%Y-%m-%d")
            dm.save_service_bills(dm.ALL_BILLS)
            return True
    return False

def get_bills_by_room(room_id: str, month: int = None, year: int = None) -> list:
    result = []
    for bill in dm.ALL_BILLS:
        if bill.room_id == room_id:
            if (month is None or bill.month == month) and (year is None or bill.year == year):
                result.append(bill)
    return result

def get_unpaid_bills() -> list:
    return [bill for bill in dm.ALL_BILLS if bill.status == "unpaid"]

def get_overdue_bills() -> list:
    overdue = []
    current_date = datetime.now().strftime("%Y-%m-%d")
    for bill in dm.ALL_BILLS:
        if bill.status == "unpaid" and bill.due_date < current_date:
            overdue.append(bill)
    return overdue
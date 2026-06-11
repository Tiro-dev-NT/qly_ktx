import data_manager
from models import ServiceBill
from datetime import datetime, timedelta

ELECTRIC_TIERS = [(50, 1806), (100, 1866), (200, 2167), (float('inf'), 2729)]
WATER_UNIT_PRICE = 15929

def calculate_electric_fee(kwh_used: int) -> float:
    total_fee = 0.0
    remaining_kwh = kwh_used
    previous_limit = 0

    for limit, price in ELECTRIC_TIERS:
        tier_amount = limit - previous_limit
        if remaining_kwh <= 0:
            break
        if remaining_kwh > tier_amount and limit != float('inf'):
            total_fee += tier_amount * price
            remaining_kwh -= tier_amount
        else:
            total_fee += remaining_kwh * price
            remaining_kwh = 0
        previous_limit = limit
    return total_fee

def calculate_water_fee(m3_used: int) -> float:
    return m3_used * WATER_UNIT_PRICE

def _generate_bill_id(contract_id: str, month: int, year: int) -> str:
    return f"{contract_id}_{year}_{month:02d}"

def record_monthly_usage(room_id: str, month: int, year: int, e_start: int, e_end: int, w_start: int, w_end: int) -> bool:
    if e_end < e_start or w_end < w_start:
        return False

    active_contract = None
    for contract in data_manager.ALL_CONTRACTS:
        if contract.room_id == room_id and contract.status == "active":
            active_contract = contract
            break

    if not active_contract:
        return False

    bill_id = _generate_bill_id(active_contract.contract_id, month, year)
    
    for bill in data_manager.ALL_BILLS:
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

    data_manager.ALL_BILLS.append(new_bill)
    data_manager.save_service_bills(data_manager.ALL_BILLS)
    return True

def pay_bill(bill_id: str) -> bool:
    for bill in data_manager.ALL_BILLS:
        if bill.bill_id == bill_id and bill.status == "unpaid":
            bill.status = "paid"
            bill.paid_date = datetime.now().strftime("%Y-%m-%d")
            data_manager.save_service_bills(data_manager.ALL_BILLS)
            return True
    return False

def get_bills_by_room(room_id: str, month: int = None, year: int = None) -> list:
    result = []
    for bill in data_manager.ALL_BILLS:
        if bill.room_id == room_id:
            if (month is None or bill.month == month) and (year is None or bill.year == year):
                result.append(bill)
    return result

def get_unpaid_bills() -> list:
    return [bill for bill in data_manager.ALL_BILLS if bill.status == "unpaid"]

def get_overdue_bills() -> list:
    overdue = []
    current_date = datetime.now().strftime("%Y-%m-%d")
    for bill in data_manager.ALL_BILLS:
        if bill.status == "unpaid" and bill.due_date < current_date:
            overdue.append(bill)
    return overdue
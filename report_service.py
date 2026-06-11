import data_manager
from datetime import datetime

def report_overdue_students() -> list:
    overdue_bills = []
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    for bill in data_manager.ALL_BILLS:
        if bill.status == "unpaid" and bill.due_date < current_date:
            overdue_bills.append(bill)
            
    result = []
    for bill in overdue_bills:
        contract = None
        for c in data_manager.ALL_CONTRACTS:
            if c.contract_id == bill.contract_id:
                contract = c
                break
        if contract:
            student = None
            for s in data_manager.ALL_STUDENTS:
                if s.student_id == contract.student_id:
                    student = s
                    break
            if student:
                result.append({
                    "student_id": student.student_id,
                    "full_name": student.full_name,
                    "room_id": bill.room_id,
                    "bill_id": bill.bill_id,
                    "total_amount": bill.total_amount,
                    "due_date": bill.due_date
                })
    return result

def report_room_occupancy_rate() -> list:
    stats = {4: {"total": 0, "occupied": 0}, 6: {"total": 0, "occupied": 0}, 8: {"total": 0, "occupied": 0}}
    
    for room in data_manager.ALL_ROOMS:
        rtype = room.room_type
        if rtype in stats:
            stats[rtype]["total"] += room.capacity
            stats[rtype]["occupied"] += room.current_occupants
            
    result = []
    for rtype, data in stats.items():
        rate = 0.0
        if data["total"] > 0:
            rate = (data["occupied"] / data["total"]) * 100
        result.append({
            "room_type": rtype,
            "occupancy_rate": round(rate, 2)
        })
    return result

def report_monthly_revenue(month: int, year: int) -> float:
    total_revenue = 0.0
    for bill in data_manager.ALL_BILLS:
        if bill.month == month and bill.year == year and bill.status == "paid":
            total_revenue += bill.total_amount
    return total_revenue

def report_rooms_by_status() -> dict:
    counts = {"available": 0, "full": 0, "maintenance": 0}
    for room in data_manager.ALL_ROOMS:
        if room.status in counts:
            counts[room.status] += 1
    return counts